# Lunexa (Streamlit)

Streamlit version of **Lunexa: Lung Cancer Prognosis and Risk Assessment**.

Same multimodal pipeline as the React + FastAPI app:

- CT DICOM series + RTSTRUCT
- MedicalNet + radiomics + clinical fusion
- Risk score, median survival, 1y / 2y survival probabilities

## Folder contents

```
lung-cancer-streamlit/
├── app.py                         # Streamlit UI (all pages)
├── inference.py                   # Model + DICOM / RTSTRUCT pipeline
├── model_config_final_v2.json
├── baseline_hazard.json
├── fusion_model_final_v2.pt
├── scalers_final_v2.pkl
├── requirements.txt
└── README.md
```

## Run locally

```bash
cd lung-cancer-streamlit
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Opens **http://localhost:8501**

## Pages (sidebar)

| Page | Content |
|------|---------|
| Home | Intro and metrics |
| Predict | DICOM + RTSTRUCT + clinical → risk |
| Symptoms | Guidance + YouTube |
| Help | DICOM / staging glossary |
| How it Works | Pipeline steps |
| About | Model + disclaimer |

## Predict inputs

1. Upload **all** `.dcm` files from one CT series (multi-file upload).
2. Upload **one** RTSTRUCT `.dcm`.
3. ROI name (default `GTV-1`).
4. Age, T/N/M, overall stage, histology, gender.
5. **Load preview images** and/or **Predict risk score**.

## Deploy on Streamlit Community Cloud

1. Push this folder to GitHub (include model files via Git LFS if large).
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. New app → select repo → main file `app.py`.
4. Deploy.

**Note:** Free Streamlit Cloud has limited RAM/CPU. Torch + MONAI may be tight or fail on free tier. For heavier use, prefer a machine with ≥8 GB RAM or a paid / HF PRO Docker Space.

## Deploy on Hugging Face Spaces (Streamlit SDK)

If your account allows Streamlit/Gradio Spaces (often needs PRO):

1. Create Space → SDK **Streamlit**.
2. Upload these files (or connect GitHub).
3. Spaces runs `streamlit run app.py`.

## Disclaimer

Research prototype only. Not a medical device. Not for clinical decisions.
