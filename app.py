"""
Lunexa - Streamlit web app
Lung Cancer Prognosis and Risk Assessment
"""

import json
import math
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Lunexa | Lung Cancer Prognosis",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------
SLIDESHOW = [
    {
        "url": "https://www.itnonline.com/sites/default/files/field/image/158096096_m.jpg",
        "title": "Precision imaging meets AI",
        "subtitle": "CT-driven multimodal risk assessment for lung cancer prognosis.",
    },
    {
        "url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&w=1600&q=80",
        "title": "From scan to survival insight",
        "subtitle": "Deep CT features, radiomics, and clinical data in one pipeline.",
    },
    {
        "url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1600&q=80",
        "title": "Built for research teams",
        "subtitle": "Transparent risk scores with 1- and 2-year survival estimates.",
    },
    {
        "url": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?auto=format&fit=crop&w=1600&q=80",
        "title": "Support, not replace, clinical care",
        "subtitle": "A research tool designed to assist education and exploration.",
    },
]

SYMPTOM_CARDS = [
    {
        "title": "Persistent cough",
        "desc": "A cough that does not go away or gets worse over weeks. May produce blood-tinged sputum.",
        "img": "https://www.houstonmethodist.org/-/media/images/contenthub/article-images/pulmonology/2022/hub_persistentcough_article.ashx?mw=1382&hash=D92AD71303623E5A3C746DF46C066F13",
    },
    {
        "title": "Shortness of breath",
        "desc": "Feeling breathless during routine activities or at rest can signal airway or lung involvement.",
        "img": "https://cdn.scope.digital/Images/Articles/nefes-darligina-ne-iyi-gelir-nefes-darligi-neden-olur-9555156.jpg?tr=w-630,h-420",
    },
    {
        "title": "Chest pain",
        "desc": "Pain that worsens with deep breathing, coughing, or laughing. Often related to the chest wall or pleura.",
        "img": "https://cadenceheart.sg/wp-content/uploads/2022/01/shutterstock_1895012779-1024x576.jpg",
    },
    {
        "title": "Hoarseness and wheezing",
        "desc": "Voice changes or new wheezing may occur if a tumor affects the larynx or large airways.",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYNWONgsOV-AN7dU-MYlTPgKUPFqdgvX4Z8nGTOPssRm-lW1fECp4vK-8&s=10",
    },
    {
        "title": "Unexplained weight loss",
        "desc": "Losing weight without trying, fatigue, and loss of appetite are common systemic signs.",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa_-Xl03se48IrYq8_bsg_aGwzGiwrNluyvKvfTezjRgVsc_DRvILAaCje&s=10",
    },
    {
        "title": "Recurrent infections",
        "desc": "Repeated bronchitis or pneumonia in the same area of the lung can be a warning sign.",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfmtu8yRUjW9ig2juIdDSnhN-gLDB3MzMBCn5xhSlDPR5909W3Ivn0HdlD&s=10",
    },
]

