"""
Lunexa core inference - same pipeline as the FastAPI / desktop app.
"""
from __future__ import annotations

import json
import os
import pickle
import tempfile
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import SimpleITK as sitk
from monai.transforms import (
    Compose,
    EnsureChannelFirst,
    Resize,
    ScaleIntensityRange,
    EnsureType,
)
from radiomics import featureextractor
from rt_utils import RTStructBuilder

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "model_config_final_v2.json") as f:
    CONFIG = json.load(f)
with open(BASE_DIR / "scalers_final_v2.pkl", "rb") as f:
    SCALERS = pickle.load(f)
with open(BASE_DIR / "baseline_hazard.json") as f:
    BASELINE_HAZARD = json.load(f)

TARGET_SHAPE = (96, 96, 96)
HU_WINDOW = (-1000, 400)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CT_TRANSFORMS = Compose(
    [
        EnsureChannelFirst(channel_dim="no_channel"),
        Resize(TARGET_SHAPE),
        ScaleIntensityRange(
            a_min=HU_WINDOW[0],
            a_max=HU_WINDOW[1],
            b_min=0.0,
            b_max=1.0,
            clip=True,
        ),
        EnsureType(),
    ]
)


class FusionDeepSurv(nn.Module):
    def __init__(self, ct_dim, rad_dim, clin_dim, ct_hidden=16, dropout=0.3):
        super().__init__()
        self.ct_branch = nn.Sequential(
            nn.Linear(ct_dim, ct_hidden), nn.ReLU(), nn.Dropout(dropout)
        )
        self.rad_branch = nn.Sequential(
            nn.Linear(rad_dim, 16), nn.ReLU(), nn.Dropout(0.2)
        )
        self.clin_branch = nn.Sequential(nn.Linear(clin_dim, clin_dim), nn.ReLU())
        self.head = nn.Sequential(
            nn.Linear(ct_hidden + 16 + clin_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1),
        )

    def forward(self, ct_x, rad_x, clin_x):
        combined = torch.cat(
            [self.ct_branch(ct_x), self.rad_branch(rad_x), self.clin_branch(clin_x)],
            dim=1,
        )
        return self.head(combined).squeeze(-1)


_MODEL = None
_MEDICALNET = None
_RADIOMICS = None


def get_model():
    global _MODEL
    if _MODEL is None:
        m = FusionDeepSurv(
            CONFIG["ct_dim"],
            CONFIG["rad_dim"],
            CONFIG["clin_dim"],
            ct_hidden=CONFIG["ct_hidden"],
        )
        m.load_state_dict(
            torch.load(BASE_DIR / "fusion_model_final_v2.pt", map_location="cpu")
        )
        m.eval()
        _MODEL = m
    return _MODEL


def get_medicalnet():
    global _MEDICALNET
    if _MEDICALNET is None:
        net = torch.hub.load("Warvito/MedicalNet-models", "medicalnet_resnet10")
        net.to(DEVICE)
        net.eval()
        _MEDICALNET = net
    return _MEDICALNET


def get_radiomics_extractor():
    global _RADIOMICS
    if _RADIOMICS is None:
        _RADIOMICS = featureextractor.RadiomicsFeatureExtractor()
    return _RADIOMICS


def build_mask_from_rtstruct(dicom_folder, rtstruct_path, roi_name="GTV-1"):
    rtstruct = RTStructBuilder.create_from(
        dicom_series_path=dicom_folder, rt_struct_path=rtstruct_path
    )
    available = rtstruct.get_roi_names()
    if roi_name not in available:
        raise ValueError(f"ROI '{roi_name}' not found. Available: {available}")
    mask_3d = rtstruct.get_roi_mask_by_name(roi_name)

    reader = sitk.ImageSeriesReader()
    names = reader.GetGDCMSeriesFileNames(dicom_folder)
    reader.SetFileNames(names)
    ct_image = reader.Execute()

    mask_array = np.transpose(mask_3d, (2, 0, 1)).astype(np.uint8)
    mask_image = sitk.GetImageFromArray(mask_array)
    mask_image.CopyInformation(ct_image)
    return mask_image


def load_ct_from_folder(dicom_folder):
    reader = sitk.ImageSeriesReader()
    names = reader.GetGDCMSeriesFileNames(dicom_folder)
    if not names:
        raise ValueError(f"No DICOM series found in: {dicom_folder}")
    reader.SetFileNames(names)
    return reader.Execute()


def extract_ct_embedding(sitk_image):
    model = get_medicalnet()
    arr = sitk.GetArrayFromImage(sitk_image).astype(np.float32)
    tensor = CT_TRANSFORMS(arr).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        x = model.conv1(tensor)
        x = model.bn1(x)
        x = model.relu(x)
        x = model.maxpool(x)
        x = model.layer1(x)
        x = model.layer2(x)
        x = model.layer3(x)
        x = model.layer4(x)
        x = nn.functional.adaptive_avg_pool3d(x, 1)
        return torch.flatten(x, 1).cpu().numpy().flatten()