SYMPTOM_HERO = "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1600&q=80"
HELP_HERO = "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=80"
ABOUT_HERO = "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?auto=format&fit=crop&w=1600&q=80"
HOW_HERO = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&q=80"
PREDICT_HERO = "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=1600&q=80"

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}

    .stApp {
        background:
            radial-gradient(1200px 500px at 10% -10%, rgba(20,184,166,0.12), transparent 60%),
            radial-gradient(900px 500px at 110% 10%, rgba(37,99,235,0.08), transparent 60%),
            linear-gradient(180deg, #E8F4FC 0%, #F5F9FC 45%, #EEF7F5 100%);
    }
    .block-container {
        padding-top: 0.75rem;
        padding-bottom: 2.5rem;
        max-width: 1320px;
    }

    .nav-shell {
        background: rgba(255,255,255,0.95);
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 10px 16px;
        margin-bottom: 18px;
        box-shadow: 0 6px 24px rgba(15,118,110,0.08);
    }
    .brand-row {
        display: flex; align-items: center; gap: 12px; padding: 4px 0;
    }
    .brand-logo {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, #0F766E, #14B8A6);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 22px;
        box-shadow: 0 4px 14px rgba(15,118,110,0.35);
    }
    .brand-text-title {
        font-size: 1.3rem; font-weight: 800; color: #0F766E; margin: 0; line-height: 1.1;
    }
    .brand-text-tag {
        font-size: 0.72rem; color: #64748B; margin: 0;
    }

    /* Keep nav items on one line */
    .nav-link { white-space: nowrap !important; }
    ul.nav { flex-wrap: nowrap !important; justify-content: center !important; }

    .stButton > button {
        background: linear-gradient(135deg, #0F766E, #14B8A6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(15,118,110,0.25);
    }
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(15,118,110,0.35) !important;
    }
    .stButton > button:disabled {
        background: #94A3B8 !important;
        box-shadow: none !important;
        color: #E2E8F0 !important;
    }
    .stDownloadButton > button {
        background: white !important;
        color: #0F766E !important;
        border: 1px solid #0F766E !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: #E6F2F0 !important;
    }

    .slideshow {
        position: relative; width: 100%; height: 420px;
        overflow: hidden; border-radius: 22px;
        box-shadow: 0 12px 32px rgba(15,118,110,0.16);
        margin-bottom: 18px;
    }
    .slideshow .slide {
        position: absolute; inset: 0; opacity: 0;
        animation: fade 24s infinite;
        background-size: cover; background-position: center;
    }
    .slideshow .slide:nth-child(1) { animation-delay: 0s; }
    .slideshow .slide:nth-child(2) { animation-delay: 6s; }
    .slideshow .slide:nth-child(3) { animation-delay: 12s; }
    .slideshow .slide:nth-child(4) { animation-delay: 18s; }
    @keyframes fade {
        0% { opacity: 0; }
        4% { opacity: 1; }
        25% { opacity: 1; }
        29% { opacity: 0; }
        100% { opacity: 0; }
    }
    .slide-overlay {
        position: absolute; inset: 0;
        background: linear-gradient(120deg, rgba(15,118,110,0.88) 0%, rgba(37,99,235,0.45) 55%, rgba(15,23,42,0.35) 100%);
        display: flex; flex-direction: column; justify-content: flex-end;
        padding: 36px 40px; color: white;
    }
    .slide-title {
        font-size: 2rem; font-weight: 800; margin: 0 0 6px 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    }
    .slide-sub { font-size: 1.05rem; opacity: 0.95; max-width: 620px; margin: 0; }
    .slide-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        color: white; padding: 4px 12px; border-radius: 999px;
        font-size: 0.75rem; letter-spacing: 0.05em; text-transform: uppercase;
        margin-bottom: 10px;
    }

    .info-card {
        background: white; border-radius: 16px; padding: 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0  2px 10px rgba(15,23,42,0.04);
        height: 100%;
    }
    .info-card h4 { color: #0F766E; margin: 0 0 8px 0; font-size: 1.05rem; }
    .info-card p { color: #475569; margin: 0; font-size: 0.95rem; line-height: 1.55; }
    .info-card ul { color: #475569; margin: 0; padding-left: 1.1rem; line-height: 1.7; font-size: 0.95rem; }
    .info-card li { margin-bottom: 4px; }

    .page-hero {
        position: relative; border-radius: 20px; overflow: hidden;
        height: 190px; margin-bottom: 22px;
        box-shadow: 0 6px 20px rgba(15,118,110,0.14);
    }
    .page-hero .bg { position: absolute; inset: 0; background-size: cover; background-position: center; }
    .page-hero .tint { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(15,118,110,0.88), rgba(37,99,235,0.4)); }
    .page-hero .content {
        position: relative; z-index: 2; height: 100%;
        display: flex; flex-direction: column; justify-content: center;
        padding: 0 32px; color: white;
    }
    .page-hero h1 { color: white; font-size: 2rem; margin: 0; }
    .page-hero p { color: rgba(255,255,255,0.92); margin: 6px 0 0 0; }

    .risk-low  { color: #16A34A; font-weight: 700; font-size: 1.35rem; }
    .risk-mod  { color: #F59E0B; font-weight: 700; font-size: 1.35rem; }
    .risk-high { color: #DC2626; font-weight: 700; font-size: 1.35rem; }

    div[data-testid="stMetric"] {
        background: white; padding: 14px 18px; border-radius: 14px;
        border: 1px solid #E2E8F0; box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    }

    .v-err  { background: #FEF2F2; border-left: 4px solid #DC2626; padding: 10px 14px; border-radius: 8px; margin: 6px 0; color: #7F1D1D; font-size: 0.92rem; }
    .v-warn { background: #FFFBEB; border-left: 4px solid #F59E0B; padding: 10px 14px; border-radius: 8px; margin: 6px 0; color: #78350F; font-size: 0.92rem; }
    .v-ok   { background: #F0FDF4; border-left: 4px solid #16A34A; padding: 10px 14px; border-radius: 8px; margin: 6px 0; color: #14532D; font-size: 0.92rem; }
    .info-banner {
        background: #EFF6FF; border-left: 4px solid #2563EB;
        padding: 14px 18px; border-radius: 10px; margin: 8px 0 18px 0;
        color: #1E3A8A; font-size: 0.94rem; line-height: 1.55;
    }

    .about-logo {
        width: 120px; height: 120px; border-radius: 28px;
        background: linear-gradient(135deg, #0F766E, #14B8A6);
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 56px;
        box-shadow: 0 12px 32px rgba(15,118,110,0.35);
        margin: 0 auto 14px auto;
    }
    .step-card {
        background: white; border-radius: 14px; padding: 18px;
        border: 1px solid #E2E8F0;
        display: flex; gap: 14px; align-items: flex-start; margin-bottom: 12px;
    }
    .step-num {
        min-width: 42px; height: 42px; border-radius: 12px;
        background: #E6F2F0; color: #0F766E;
        display: flex; align-items: center; justify-content: center; font-weight: 800;
    }
    .step-card h4 { margin: 0 0 4px 0; color: #0F172A; }
    .step-card p { margin: 0; color: #475569; }

    .symptom-card {
        background: white; border-radius: 14px; overflow: hidden;
        border: 1px solid #E2E8F0; box-shadow: 0 2px 8px rgba(15,23,42,0.04);
        margin-bottom: 14px;
    }
    .symptom-card img { width: 100%; height: 140px; object-fit: cover; display: block; }
    .symptom-card .body { padding: 14px 16px; }
    .symptom-card h4 { color: #0F766E; margin: 0 0 6px 0; }
    .symptom-card p { color: #475569; margin: 0; font-size: 0.92rem; }

    .sect-title { font-size: 1.35rem; font-weight: 700; color: #0F172A; margin: 22px 0 12px 0; }
    .footer-bar {
        margin-top: 2rem; padding: 1.1rem;
        text-align: center; background: white;
        border: 1px solid #E2E8F0; border-radius: 16px;
        color: #64748b; font-size: 0.9rem;
    }
    .footer-bar strong { color: #0F766E; }

    .result-panel {
        background: white; border-radius: 16px; padding: 22px;
        border: 1px solid #E2E8F0; box-shadow: 0 4px 16px rgba(15,118,110,0.08);
        margin-top: 14px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation state
# ---------------------------------------------------------------------------
PAGES = ["Home", "Predict", "Symptoms", "Help", "How it Works", "About"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "nav_epoch" not in st.session_state:
    st.session_state.nav_epoch = 0


def nav_to(page: str):
    """Programmatic navigation. Bumping nav_epoch forces option_menu to
    re-init with the new default_index so the change actually shows."""
    st.session_state.current_page = page
    st.session_state.nav_epoch += 1


# --- Navbar ---
st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
h_left, h_mid, h_right = st.columns([1.8, 6.4, 1.6])

with h_left:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-logo">🫁</div>
            <div>
                <p class="brand-text-title">Lunexa</p>
                <p class="brand-text-tag">Lung Cancer Prognosis</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with h_mid:
    picked = option_menu(
        menu_title=None,
        options=PAGES,
        icons=None,   # icons removed as requested
        default_index=PAGES.index(st.session_state.current_page),
        orientation="horizontal",
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "nav-link": {
                "font-size": "14.5px",
                "text-align": "center",
                "margin": "0 2px",
                "padding": "10px 14px",
                "color": "#475569",
                "background-color": "transparent",
                "--hover-color": "#E6F2F0",
                "border-radius": "10px",
                "white-space": "nowrap",
            },
            "nav-link-selected": {
                "background-color": "#E6F2F0",
                "color": "#0F766E",
                "font-weight": "600",
            },
        },
        # Bumping nav_epoch on programmatic nav gives option_menu a fresh key,
        # which is what actually makes the Start Assessment button work.
        key=f"main_nav_{st.session_state.nav_epoch}",
    )
    if picked != st.session_state.current_page:
        st.session_state.current_page = picked
        st.rerun()

with h_right:
    st.write("")
    st.button(
        "Start Assessment",
        on_click=nav_to,
        args=("Predict",),
        use_container_width=True,
        key="cta_top",
    )
st.markdown("</div>", unsafe_allow_html=True)

page = st.session_state.current_page


def render_slideshow():
    slides_html = ""
    for i, s in enumerate(SLIDESHOW):
        slides_html += (
            f'<div class="slide" style="background-image:url({s["url"]});'
            f'z-index:{len(SLIDESHOW) - i};"></div>'
        )
    first = SLIDESHOW[0]
    st.markdown(
        f"""
        <div class="slideshow">
            {slides_html}
            <div class="slide-overlay">
                <span class="slide-badge">Multimodal Deep Survival Model</span>
                <p class="slide-title">{first["title"]}</p>
                <p class="slide-sub">{first["subtitle"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_hero(title: str, subtitle: str, image_url: str):
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="bg" style="background-image:url({image_url});"></div>
            <div class="tint"></div>
            <div class="content">
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def page_home():
    render_slideshow()

    st.markdown(
        "<h2 style='text-align:center;margin:0.5rem 0 0.35rem 0;'>Welcome to "
        "<span style='color:#0F766E'>Lunexa</span></h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#475569;max-width:720px;margin:0 auto 1.2rem auto;'>"
        "A research tool for lung cancer prognosis. Upload a CT DICOM series and RTSTRUCT "
        "tumor contour, add clinical details, and explore relative risk and survival estimates."
        "</p>",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Test C-index", "0.598")
    m2.metric("Validation C-index", "0.665")
    m3.metric("Modalities fused", "3")
    m4.metric("Radiomics features", "16")

    st.markdown('<p class="sect-title">Why multimodal fusion?</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("CT deep features", "MedicalNet ResNet-10 encodes the full CT volume into a 512-dim embedding."),
        ("Radiomics", "Sixteen selected PyRadiomics descriptors of tumor shape, intensity, and texture."),
        ("Clinical context", "Age, TNM, overall stage, histology, and gender feed a dedicated branch."),
        ("Survival output", "Risk score with median survival and 1-year / 2-year probabilities."),
    ]
    for col, (t, d) in zip([c1, c2, c3, c4], cards):
        col.markdown(f'<div class="info-card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">What you need to run a prediction</p>', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    n1.markdown('<div class="info-card"><h4>1. CT DICOM series</h4><p>Upload all .dcm slices from one CT series so the 3D volume can be rebuilt correctly.</p></div>', unsafe_allow_html=True)
    n2.markdown('<div class="info-card"><h4>2. RTSTRUCT contour</h4><p>Provide the radiotherapy structure file and ROI name (for example GTV-1) for the tumor mask.</p></div>', unsafe_allow_html=True)
    n3.markdown('<div class="info-card"><h4>3. Clinical details</h4><p>Enter age, T/N/M stages, overall stage, histology, and gender to complete the fusion input.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Ready to explore a case?</p>', unsafe_allow_html=True)
    b1, b2, b3, _ = st.columns([1.2, 1.2, 1.2, 2])
    with b1:
        st.button("Start assessment", on_click=nav_to, args=("Predict",), key="cta_home_1", use_container_width=True)
    with b2:
        st.button("How it works", on_click=nav_to, args=("How it Works",), key="cta_home_2", use_container_width=True)
    with b3:
        st.button("Help centre", on_click=nav_to, args=("Help",), key="cta_home_3", use_container_width=True)


# ---------------------------------------------------------------------------
# Predict
# ---------------------------------------------------------------------------

def _validate_clinical(age, t_stage, n_stage, m_stage):
    errs, warns = [], []
    if age is None or age <= 0:
        errs.append("Age must be greater than 0.")
    elif age < 18:
        warns.append("Age is below 18. This model was trained on adult data.")
    elif age > 100:
        warns.append("Age above 100 is outside the typical training range.")
    if t_stage is None or t_stage < 0 or t_stage > 4:
        errs.append("T-stage must be between 0 and 4.")
    if n_stage is None or n_stage < 0 or n_stage > 3:
        errs.append("N-stage must be between 0 and 3.")
    if m_stage is None or m_stage < 0 or m_stage > 1:
        errs.append("M-stage must be 0 or 1.")
    return errs, warns


def _validate_files(dicom_files, rt_file, roi_name):
    errs, warns = [], []
    if not dicom_files:
        errs.append("Upload the CT DICOM series (multiple .dcm files).")
    elif len(dicom_files) < 10:
        warns.append(
            f"Only {len(dicom_files)} DICOM file(s) uploaded. A full CT series "
            "usually contains dozens to hundreds of slices."
        )
    if not rt_file:
        errs.append("Upload the RTSTRUCT file (.dcm).")
    else:
        name = rt_file.name.lower()
        if not (name.endswith(".dcm") or name.endswith(".dicom")):
            errs.append("RTSTRUCT file should have a .dcm extension.")
    if not roi_name or not roi_name.strip():
        errs.append("ROI name cannot be empty (default is GTV-1).")
    return errs, warns


def page_predict():
    page_hero(
        "Risk Prediction",
        "Upload a CT DICOM series and RTSTRUCT contour, add clinical details, get a risk score.",
        PREDICT_HERO,
    )

    st.markdown(
        """
        <div class="info-banner">
        <strong>Before you start:</strong> Lunexa runs deep-learning inference on your CT volume,
        radiomics extraction on the tumor region, and a fusion survival model. On CPU-only servers
        this can take 30 to 90 seconds after upload. Files are processed in a temporary directory
        and removed when your session ends. This is a research prototype, not clinical advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick "what you'll get" tiles
    q1, q2, q3, q4 = st.columns(4)
    q1.markdown('<div class="info-card"><h4>Risk score</h4><p>Relative hazard number produced by the fusion model.</p></div>', unsafe_allow_html=True)
    q2.markdown('<div class="info-card"><h4>Risk band</h4><p>Lower, moderate, or higher for a quick visual summary.</p></div>', unsafe_allow_html=True)
    q3.markdown('<div class="info-card"><h4>Median survival</h4><p>Estimated time to 50% survival using the baseline hazard.</p></div>', unsafe_allow_html=True)
    q4.markdown('<div class="info-card"><h4>1y / 2y survival</h4><p>Fixed-time survival probabilities from the same curve.</p></div>', unsafe_allow_html=True)

    try:
        from inference import (
            get_config,
            generate_previews,
            run_prediction,
            save_uploaded_dicoms,
        )
        cfg = get_config()
    except Exception as e:
        st.error(f"Could not load the inference module or model files. Details: {e}")
        st.info(
            "Ensure fusion_model_final_v2.pt, scalers_final_v2.pkl, "
            "model_config_final_v2.json, and baseline_hazard.json sit next to app.py."
        )
        return

    st.caption(f"Loaded model · Test C-index: **{cfg['test_cindex']:.4f}**")

    # --- Section 1: DICOM upload ---
    st.markdown('<p class="sect-title">1. CT scan (DICOM series)</p>', unsafe_allow_html=True)
    st.write(
        "Select **all** `.dcm` files from a single CT series. If you have a folder, open it and "
        "pick every file inside. Do not mix files from different scans or patients."
    )
    dicom_files = st.file_uploader(
        "DICOM files",
        type=["dcm", "dicom"],
        accept_multiple_files=True,
        key="dicom_upload",
        help="A CT series is one 3D scan stored as many 2D slice files. All slices are needed.",
    )
    if dicom_files:
        st.caption(f"✓ {len(dicom_files)} file(s) selected.")

    # --- Section 2: RTSTRUCT ---
    st.markdown('<p class="sect-title">2. Tumor mask (RTSTRUCT)</p>', unsafe_allow_html=True)
    st.write(
        "An RTSTRUCT file stores tumor outlines drawn by a clinician. It links to the same CT "
        "series above through DICOM IDs, so both files must come from the same study."
    )
    rt_file = st.file_uploader(
        "RTSTRUCT file",
        type=["dcm", "dicom"],
        accept_multiple_files=False,
        key="rt_upload",
        help="A single .dcm file containing the RTSTRUCT (radiotherapy structure) contours.",
    )
    roi_name = st.text_input(
        "ROI name",
        value="GTV-1",
        help="The structure name to use as the tumor mask. GTV-1 is the standard default in the training data.",
    )

    # --- Section 3: Clinical ---
    st.markdown('<p class="sect-title">3. Clinical details</p>', unsafe_allow_html=True)
    st.write(
        "These variables come from the patient's clinical record. If any are unknown, use the "
        "closest documented value rather than guessing wildly, since bad inputs distort the risk."
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age = st.number_input(
            "Age (years)", min_value=0.0, max_value=120.0, value=65.0, step=1.0,
            help="Patient age in years at the time of the scan.",
        )
    with c2:
        t_stage = st.number_input(
            "T-Stage (0–4)", min_value=0.0, max_value=4.0, value=1.0, step=1.0,
            help="Primary tumor size and local extent. 0 = no evidence, 4 = invades nearby structures.",
        )
    with c3:
        n_stage = st.number_input(
            "N-Stage (0–3)", min_value=0.0, max_value=3.0, value=0.0, step=1.0,
            help="Regional lymph node involvement. 0 = none, 3 = distant or contralateral nodes.",
        )
    with c4:
        m_stage = st.number_input(
            "M-Stage (0–1)", min_value=0.0, max_value=1.0, value=0.0, step=1.0,
            help="Distant metastasis. 0 = none detected, 1 = distant spread present.",
        )

    c5, c6, c7 = st.columns(3)
    with c5:
        overall = st.selectbox(
            "Overall Stage", cfg["stage_options"],
            help="Combined TNM stage grouping. Matches the categories used during model training.",
        )
    with c6:
        histology = st.selectbox(
            "Histology", cfg["histology_options"],
            help="Tumor cell type from biopsy. NOS = not otherwise specified.",
        )
    with c7:
        gender = st.selectbox("Gender", ["male", "female"])

    # --- Validation ---
    clin_errs, clin_warns = _validate_clinical(age, t_stage, n_stage, m_stage)
    file_errs, file_warns = _validate_files(dicom_files, rt_file, roi_name)

    if m_stage == 0 and overall and str(overall).lower() in {"iv", "4"}:
        clin_warns.append("Overall stage IV but M-stage is 0. Please double-check.")
    if int(t_stage) == 0 and int(n_stage) == 0 and int(m_stage) == 0:
        clin_warns.append("T=0, N=0, M=0 is unusual for a diagnosed tumor. Please verify.")

    all_errs = file_errs + clin_errs
    all_warns = file_warns + clin_warns

    st.markdown('<p class="sect-title">Validation</p>', unsafe_allow_html=True)
    if not all_errs and not all_warns:
        st.markdown('<div class="v-ok">All checks passed. Ready to predict.</div>', unsafe_allow_html=True)
    else:
        for e in all_errs:
            st.markdown(f'<div class="v-err">❌ {e}</div>', unsafe_allow_html=True)
        for w in all_warns:
            st.markdown(f'<div class="v-warn">⚠️ {w}</div>', unsafe_allow_html=True)

    can_run = len(all_errs) == 0
    col_a, col_b = st.columns(2)
    do_preview = col_a.button("Load preview images", use_container_width=True, disabled=not can_run)
    do_predict = col_b.button("Predict risk score", use_container_width=True, disabled=not can_run, key="predict_btn")

    if not (do_preview or do_predict):
        return

    tmp_root = Path(tempfile.mkdtemp(prefix="lunexa_"))
    series_dir = tmp_root / "dicom"
    series_dir.mkdir(parents=True, exist_ok=True)
    save_uploaded_dicoms(dicom_files, series_dir)
    rt_path = tmp_root / Path(rt_file.name).name
    with open(rt_path, "wb") as f:
        f.write(rt_file.getbuffer())

    if do_preview:
        with st.spinner("Building preview slices..."):
            try:
                imgs = generate_previews(str(series_dir), str(rt_path), roi_name)
                st.markdown('<p class="sect-title">Preview</p>', unsafe_allow_html=True)
                p1, p2, p3 = st.columns(3)
                p1.image(imgs["full"], caption="Full CT slice")
                p2.image(imgs["overlay"], caption="Tumor contour")
                p3.image(imgs["cropped"], caption="Cropped region")
            except Exception as e:
                st.error(f"Preview failed: {e}")

    if do_predict:
        with st.spinner("Extracting features and predicting... this may take up to a minute."):
            try:
                result = run_prediction(
                    str(series_dir), str(rt_path), roi_name,
                    age, t_stage, n_stage, m_stage,
                    overall, histology, gender,
                )
                risk = result["risk_score"]
                frac = 1 / (1 + math.exp(-risk))
                if frac < 0.4:
                    band, cls = "Lower relative risk", "risk-low"
                elif frac < 0.65:
                    band, cls = "Moderate relative risk", "risk-mod"
                else:
                    band, cls = "Higher relative risk", "risk-high"

                st.markdown('<p class="sect-title">Prediction result</p>', unsafe_allow_html=True)
                st.markdown('<div class="result-panel">', unsafe_allow_html=True)
                st.markdown(f'<p class="{cls}">Risk score: {risk:.4f} · {band}</p>', unsafe_allow_html=True)
                st.progress(min(max(frac, 0.0), 1.0))

                med = result["median_survival_days"]
                if med is not None:
                    st.write(f"**Estimated median survival:** {med:.0f} days (~{med / 30.4:.1f} months)")
                else:
                    st.write("**Estimated median survival:** beyond the model's follow-up horizon (a favorable relative outlook).")
                m1, m2 = st.columns(2)
                m1.metric("1-year survival probability", f"{result['prob_1yr'] * 100:.1f}%")
                m2.metric("2-year survival probability", f"{result['prob_2yr'] * 100:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)

                # Inline interpretation
                st.markdown(
                    """
                    <div class="info-card" style="margin-top:14px">
                    <h4>How to read this result</h4>
                    <ul>
                        <li><strong>Risk score</strong> is a relative number, not an absolute probability of death. Higher values mean higher predicted hazard within the training cohort.</li>
                        <li><strong>Risk band</strong> (lower / moderate / higher) comes from a sigmoid of the score and is only a visual guide.</li>
                        <li><strong>Median survival</strong> and <strong>1- / 2-year probabilities</strong> combine the score with a baseline hazard curve fitted on training data.</li>
                        <li>Two cases with similar scores can still have very different outcomes because of factors not captured by this model.</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Downloadable JSON report
                report = {
                    "generated_at": datetime.now().isoformat(timespec="seconds"),
                    "inputs": {
                        "age": age, "t_stage": t_stage, "n_stage": n_stage,
                        "m_stage": m_stage, "overall_stage": overall,
                        "histology": histology, "gender": gender, "roi": roi_name,
                    },
                    "outputs": {
                        "risk_score": round(risk, 4),
                        "risk_band": band,
                        "sigmoid_fraction": round(frac, 4),
                        "median_survival_days": med,
                        "prob_1yr": round(result["prob_1yr"], 4),
                        "prob_2yr": round(result["prob_2yr"], 4),
                    },
                    "model": {"test_cindex": result["test_cindex"]},
                    "disclaimer": "Research prototype. Not clinical advice.",
                }
                st.download_button(
                    "Download result (JSON)",
                    data=json.dumps(report, indent=2),
                    file_name=f"lunexa_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                )

                with st.expander("Detailed breakdown"):
                    st.json(report)

                st.caption(
                    "Scores are relative within the training cohort. "
                    "Research prototype only, not clinical advice."
                )
            except Exception as e:
                st.error(f"Prediction failed: {e}")


# ---------------------------------------------------------------------------
# Symptoms
# ---------------------------------------------------------------------------

def page_symptoms():
    page_hero(
        "Symptoms and Guidance",
        "Educational information only. Please see a clinician for personal medical advice.",
        SYMPTOM_HERO,
    )

    st.markdown('<p class="sect-title">Common symptoms</p>', unsafe_allow_html=True)
    rows = [SYMPTOM_CARDS[i : i + 3] for i in range(0, len(SYMPTOM_CARDS), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, card in zip(cols, row):
            with col:
                st.markdown(
                    f"""
                    <div class="symptom-card">
                        <img src="{card['img']}" alt="{card['title']}"/>
                        <div class="body">
                            <h4>{card['title']}</h4>
                            <p>{card['desc']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<p class="sect-title">How to reduce risk and seek help</p>', unsafe_allow_html=True)
    tips = [
        ("Quit smoking", "Stopping tobacco use and avoiding second-hand smoke is the single largest modifiable risk factor."),
        ("Act early", "Seek care for lasting cough, chest pain, or coughing up blood without delay."),
        ("Consider screening", "Long-term smokers or former smokers aged 50+ may benefit from low-dose CT screening."),
        ("Stay active", "Regular activity, good nutrition, and routine check-ups support long-term lung health."),
        ("Know your exposures", "Family history and occupational exposures like asbestos, radon, and diesel matter."),
        ("Ask about symptoms", "Use the Help page to learn terms such as DICOM, RTSTRUCT, and staging."),
    ]
    tcols = st.columns(3)
    for i, (t, d) in enumerate(tips):
        with tcols[i % 3]:
            st.markdown(f'<div class="info-card" style="margin-bottom:14px"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Educational videos</p>', unsafe_allow_html=True)
    videos = [
        ("Understand lung cancer", "hKV0f_h-f6w"),
        ("Warning signs to discuss with a doctor", "GwVz0HyMyds"),
        ("Symptoms explained", "gIbmqYEf2ag"),
        ("Living with lung cancer", "XIemxRJRuuQ"),
    ]
    vcols = st.columns(2)
    for i, (title, vid) in enumerate(videos):
        with vcols[i % 2]:
            st.markdown(f"**{title}**")
            st.video(f"https://www.youtube.com/watch?v={vid}")

    st.error(
        "**When to get urgent care:** sudden severe shortness of breath, coughing up "
        "large amounts of blood, chest pain with dizziness, or new confusion."
    )


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

def page_help():
    page_hero(
        "Help Centre",
        "Plain-language guides for lung cancer, DICOM, RTSTRUCT, staging, and how to read Lunexa.",
        HELP_HERO,
    )

    st.markdown('<p class="sect-title">Quick topics</p>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    q1.markdown('<div class="info-card"><h4>New to CT scans?</h4><p>Start with what a CT is, what DICOM means, and how to spot a valid series.</p></div>', unsafe_allow_html=True)
    q2.markdown('<div class="info-card"><h4>Not sure about staging?</h4><p>Understand T, N, M, overall stage, and how they relate to prognosis.</p></div>', unsafe_allow_html=True)
    q3.markdown('<div class="info-card"><h4>Confused by the result?</h4><p>Learn what the risk score, band, and survival probabilities really mean.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Lung cancer basics</p>', unsafe_allow_html=True)
    with st.expander("What is lung cancer?", expanded=True):
        st.write(
            "Lung cancer is a group of diseases in which cells in the lung grow uncontrollably. "
            "The two broad categories are non-small-cell lung cancer (NSCLC), which accounts for "
            "roughly 85% of cases, and small-cell lung cancer (SCLC). NSCLC itself includes "
            "adenocarcinoma, squamous cell carcinoma, and large cell carcinoma, each with "
            "different treatment implications. Lunexa was trained on an NSCLC cohort."
        )
    with st.expander("What are the main risk factors?"):
        st.write(
            "Smoking is the single largest risk factor. Second-hand smoke, radon gas, asbestos, "
            "diesel exhaust, air pollution, family history, previous chest radiation, and certain "
            "occupational exposures also raise risk. Never-smokers can still develop lung cancer, "
            "particularly adenocarcinoma."
        )
    with st.expander("How is lung cancer diagnosed?"):
        st.write(
            "Diagnosis usually starts with a chest X-ray or CT scan, followed by a biopsy to "
            "confirm the cancer type. Additional imaging such as PET-CT and MRI helps determine "
            "how far the cancer has spread. Staging combines tumor size, node involvement, and "
            "any distant metastasis into the TNM system used across the Predict page."
        )
    with st.expander("What treatments are available?"):
        st.write(
            "Treatment depends on stage and cell type. Options include surgery, radiotherapy, "
            "chemotherapy, targeted therapy for specific mutations (EGFR, ALK, KRAS, ROS1), and "
            "immunotherapy. Early-stage disease is often treated with surgery, advanced disease "
            "with combinations of systemic therapy. Multidisciplinary teams decide the plan."
        )

    st.markdown('<p class="sect-title">Imaging and file formats</p>', unsafe_allow_html=True)
    with st.expander("What is a CT scan?"):
        st.write(
            "A CT (Computed Tomography) scan uses X-rays to produce detailed cross-sectional "
            "images of the body. Lunexa uses the full 3D CT volume as one of its imaging inputs."
        )
    with st.expander("What is DICOM and what is a DICOM series?"):
        st.write(
            "DICOM is the standard file format for medical images. A CT scan is stored as many "
            "2D slice files, and the full set of slice files for one scan is called a DICOM "
            "series. For Predict, you need every slice from a single series. Do not mix files "
            "from different scans or different patients."
        )
    with st.expander("How do I know if my DICOM files are valid?"):
        st.write(
            "A valid series usually has dozens to hundreds of files, all with the .dcm extension, "
            "and all sharing the same Study and Series identifiers. Chrome's folder picker is the "
            "easiest way to select every file at once. If Lunexa warns that too few files are "
            "uploaded, you likely selected only part of the series."
        )
    with st.expander("What is RTSTRUCT, GTV-1, ROI, or a tumor mask?"):
        st.markdown(
            """
- **RTSTRUCT**: a DICOM file that stores structures a clinician has outlined on the CT.
- **Contour**: the outline drawn around the tumor on individual slices.
- **GTV-1**: the Gross Tumor Volume label used by default in this dataset.
- **ROI**: Region of Interest, the structure name you type in (for example GTV-1).
- **Tumor mask**: a 3D binary volume where 1 marks tumor voxels and 0 marks background.
            """
        )
    with st.expander("I don't have an RTSTRUCT. Can I still use Lunexa?"):
        st.write(
            "Not yet. The current pipeline needs a clinician-drawn RTSTRUCT so radiomics can be "
            "extracted from the exact tumor region. A future version could integrate automated "
            "segmentation, but that would add its own uncertainty into the pipeline."
        )

    st.markdown('<p class="sect-title">Staging and clinical inputs</p>', unsafe_allow_html=True)
    with st.expander("What do T, N, M, and Overall Stage mean?"):
        st.markdown(
            """
- **T-stage**: size and local extent of the primary tumor (0 to 4).
- **N-stage**: regional lymph-node involvement (0 to 3).
- **M-stage**: distant metastasis (M0 = none, M1 = present).
- **Overall stage** in this app: I, II, IIIa, IIIb, matching the training data categories.

TNM values are grouped into the overall stage. Two patients with different T and N can end up in the same overall stage.
            """
        )
    with st.expander("What is histology and why does it matter?"):
        st.write(
            "Histology is the tumor cell type as identified under a microscope after biopsy. "
            "Adenocarcinoma, squamous cell carcinoma, and large cell carcinoma respond differently "
            "to treatment, and prognosis varies between them. NOS means not otherwise specified, "
            "used when the biopsy could not classify the cell type precisely."
        )
    with st.expander("What if some clinical fields are unknown?"):
        st.write(
            "Use the closest documented value from the clinical record. Guessing wildly, for "
            "example putting stage IV when the true stage is unknown, can distort the prediction "
            "more than a missing value would. In future versions Lunexa could accept explicit "
            "missing-data indicators."
        )

    st.markdown('<p class="sect-title">Reading the prediction</p>', unsafe_allow_html=True)
    with st.expander("What does the risk score mean?"):
        st.write(
            "The risk score is a relative number learned from the training cohort. Higher values "
            "mean higher predicted hazard compared to other patients seen during training. It is "
            "not a probability of death, and comparing scores between very different populations "
            "is not meaningful."
        )
    with st.expander("How reliable is the model?"):
        st.write(
            "Lunexa achieved a validation C-index around 0.665 and a test C-index around 0.598. "
            "A C-index of 0.5 is random ranking and 1.0 is perfect. So the model ranks correctly "
            "somewhat better than chance, which is typical for imaging survival models on this "
            "task. It is far from a replacement for clinical judgment."
        )
    with st.expander("Why do two similar patients get different scores?"):
        st.write(
            "The CT deep-feature branch responds to subtle image texture and shape cues, so two "
            "cases with the same TNM can look different to the model based on imaging alone. "
            "This is a feature, not a bug: multimodal fusion is designed to pick up signal the "
            "clinical fields alone would miss. It also means small changes can shift the score."
        )
    with st.expander("Can I trust this in real clinical decisions?"):
        st.write(
            "No. Lunexa is a research prototype, not a certified medical device. It was trained "
            "on a limited public dataset and has not been validated on your local patient "
            "population. Never use it as a stand-alone decision tool. Always follow "
            "guideline-based care and your clinical team's advice."
        )

    st.markdown('<p class="sect-title">Troubleshooting</p>', unsafe_allow_html=True)
    with st.expander("The Predict page says my ROI was not found."):
        st.write(
            "The ROI name in the text box must match a structure inside the RTSTRUCT exactly, "
            "including case. Try the default GTV-1, and if that fails, open the RTSTRUCT in a "
            "DICOM viewer to see the list of available structure names."
        )
    with st.expander("Prediction is very slow."):
        st.write(
            "On CPU-only servers the deep CT branch and radiomics extraction can take up to a "
            "minute per case. The first prediction after the app starts is slowest because "
            "PyTorch and MedicalNet need to warm up. Repeat runs are faster."
        )
    with st.expander("The app crashed or the model failed to load."):
        st.write(
            "Check the terminal or Streamlit Cloud logs for the exact error. On the free "
            "Streamlit tier, memory limits can cause torch and monai to be killed during "
            "loading. If that happens, deploy the app on a container with more RAM, such as a "
            "Hugging Face Docker Space."
        )
    with st.expander("Preview looks blank or the tumor isn't visible."):
        st.write(
            "The preview picks the slice with the largest tumor area from the mask. If nothing "
            "shows, the ROI probably has zero voxels, meaning the ROI name didn't match anything "
            "in the RTSTRUCT. Double-check the ROI name against the structures in the file."
        )

    st.info(
        "Still stuck? Note the exact error message, the page you were on, and what you were "
        "trying to do, then contact the project owner. Screenshots help a lot."
    )


# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------

def page_how():
    page_hero(
        "How Lunexa Works",
        "A five-step pipeline from raw DICOM to a survival risk estimate.",
        HOW_HERO,
    )
    steps = [
        ("Upload DICOM and RTSTRUCT",
         "The RTSTRUCT is aligned to the CT series and the named ROI (for example GTV-1) becomes a 3D tumor mask."),
        ("Deep CT embedding",
         "A MedicalNet ResNet-10, pretrained on medical volumes, produces a 512-dimensional embedding of the CT."),
        ("Radiomics feature extraction",
         "PyRadiomics computes shape, first-order, and texture features. Sixteen selected descriptors are kept and scaled."),
        ("Clinical encoding",
         "Age, T/N/M stages, overall stage, histology, and gender are encoded and scaled to match training."),
        ("Fusion and survival estimate",
         "A DeepSurv-style head fuses the three streams into a risk score, and a baseline hazard turns it into survival probabilities."),
    ]
    for i, (title, body) in enumerate(steps, 1):
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-num">{i}</div>
                <div>
                    <h4>{title}</h4>
                    <p>{body}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def page_about():
    page_hero(
        "About Lunexa",
        "A multimodal research tool for lung cancer survival risk assessment.",
        ABOUT_HERO,
    )

    lcol, rcol = st.columns([1, 2.2])
    with lcol:
        st.markdown('<div class="about-logo">🫁</div>', unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center'>"
            "<div style='font-size:1.55rem;font-weight:800;color:#0F766E'>Lunexa</div>"
            "<div style='color:#64748B'>Lung Cancer Prognosis</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with rcol:
        st.write(
            "Lunexa is a multimodal research prototype for estimating relative survival risk "
            "in lung cancer. It combines three information sources that clinicians already use "
            "in complementary ways: imaging appearance on CT, quantitative tumor descriptors "
            "(radiomics), and structured clinical variables such as stage and histology."
        )
        st.write(
            "The goal is educational and exploratory. Lunexa is designed to show how modern "
            "fusion models can surface a transparent risk score and fixed-time survival "
            "probabilities. It is **not** a certified medical device and must never replace "
            "qualified clinical judgment, pathology, or guideline-based care."
        )
        m1, m2 = st.columns(2)
        m1.metric("Validation C-index", "0.665")
        m2.metric("Test C-index", "0.598")

    st.markdown('<p class="sect-title">What problem does Lunexa address?</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
        <p>
        Lung cancer prognosis depends on more than a single number. Tumor size and location,
        texture on CT, nodal status, distant spread, cell type, and patient factors all matter.
        Many research models use only one of these streams. Lunexa was built to practice
        <strong>multimodal fusion</strong>: learning a joint representation so that imaging and
        clinical signals can inform one coherent risk estimate.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="sect-title">Model overview</p>', unsafe_allow_html=True)
    ov1, ov2, ov3 = st.columns(3)
    ov1.markdown('<div class="info-card"><h4>CT branch</h4><p>MedicalNet ResNet-10 embeddings of the full DICOM volume, projected into a compact hidden layer before fusion.</p></div>', unsafe_allow_html=True)
    ov2.markdown('<div class="info-card"><h4>Radiomics branch</h4><p>Sixteen PyRadiomics features from the RTSTRUCT-defined tumor, scaled to match training statistics.</p></div>', unsafe_allow_html=True)
    ov3.markdown('<div class="info-card"><h4>Fusion head</h4><p>Concatenated features feed a DeepSurv-style head that outputs a scalar relative risk score.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">How to interpret outputs</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
        <ul>
          <li><strong>Risk score</strong> is relative within the training cohort, not an absolute probability of death.</li>
          <li><strong>Risk band</strong> (lower / moderate / higher) is a simple visual guide based on a sigmoid of the score.</li>
          <li><strong>Median survival</strong> and <strong>1- / 2-year probabilities</strong> come from combining the risk score with a baseline hazard curve.</li>
          <li><strong>C-index</strong> values summarize ranking quality on validation and held-out test data during model development.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="sect-title">Intended audience</p>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    a1.markdown('<div class="info-card"><h4>Students</h4><p>Learn how multimodal survival models connect DICOM, radiomics, and clinical tables.</p></div>', unsafe_allow_html=True)
    a2.markdown('<div class="info-card"><h4>Researchers</h4><p>Prototype workflows that need CT series + RTSTRUCT + structured clinical fields.</p></div>', unsafe_allow_html=True)
    a3.markdown('<div class="info-card"><h4>Educators</h4><p>Demonstrate transparent risk outputs without presenting them as bedside advice.</p></div>', unsafe_allow_html=True)

    st.warning(
        "**Disclaimer:** Lunexa is a research prototype. It is not a certified medical device "
        "and must not be used alone for clinical decisions. Always rely on qualified professionals "
        "and standard care pathways."
    )
    st.caption("Group 7 · Multimodal Cancer Prognosis · University research project")


# ---------------------------------------------------------------------------
# Router + footer
# ---------------------------------------------------------------------------
if page == "Home":
    page_home()
elif page == "Predict":
    page_predict()
elif page == "Symptoms":
    page_symptoms()
elif page == "Help":
    page_help()
elif page == "How it Works":
    page_how()
else:
    page_about()

st.markdown(
    """
    <div class="footer-bar">
      <strong>Lunexa</strong> · Lung Cancer Prognosis and Risk Assessment<br/>
      Home · Predict · Symptoms · Help · How it Works · About
    </div>
    """,
    unsafe_allow_html=True,
)