def extract_radiomics(ct_path, mask_path):
    extractor = get_radiomics_extractor()
    result = extractor.execute(ct_path, mask_path)
    kept_cols = SCALERS["kept_cols"]
    raw_values = []
    for name in kept_cols:
        if name not in result:
            raise KeyError(f"Missing radiomics feature: {name}")
        raw_values.append(float(result[name]))
    raw = np.array(raw_values).reshape(1, -1)
    scaled = SCALERS["rad_scaler"].transform(raw)
    scaled_map = {n: v for n, v in zip(kept_cols, scaled.flatten())}
    return np.array([scaled_map[f] for f in CONFIG["rad_feature_names"]])


def estimate_median_survival(risk_score):
    exp_r = np.exp(risk_score)
    for t, H in zip(BASELINE_HAZARD["times"], BASELINE_HAZARD["cumulative_hazard"]):
        if np.exp(-H * exp_r) <= 0.5:
            return t
    return None


def survival_probability_at(risk_score, days):
    exp_r = np.exp(risk_score)
    H_at_t = 0.0
    for t, H in zip(BASELINE_HAZARD["times"], BASELINE_HAZARD["cumulative_hazard"]):
        if t > days:
            break
        H_at_t = H
    return float(np.exp(-H_at_t * exp_r))


def render_slice_png(array_2d):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import io

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(array_2d, cmap="gray")
    ax.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_previews(dicom_folder, rtstruct_path, roi_name):
    sitk_image = load_ct_from_folder(dicom_folder)
    ct_array = sitk.GetArrayFromImage(sitk_image).astype(np.float32)
    mask_image = build_mask_from_rtstruct(dicom_folder, rtstruct_path, roi_name)
    mask_array = sitk.GetArrayFromImage(mask_image)

    areas = mask_array.sum(axis=(1, 2))
    best = int(np.argmax(areas)) if areas.max() > 0 else ct_array.shape[0] // 2

    windowed = np.clip(ct_array[best], -1000, 400)
    windowed = (windowed - windowed.min()) / (windowed.max() - windowed.min() + 1e-8)

    full = render_slice_png(windowed)

    overlay = np.stack([windowed, windowed, windowed], axis=-1)
    mslice = mask_array[best] > 0
    overlay[mslice] = [1.0, 0.3, 0.3]
    ov = render_slice_png(overlay)

    ys, xs = np.where(mslice)
    if len(ys) > 0:
        margin = 20
        y0 = max(0, ys.min() - margin)
        y1 = min(windowed.shape[0], ys.max() + margin)
        x0 = max(0, xs.min() - margin)
        x1 = min(windowed.shape[1], xs.max() + margin)
        crop = render_slice_png(windowed[y0:y1, x0:x1])
    else:
        crop = full

    return {"full": full, "overlay": ov, "cropped": crop}


def run_prediction(
    dicom_folder,
    rtstruct_path,
    roi_name,
    age,
    t_stage,
    n_stage,
    m_stage,
    overall_stage,
    histology,
    gender,
):
    sitk_image = load_ct_from_folder(dicom_folder)
    ct_emb = extract_ct_embedding(sitk_image).reshape(1, -1)

    tmp_ct = os.path.join(tempfile.gettempdir(), "_lunexa_ct.nii.gz")
    sitk.WriteImage(sitk_image, tmp_ct)

    mask_image = build_mask_from_rtstruct(dicom_folder, rtstruct_path, roi_name)
    tmp_mask = os.path.join(tempfile.gettempdir(), "_lunexa_mask.nii.gz")
    sitk.WriteImage(mask_image, tmp_mask)

    rad = extract_radiomics(tmp_ct, tmp_mask).reshape(1, -1)

    hist_dummy = {f"hist_{c}": 0.0 for c in CONFIG["histology_categories"]}
    hist_dummy[f"hist_{histology}"] = 1.0

    clin = np.array(
        [
            [
                float(age),
                float(t_stage),
                float(n_stage),
                float(m_stage),
                1.0 if gender == "male" else 0.0,
                CONFIG["stage_map"].get(overall_stage, 0),
                *[hist_dummy[f"hist_{c}"] for c in CONFIG["histology_categories"]],
            ]
        ]
    )

    ct_s = SCALERS["ct_scaler"].transform(ct_emb)
    clin_s = SCALERS["clin_scaler"].transform(clin)
    model = get_model()

    with torch.no_grad():
        risk = model(
            torch.tensor(ct_s, dtype=torch.float32),
            torch.tensor(rad, dtype=torch.float32),
            torch.tensor(clin_s, dtype=torch.float32),
        ).item()

    return {
        "risk_score": risk,
        "median_survival_days": estimate_median_survival(risk),
        "prob_1yr": survival_probability_at(risk, 365),
        "prob_2yr": survival_probability_at(risk, 730),
        "test_cindex": CONFIG["test_cindex"],
    }


def save_uploaded_dicoms(uploaded_files, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for uf in uploaded_files:
        name = Path(uf.name).name
        path = dest_dir / name
        with open(path, "wb") as f:
            f.write(uf.getbuffer())
    return dest_dir


def get_config():
    return {
        "test_cindex": CONFIG["test_cindex"],
        "val_cindex": CONFIG.get("val_cindex"),
        "stage_options": list(CONFIG["stage_map"].keys()),
        "histology_options": CONFIG["histology_categories"],
    }
