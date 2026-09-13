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
        "url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=80",
        "title": "Precision Imaging Meets AI",
        "subtitle": "CT-driven multimodal risk assessment for lung cancer prognosis.",
    },
    {
        "url": "https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&w=1600&q=80",
        "title": "From Scan to Survival Insight",
        "subtitle": "Deep CT features, radiomics, and clinical data in one pipeline.",
    },
    {
        "url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1600&q=80",
        "title": "Built for Research Teams",
        "subtitle": "Transparent risk scores with 1- and 2-year survival estimates.",
    },
    {
        "url": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?auto=format&fit=crop&w=1600&q=80",
        "title": "Support, Not Replace, Clinical Care",
        "subtitle": "A research tool designed to assist education and exploration.",
    },
]

SYMPTOM_CARDS = [
    {"title": "Persistent cough", "desc": "A cough that does not go away or gets worse over weeks. May produce blood-tinged sputum.", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNuAHaCwTH5tqXDpJebnBOI_YVnnonG0JvioJ4PM93Sg&s=10"},
    {"title": "Shortness of breath", "desc": "Feeling breathless during routine activities or at rest can signal airway or lung involvement.", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtQ1i9R24TSK2dlkOptzC79LiJs9-kN0zKSt6V6-4lHw&s=10"},
    {"title": "Chest pain", "desc": "Pain that worsens with deep breathing, coughing, or laughing. Often related to the chest wall or pleura.", "img": "https://cadenceheart.sg/wp-content/uploads/2022/01/shutterstock_1895012779-1024x576.jpg"},
    {"title": "Hoarseness and wheezing", "desc": "Voice changes or new wheezing may occur if a tumor affects the larynx or large airways.", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbP5qG0W_damO_sK1LFxy0UHRr4AxLfayvDEPZDu1wMg&s=10"},
    {"title": "Unexplained weight loss", "desc": "Losing weight without trying, fatigue, and loss of appetite are common systemic signs.", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa_-Xl03se48IrYq8_bsg_aGwzGiwrNluyvKvfTezjRgVsc_DRvILAaCje&s=10"},
    {"title": "Recurrent infections", "desc": "Repeated bronchitis or pneumonia in the same area of the lung can be a warning sign.", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfmtu8yRUjW9ig2juIdDSnhN-gLDB3MzMBCn5xhSlDPR5909W3Ivn0HdlD&s=10"},
]

SYMPTOM_HERO = "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1600&q=80"
HELP_HERO    = "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=80"
ABOUT_HERO   = "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?auto=format&fit=crop&w=1600&q=80"
HOW_HERO     = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&q=80"
PREDICT_HERO = "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=1600&q=80"

# ---------------------------------------------------------------------------
# CSS  – light mode forced, no dark-mode bleed, triangles removed
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Force light mode ── */
html, body, [data-testid="stAppViewContainer"], .stApp {
    color-scheme: light !important;
    background-color: #F0F8FF !important;
    color: #0F172A !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 1100px 420px at 8% -5%, rgba(20,184,166,0.13), transparent 58%),
        radial-gradient(ellipse 800px 400px at 105% 5%, rgba(37,99,235,0.07), transparent 58%),
        linear-gradient(180deg, #E8F6FC 0%, #F5F9FC 50%, #EEF7F5 100%) !important;
}

/* ── Chrome ── */
#MainMenu {visibility:hidden;}
footer    {visibility:hidden;}
header    {visibility:hidden;}
[data-testid="stSidebar"]        {display:none;}
[data-testid="collapsedControl"] {display:none;}

/* ── Layout ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2.5rem;
    max-width: 1340px;
}

/* ── Navbar shell – sits at very top, full width ── */
.nav-shell {
    background: #ffffff;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    border-radius: 0;
    padding: 10px 24px;
    margin: 0 -3rem 18px -3rem;   /* bleed past block-container padding */
    box-shadow: 0 2px 12px rgba(15,118,110,0.07);
    display: flex;
    align-items: center;
}

/* ── Brand ── */
.brand-row { display:flex; align-items:center; gap:12px; }
.brand-logo {
    width:42px; height:42px;
    background: linear-gradient(135deg,#0F766E,#14B8A6);
    border-radius:11px;
    display:flex; align-items:center; justify-content:center;
    color:white; font-size:21px;
    box-shadow: 0 4px 12px rgba(15,118,110,0.32);
    flex-shrink:0;
}
.brand-text-title { font-size:1.25rem; font-weight:800; color:#0F766E; margin:0; line-height:1.1; }
.brand-text-tag   { font-size:0.7rem;  color:#64748B; margin:0; white-space:nowrap; }

/* ── Remove triangles from option_menu items ── */
[data-testid="stHorizontalBlock"] nav ul li a::before,
[data-testid="stHorizontalBlock"] nav ul li a .icon,
nav ul li a svg,
.nav-link .icon { display:none !important; }

/* Keep nav items on one line */
nav ul { flex-wrap:nowrap !important; }
nav ul li a { white-space:nowrap !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg,#0F766E,#14B8A6) !important;
    color: white !important;
    border: none !important;
    padding: 9px 18px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 12px rgba(15,118,110,0.22);
    transition: box-shadow .15s;
}
.stButton > button:hover  { box-shadow: 0 7px 18px rgba(15,118,110,0.32) !important; }
.stButton > button:disabled {
    background: #CBD5E1 !important; box-shadow:none !important; color:#94A3B8 !important;
}
.stDownloadButton > button {
    background: white !important; color:#0F766E !important;
    border: 1.5px solid #0F766E !important; border-radius:10px !important;
    padding: 9px 18px !important; font-weight:600 !important; box-shadow:none !important;
}
.stDownloadButton > button:hover { background:#E6F2F0 !important; }

/* ── Slideshow ── */
.slideshow {
    position:relative; width:100%; height:420px;
    overflow:hidden; border-radius:20px;
    box-shadow: 0 10px 30px rgba(15,118,110,0.14);
    margin-bottom:20px;
}
.slideshow .slide {
    position:absolute; inset:0; opacity:0;
    animation: lunFade 24s infinite;
    background-size:cover; background-position:center;
}
.slideshow .slide:nth-child(1){animation-delay:0s;}
.slideshow .slide:nth-child(2){animation-delay:6s;}
.slideshow .slide:nth-child(3){animation-delay:12s;}
.slideshow .slide:nth-child(4){animation-delay:18s;}
@keyframes lunFade {
    0%  {opacity:0;}
    5%  {opacity:1;}
    25% {opacity:1;}
    30% {opacity:0;}
    100%{opacity:0;}
}
.slide-overlay {
    position:absolute; inset:0;
    background: linear-gradient(160deg,rgba(15,118,110,0.82) 0%,rgba(37,99,235,0.38) 55%,rgba(15,23,42,0.28) 100%);
    display:flex; flex-direction:column; justify-content:flex-end;
    padding:32px 40px; color:white;
}
.slide-badge {
    display:inline-block;
    background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.35);
    color:white; padding:4px 12px; border-radius:999px;
    font-size:0.74rem; letter-spacing:.05em; text-transform:uppercase; margin-bottom:10px;
}
/* Each slide has its own text overlay */
.slide-text { display:none; position:absolute; inset:0; flex-direction:column; justify-content:flex-end; padding:32px 40px; color:white; }
.slide-text h2 { color:white; font-size:1.9rem; font-weight:800; margin:0 0 6px 0; text-shadow:0 2px 10px rgba(0,0,0,0.28); }
.slide-text p  { color:rgba(255,255,255,0.92); font-size:1rem; margin:0; max-width:580px; }

/* ── Cards ── */
.info-card {
    background:white; border-radius:14px; padding:20px;
    border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(15,23,42,0.04);
    height:100%; box-sizing:border-box;
}
.info-card h4 { color:#0F766E; margin:0 0 7px 0; font-size:1rem; }
.info-card p  { color:#475569; margin:0; font-size:0.93rem; line-height:1.55; }
.info-card ul { color:#475569; margin:0; padding-left:1rem; line-height:1.7; font-size:0.93rem; }
.info-card li { margin-bottom:3px; }

/* ── Page hero banners ── */
.page-hero {
    position:relative; border-radius:18px; overflow:hidden;
    height:180px; margin-bottom:20px;
    box-shadow:0 5px 18px rgba(15,118,110,0.12);
}
.page-hero .bg  { position:absolute; inset:0; background-size:cover; background-position:center; }
.page-hero .tint{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(15,118,110,0.86),rgba(37,99,235,0.38)); }
.page-hero .content {
    position:relative; z-index:2; height:100%;
    display:flex; flex-direction:column; justify-content:center;
    padding:0 30px; color:white;
}
.page-hero h1 { color:white; font-size:1.85rem; margin:0; }
.page-hero p  { color:rgba(255,255,255,0.9); margin:5px 0 0 0; font-size:0.97rem; }

/* ── Risk colours ── */
.risk-low  {color:#16A34A; font-weight:700; font-size:1.3rem;}
.risk-mod  {color:#F59E0B; font-weight:700; font-size:1.3rem;}
.risk-high {color:#DC2626; font-weight:700; font-size:1.3rem;}

/* ── Metrics ── */
div[data-testid="stMetric"] {
    background:white; padding:14px 16px; border-radius:12px;
    border:1px solid #E2E8F0; box-shadow:0 2px 6px rgba(15,23,42,0.04);
}

/* ── Validation banners ── */
.v-err  {background:#FEF2F2; border-left:4px solid #DC2626; padding:9px 13px; border-radius:7px; margin:5px 0; color:#7F1D1D; font-size:0.91rem;}
.v-warn {background:#FFFBEB; border-left:4px solid #F59E0B; padding:9px 13px; border-radius:7px; margin:5px 0; color:#78350F; font-size:0.91rem;}
.v-ok   {background:#F0FDF4; border-left:4px solid #16A34A; padding:9px 13px; border-radius:7px; margin:5px 0; color:#14532D; font-size:0.91rem;}

/* ── Section titles ── */
.sect-title { font-size:1.25rem; font-weight:700; color:#0F172A; margin:20px 0 10px 0; }

/* ── About logo ── */
.about-logo {
    width:110px; height:110px; border-radius:26px;
    background:linear-gradient(135deg,#0F766E,#14B8A6);
    display:flex; align-items:center; justify-content:center;
    color:white; font-size:52px;
    box-shadow:0 10px 28px rgba(15,118,110,0.32);
    margin:0 auto 12px auto;
}

/* ── Step cards ── */
.step-card {
    background:white; border-radius:13px; padding:16px;
    border:1px solid #E2E8F0;
    display:flex; gap:13px; align-items:flex-start; margin-bottom:11px;
}
.step-num {
    min-width:40px; height:40px; border-radius:10px;
    background:#E6F2F0; color:#0F766E;
    display:flex; align-items:center; justify-content:center; font-weight:800;
}
.step-card h4 {margin:0 0 3px 0; color:#0F172A;}
.step-card p  {margin:0; color:#475569;}

/* ── Symptom cards ── */
.symptom-card {
    background:white; border-radius:13px; overflow:hidden;
    border:1px solid #E2E8F0; box-shadow:0 2px 7px rgba(15,23,42,0.04);
    margin-bottom:13px;
}
.symptom-card img   {width:100%; height:135px; object-fit:cover; display:block;}
.symptom-card .body {padding:13px 15px;}
.symptom-card h4    {color:#0F766E; margin:0 0 5px 0;}
.symptom-card p     {color:#475569; margin:0; font-size:0.91rem;}

/* ── Result panel ── */
.result-panel {
    background:white; border-radius:14px; padding:20px;
    border:1px solid #E2E8F0; box-shadow:0 4px 14px rgba(15,118,110,0.07);
    margin-top:13px;
}

/* ── Footer ── */
.footer-bar {
    margin-top:2rem; padding:1rem; text-align:center;
    background:white; border:1px solid #E2E8F0; border-radius:14px;
    color:#64748b; font-size:0.88rem;
}
.footer-bar strong {color:#0F766E;}

/* ── Mobile responsive ── */
@media (max-width: 768px) {
    .nav-shell { padding:8px 12px; margin:0 -1rem 14px -1rem; }
    .brand-text-tag { display:none; }
    .slideshow { height:260px; }
    .slide-overlay { padding:18px 18px; }
    .slide-text h2 { font-size:1.3rem; }
    .page-hero { height:130px; }
    .page-hero h1 { font-size:1.35rem; }
    .block-container { padding-left:1rem !important; padding-right:1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Navigation state
# ---------------------------------------------------------------------------
PAGES = ["Home", "Predict", "Symptoms", "Help", "How it Works", "About"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "nav_epoch" not in st.session_state:
    st.session_state.nav_epoch = 0


def nav_to(page: str):
    st.session_state.current_page = page
    st.session_state.nav_epoch += 1


# ---------------------------------------------------------------------------
# Navbar  – white bar flush to top
# ---------------------------------------------------------------------------
st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
h_left, h_mid, h_right = st.columns([1.7, 6.6, 1.5])

with h_left:
    st.markdown("""
        <div class="brand-row">
            <div class="brand-logo">🫁</div>
            <div>
                <p class="brand-text-title">Lunexa</p>
                <p class="brand-text-tag">Lung Cancer Prognosis</p>
            </div>
        </div>""", unsafe_allow_html=True)

with h_mid:
    picked = option_menu(
        menu_title=None,
        options=PAGES,
        icons=["house","activity","clipboard-pulse","question-circle","gear","info-circle"],
        default_index=PAGES.index(st.session_state.current_page),
        orientation="horizontal",
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon":       {"display": "none"},          # hide icons = no triangles
            "nav-link": {
                "font-size": "14px", "text-align": "center",
                "margin": "0 1px", "padding": "9px 13px",
                "color": "#475569", "background-color": "transparent",
                "--hover-color": "#E6F2F0", "border-radius": "9px",
                "white-space": "nowrap",
            },
            "nav-link-selected": {
                "background-color": "#E6F2F0", "color": "#0F766E", "font-weight": "600",
            },
        },
        key=f"main_nav_{st.session_state.nav_epoch}",
    )
    if picked != st.session_state.current_page:
        st.session_state.current_page = picked
        st.rerun()

with h_right:
    st.write("")
    st.button("Start Assessment", on_click=nav_to, args=("Predict",),
              use_container_width=True, key="cta_top")

st.markdown("</div>", unsafe_allow_html=True)
page = st.session_state.current_page


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def render_slideshow():
    """Animated slideshow where every slide shows its own title/subtitle."""
    # Build per-slide text divs with CSS animation-delay matching the image fade
    slides_html = ""
    for i, s in enumerate(SLIDESHOW):
        slides_html += (
            f'<div class="slide" style="background-image:url({s["url"]});'
            f'z-index:{len(SLIDESHOW)-i};"></div>'
        )
    text_layers = ""
    for i, s in enumerate(SLIDESHOW):
        delay = i * 6
        text_layers += f"""
        <div style="position:absolute;inset:0;opacity:0;z-index:{len(SLIDESHOW)+i+1};
            animation:lunFade 24s {delay}s infinite;
            display:flex;flex-direction:column;justify-content:flex-end;
            padding:32px 40px;pointer-events:none;">
            <span style="display:inline-block;background:rgba(255,255,255,0.18);
                border:1px solid rgba(255,255,255,0.35);color:white;padding:4px 12px;
                border-radius:999px;font-size:0.74rem;letter-spacing:.05em;
                text-transform:uppercase;margin-bottom:10px;width:fit-content;">
                Multimodal Deep Survival Model
            </span>
            <h2 style="color:white;font-size:1.9rem;font-weight:800;margin:0 0 6px 0;
                text-shadow:0 2px 10px rgba(0,0,0,0.28);">{s["title"]}</h2>
            <p style="color:rgba(255,255,255,0.92);font-size:1rem;margin:0;max-width:580px;">
                {s["subtitle"]}
            </p>
        </div>"""

    tint = (
        "linear-gradient(160deg,rgba(15,118,110,0.75) 0%,"
        "rgba(37,99,235,0.32) 55%,rgba(15,23,42,0.22) 100%)"
    )
    st.markdown(f"""
    <div class="slideshow">
        {slides_html}
        <div style="position:absolute;inset:0;background:{tint};z-index:10;"></div>
        <div style="position:absolute;inset:0;z-index:20;">{text_layers}</div>
    </div>""", unsafe_allow_html=True)


def page_hero(title, subtitle, image_url):
    st.markdown(f"""
    <div class="page-hero">
        <div class="bg" style="background-image:url({image_url});"></div>
        <div class="tint"></div>
        <div class="content"><h1>{title}</h1><p>{subtitle}</p></div>
    </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def page_home():
    render_slideshow()

    st.markdown(
        "<h2 style='text-align:center;margin:.4rem 0 .3rem 0;'>Welcome to "
        "<span style='color:#0F766E'>Lunexa</span></h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#475569;max-width:700px;margin:0 auto 1rem auto;'>"
        "A research tool for lung cancer prognosis. Upload a CT DICOM series and RTSTRUCT "
        "tumor contour, add clinical details, and explore relative risk and survival estimates."
        "</p>", unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Test C-index", "0.598")
    m2.metric("Validation C-index", "0.665")
    m3.metric("Modalities fused", "3")
    m4.metric("Radiomics features", "16")

    st.markdown('<p class="sect-title">Why multimodal fusion?</p>', unsafe_allow_html=True)
    cards = [
        ("CT deep features", "MedicalNet ResNet-10 encodes the full CT volume into a 512-dim embedding."),
        ("Radiomics",        "Sixteen selected PyRadiomics descriptors of tumor shape, intensity, and texture."),
        ("Clinical context", "Age, TNM, overall stage, histology, and gender feed a dedicated branch."),
        ("Survival output",  "Risk score with median survival and 1-year / 2-year probabilities."),
    ]
    for col, (t, d) in zip(st.columns(4), cards):
        col.markdown(f'<div class="info-card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">What you need to run a prediction</p>', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    n1.markdown('<div class="info-card"><h4>1. CT DICOM series</h4><p>Upload all .dcm slices from one CT series so the 3D volume can be rebuilt correctly.</p></div>', unsafe_allow_html=True)
    n2.markdown('<div class="info-card"><h4>2. RTSTRUCT contour</h4><p>Provide the radiotherapy structure file and ROI name (e.g. GTV-1) for the tumor mask.</p></div>', unsafe_allow_html=True)
    n3.markdown('<div class="info-card"><h4>3. Clinical details</h4><p>Enter age, T/N/M stages, overall stage, histology, and gender to complete the fusion input.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Ready to explore a case?</p>', unsafe_allow_html=True)
    b1, b2, b3, _ = st.columns([1.2, 1.2, 1.2, 2])
    with b1:
        st.button("Start assessment", on_click=nav_to, args=("Predict",),    key="cta_h1", use_container_width=True)
    with b2:
        st.button("How it works",     on_click=nav_to, args=("How it Works",), key="cta_h2", use_container_width=True)
    with b3:
        st.button("Help centre",      on_click=nav_to, args=("Help",),        key="cta_h3", use_container_width=True)


# ---------------------------------------------------------------------------
# Predict
# ---------------------------------------------------------------------------

def _validate_clinical(age, t_stage, n_stage, m_stage):
    errs, warns = [], []
    if age is None or age <= 0:
        errs.append("Age must be greater than 0.")
    elif age < 18:
        warns.append("Age below 18 — model trained on adult data.")
    elif age > 100:
        warns.append("Age above 100 is outside the typical training range.")
    if t_stage < 0 or t_stage > 4:
        errs.append("T-stage must be 0–4.")
    if n_stage < 0 or n_stage > 3:
        errs.append("N-stage must be 0–3.")
    if m_stage < 0 or m_stage > 1:
        errs.append("M-stage must be 0 or 1.")
    return errs, warns


def _validate_files(dicom_files, rt_file, roi_name):
    errs, warns = [], []
    if not dicom_files:
        errs.append("Upload the CT DICOM series (multiple .dcm files).")
    elif len(dicom_files) < 10:
        warns.append(f"Only {len(dicom_files)} file(s) — a full CT series is usually 50–300 slices.")
    if not rt_file:
        errs.append("Upload the RTSTRUCT file (.dcm).")
    else:
        if not rt_file.name.lower().endswith((".dcm", ".dicom")):
            errs.append("RTSTRUCT file should have a .dcm extension.")
    if not roi_name or not roi_name.strip():
        errs.append("ROI name cannot be empty (default is GTV-1).")
    return errs, warns


def page_predict():
    page_hero("Risk Prediction",
              "Upload your CT DICOM series and RTSTRUCT, fill clinical details, then predict.",
              PREDICT_HERO)

    # ── Load inference module ──────────────────────────────────────────────
    try:
        from inference import get_config, generate_previews, run_prediction, save_uploaded_dicoms
        cfg = get_config()
    except Exception as e:
        st.error(f"Could not load inference module or model files. Details: {e}")
        st.info("Ensure fusion_model_final_v2.pt, scalers_final_v2.pkl, "
                "model_config_final_v2.json, and baseline_hazard.json sit next to app.py.")
        return

    st.caption(f"Model loaded · Test C-index **{cfg['test_cindex']:.4f}**")

    # ── Section 1: CT DICOM ────────────────────────────────────────────────
    st.markdown('<p class="sect-title">1 · CT scan (DICOM series)</p>', unsafe_allow_html=True)
    st.markdown(
        "Select **all `.dcm` files** from a single CT series. "
        "Use your browser's folder-upload or multi-select to pick every slice at once.",
        unsafe_allow_html=False,
    )
    dicom_files = st.file_uploader(
        "Upload DICOM files (select entire folder contents)",
        type=["dcm", "dicom"],
        accept_multiple_files=True,
        key="dicom_upload",
        help="Tip: in Chrome you can drag-and-drop a whole folder onto this area.",
    )
    if dicom_files:
        st.success(f"✓ {len(dicom_files)} DICOM file(s) loaded.")

    # ── Section 2: RTSTRUCT ───────────────────────────────────────────────
    st.markdown('<p class="sect-title">2 · Tumor mask (RTSTRUCT)</p>', unsafe_allow_html=True)
    rt_file = st.file_uploader(
        "Upload RTSTRUCT file",
        type=["dcm", "dicom"],
        accept_multiple_files=False,
        key="rt_upload",
        help="Single .dcm containing the radiotherapy structure contours for this CT study.",
    )
    roi_name = st.text_input(
        "ROI / structure name",
        value="GTV-1",
        help="Must match the structure label inside the RTSTRUCT exactly (case-sensitive).",
    )

    # ── Section 3: Clinical ───────────────────────────────────────────────
    st.markdown('<p class="sect-title">3 · Clinical details</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age = st.number_input("Age (years)", 0.0, 120.0, 65.0, 1.0,
                              help="Patient age at time of scan.")
    with c2:
        t_stage = st.number_input("T-Stage (0–4)", 0.0, 4.0, 1.0, 1.0,
                                  help="Primary tumour size / local extent.")
    with c3:
        n_stage = st.number_input("N-Stage (0–3)", 0.0, 3.0, 0.0, 1.0,
                                  help="Regional lymph-node involvement.")
    with c4:
        m_stage = st.number_input("M-Stage (0–1)", 0.0, 1.0, 0.0, 1.0,
                                  help="Distant metastasis (0=none, 1=present).")

    c5, c6, c7 = st.columns(3)
    with c5:
        overall  = st.selectbox("Overall Stage",  cfg["stage_options"],
                                help="Combined TNM grouping matching training categories.")
    with c6:
        histology = st.selectbox("Histology", cfg["histology_options"],
                                 help="Tumour cell type from biopsy. NOS = not otherwise specified.")
    with c7:
        gender = st.selectbox("Gender", ["male", "female"])

    # ── Validation ────────────────────────────────────────────────────────
    clin_errs, clin_warns = _validate_clinical(age, t_stage, n_stage, m_stage)
    file_errs, file_warns = _validate_files(dicom_files, rt_file, roi_name)

    if m_stage == 0 and overall and str(overall).lower() in {"iv", "4"}:
        clin_warns.append("Stage IV but M=0 — please double-check.")
    if int(t_stage) == 0 and int(n_stage) == 0 and int(m_stage) == 0:
        clin_warns.append("T=N=M=0 is unusual for a diagnosed tumour. Please verify.")

    all_errs  = file_errs  + clin_errs
    all_warns = file_warns + clin_warns

    st.markdown('<p class="sect-title">Validation</p>', unsafe_allow_html=True)
    if not all_errs and not all_warns:
        st.markdown('<div class="v-ok">✓ All checks passed — ready to predict.</div>', unsafe_allow_html=True)
    else:
        for e in all_errs:
            st.markdown(f'<div class="v-err">❌ {e}</div>', unsafe_allow_html=True)
        for w in all_warns:
            st.markdown(f'<div class="v-warn">⚠️ {w}</div>', unsafe_allow_html=True)

    can_run = len(all_errs) == 0
    col_a, col_b = st.columns(2)
    do_preview = col_a.button("Load CT preview",    use_container_width=True, disabled=not can_run)
    do_predict = col_b.button("Predict risk score",  use_container_width=True,
                               disabled=not can_run, key="predict_btn")

    if not (do_preview or do_predict):
        return

    # ── Save uploads to temp dir ──────────────────────────────────────────
    tmp_root   = Path(tempfile.mkdtemp(prefix="lunexa_"))
    series_dir = tmp_root / "dicom"
    series_dir.mkdir(parents=True, exist_ok=True)

    with st.spinner("Saving uploaded files…"):
        save_uploaded_dicoms(dicom_files, series_dir)
        rt_path = tmp_root / Path(rt_file.name).name
        with open(rt_path, "wb") as f:
            f.write(rt_file.getbuffer())

    # ── Preview ───────────────────────────────────────────────────────────
    if do_preview:
        with st.spinner("Rendering CT slice and tumour overlay…"):
            try:
                imgs = generate_previews(str(series_dir), str(rt_path), roi_name)
                st.markdown('<p class="sect-title">CT preview</p>', unsafe_allow_html=True)
                p1, p2, p3 = st.columns(3)
                p1.image(imgs["full"],    caption="Full CT slice",   use_container_width=True)
                p2.image(imgs["overlay"], caption="Tumour contour",  use_container_width=True)
                p3.image(imgs["cropped"], caption="Cropped region",  use_container_width=True)
            except Exception as e:
                st.error(f"Preview failed: {e}")

    # ── Prediction ────────────────────────────────────────────────────────
    if do_predict:
        prog = st.progress(0, text="Starting inference…")
        try:
            prog.progress(10, text="Loading CT volume…")
            result = run_prediction(
                str(series_dir), str(rt_path), roi_name,
                age, t_stage, n_stage, m_stage, overall, histology, gender,
            )
            prog.progress(100, text="Done!")
            prog.empty()

            risk = result["risk_score"]
            frac = 1 / (1 + math.exp(-risk))
            if frac < 0.4:
                band, cls = "Lower relative risk",   "risk-low"
            elif frac < 0.65:
                band, cls = "Moderate relative risk", "risk-mod"
            else:
                band, cls = "Higher relative risk",   "risk-high"

            st.markdown('<p class="sect-title">Prediction result</p>', unsafe_allow_html=True)
            st.markdown('<div class="result-panel">', unsafe_allow_html=True)
            st.markdown(f'<p class="{cls}">Risk score: {risk:.4f} · {band}</p>', unsafe_allow_html=True)
            st.progress(min(max(frac, 0.0), 1.0))

            med = result["median_survival_days"]
            if med is not None:
                st.write(f"**Estimated median survival:** {med:.0f} days (~{med/30.4:.1f} months)")
            else:
                st.write("**Estimated median survival:** beyond follow-up horizon (favourable outlook).")

            m1, m2 = st.columns(2)
            m1.metric("1-year survival probability", f"{result['prob_1yr']*100:.1f}%")
            m2.metric("2-year survival probability", f"{result['prob_2yr']*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="info-card" style="margin-top:14px">
            <h4>How to read this result</h4>
            <ul>
                <li><strong>Risk score</strong> is relative within the training cohort, not an absolute mortality probability.</li>
                <li><strong>Risk band</strong> (lower / moderate / higher) is a visual guide derived from a sigmoid of the score.</li>
                <li><strong>Median survival</strong> and <strong>1-/2-year probabilities</strong> combine the score with a baseline hazard curve.</li>
                <li>Two patients with similar scores can still have very different outcomes due to factors outside this model.</li>
            </ul>
            </div>""", unsafe_allow_html=True)

            report = {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "inputs": {"age": age, "t_stage": t_stage, "n_stage": n_stage,
                           "m_stage": m_stage, "overall_stage": overall,
                           "histology": histology, "gender": gender, "roi": roi_name},
                "outputs": {"risk_score": round(risk, 4), "risk_band": band,
                            "sigmoid_fraction": round(frac, 4),
                            "median_survival_days": med,
                            "prob_1yr": round(result["prob_1yr"], 4),
                            "prob_2yr": round(result["prob_2yr"], 4)},
                "model": {"test_cindex": result["test_cindex"]},
                "disclaimer": "Research prototype. Not clinical advice.",
            }
            st.download_button("Download result (JSON)",
                               data=json.dumps(report, indent=2),
                               file_name=f"lunexa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                               mime="application/json")
            with st.expander("Detailed breakdown"):
                st.json(report)
            st.caption("Research prototype only. Not clinical advice.")

        except Exception as e:
            prog.empty()
            st.error(f"Prediction failed: {e}")


# ---------------------------------------------------------------------------
# Symptoms
# ---------------------------------------------------------------------------

def page_symptoms():
    page_hero("Symptoms and Guidance",
              "Educational information only. Please see a clinician for personal medical advice.",
              SYMPTOM_HERO)

    st.markdown('<p class="sect-title">Common symptoms</p>', unsafe_allow_html=True)
    for row in [SYMPTOM_CARDS[:3], SYMPTOM_CARDS[3:]]:
        cols = st.columns(3)
        for col, card in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="symptom-card">
                    <img src="{card['img']}" alt="{card['title']}"/>
                    <div class="body"><h4>{card['title']}</h4><p>{card['desc']}</p></div>
                </div>""", unsafe_allow_html=True)

    st.markdown('<p class="sect-title">How to reduce risk and seek help</p>', unsafe_allow_html=True)
    tips = [
        ("Quit smoking",       "Stopping tobacco use and avoiding second-hand smoke is the largest modifiable risk factor."),
        ("Act early",          "Seek care for lasting cough, chest pain, or coughing up blood without delay."),
        ("Consider screening", "Smokers or former smokers aged 50+ may benefit from low-dose CT screening."),
        ("Stay active",        "Regular activity, good nutrition, and routine check-ups support lung health."),
        ("Know your exposures","Family history and occupational exposures like asbestos, radon, and diesel matter."),
        ("Ask about symptoms", "Use the Help page to learn terms such as DICOM, RTSTRUCT, and staging."),
    ]
    tcols = st.columns(3)
    for i, (t, d) in enumerate(tips):
        with tcols[i % 3]:
            st.markdown(f'<div class="info-card" style="margin-bottom:13px"><h4>{t}</h4><p>{d}</p></div>',
                        unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Educational videos</p>', unsafe_allow_html=True)
    vcols = st.columns(2)
    for i, (title, vid) in enumerate([
        ("Understand lung cancer", "hKV0f_h-f6w"),
        ("Warning signs", "GwVz0HyMyds"),
        ("Symptoms explained", "gIbmqYEf2ag"),
        ("Living with lung cancer", "XIemxRJRuuQ"),
    ]):
        with vcols[i % 2]:
            st.markdown(f"**{title}**")
            st.video(f"https://www.youtube.com/watch?v={vid}")

    st.error("**Urgent care:** sudden severe breathlessness, coughing up large amounts of blood, "
             "chest pain with dizziness, or new confusion.")


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

def page_help():
    page_hero("Help Centre",
              "Plain-language guides for lung cancer, DICOM, RTSTRUCT, staging, and Lunexa outputs.",
              HELP_HERO)

    q1, q2, q3 = st.columns(3)
    q1.markdown('<div class="info-card"><h4>New to CT scans?</h4><p>Start with what a CT is, what DICOM means, and how to spot a valid series.</p></div>', unsafe_allow_html=True)
    q2.markdown('<div class="info-card"><h4>Not sure about staging?</h4><p>Understand T, N, M, overall stage, and how they relate to prognosis.</p></div>', unsafe_allow_html=True)
    q3.markdown('<div class="info-card"><h4>Confused by the result?</h4><p>Learn what the risk score, band, and survival probabilities really mean.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Lung cancer basics</p>', unsafe_allow_html=True)
    with st.expander("What is lung cancer?", expanded=True):
        st.write("Lung cancer is a group of diseases in which lung cells grow uncontrollably. "
                 "Roughly 85% of cases are non-small-cell (NSCLC) — adenocarcinoma, squamous cell, "
                 "or large cell. Lunexa was trained on an NSCLC cohort.")
    with st.expander("Main risk factors"):
        st.write("Smoking is the largest risk factor. Second-hand smoke, radon, asbestos, diesel, "
                 "air pollution, family history, and previous chest radiation also raise risk.")
    with st.expander("How is lung cancer diagnosed?"):
        st.write("Usually chest X-ray or CT, then biopsy to confirm cell type. PET-CT and MRI "
                 "clarify spread. TNM staging then combines tumour size, nodes, and metastasis.")
    with st.expander("What treatments are available?"):
        st.write("Surgery, radiotherapy, chemotherapy, targeted therapy (EGFR, ALK, KRAS, ROS1), "
                 "and immunotherapy — chosen based on stage, cell type, and patient factors.")

    st.markdown('<p class="sect-title">Imaging and file formats</p>', unsafe_allow_html=True)
    with st.expander("What is DICOM and a DICOM series?"):
        st.write("DICOM is the standard medical image format. A CT series is all the 2D slice "
                 "files for one scan. Lunexa needs every slice — do not mix files from different scans.")
    with st.expander("What is RTSTRUCT, GTV-1, ROI, tumor mask?"):
        st.markdown("- **RTSTRUCT**: DICOM file storing clinician-drawn contours.\n"
                    "- **GTV-1**: Gross Tumour Volume label used by default.\n"
                    "- **ROI**: the structure name you type (must match exactly, case-sensitive).\n"
                    "- **Tumour mask**: 3D binary volume where 1 = tumour voxels.")
    with st.expander("How do I upload a folder of DICOM files?"):
        st.write("In Chrome you can drag the entire folder onto the file-upload area, or click "
                 "'Browse files' and navigate inside the folder, then select all files (Ctrl+A / Cmd+A). "
                 "Firefox and Safari may require selecting individual files.")

    st.markdown('<p class="sect-title">Staging and clinical inputs</p>', unsafe_allow_html=True)
    with st.expander("T, N, M, and Overall Stage explained"):
        st.markdown("- **T (0–4)**: primary tumour size and local extent.\n"
                    "- **N (0–3)**: regional lymph-node involvement.\n"
                    "- **M (0–1)**: distant metastasis.\n"
                    "- **Overall stage**: I, II, IIIa, IIIb — matching training categories.")
    with st.expander("What is histology?"):
        st.write("Cell type from biopsy: adenocarcinoma, squamous cell, large cell, or NOS "
                 "(not otherwise specified). Cell type affects treatment response and prognosis.")

    st.markdown('<p class="sect-title">Reading the prediction</p>', unsafe_allow_html=True)
    with st.expander("What does the risk score mean?"):
        st.write("A relative hazard within the training cohort — higher means higher predicted risk "
                 "vs. others in the dataset. Not an absolute mortality probability.")
    with st.expander("How reliable is the model?"):
        st.write("Validation C-index ~0.665, test C-index ~0.598. (0.5 = random, 1.0 = perfect.) "
                 "Better than chance, but nowhere near replacing clinical judgment.")
    with st.expander("Can I use this for real clinical decisions?"):
        st.write("No. Lunexa is a research prototype, not a certified medical device. Always follow "
                 "guideline-based care and your clinical team's advice.")

    st.markdown('<p class="sect-title">Troubleshooting</p>', unsafe_allow_html=True)
    with st.expander("ROI not found"):
        st.write("The ROI name must match a structure inside the RTSTRUCT exactly. "
                 "Open the RTSTRUCT in a DICOM viewer to list available names.")
    with st.expander("Prediction is very slow"):
        st.write("First inference after a cold start can take 60–90 s on CPU-only servers. "
                 "Repeat runs are faster once PyTorch and MedicalNet are warmed up.")
    with st.expander("App runs out of memory"):
        st.write("The free Streamlit tier has ~1 GB RAM. Torch + MedicalNet can exceed this. "
                 "If the app crashes mid-prediction, deploy on a Hugging Face Docker Space "
                 "(16 GB RAM, free CPU).")
    with st.expander("Preview shows blank / no tumour visible"):
        st.write("Zero voxels in the mask means the ROI name didn't match. "
                 "Double-check the ROI label inside the RTSTRUCT file.")

    st.info("Still stuck? Note the exact error, the page, and what you were doing — then contact the project owner.")


# ---------------------------------------------------------------------------
# How it Works
# ---------------------------------------------------------------------------

def page_how():
    page_hero("How Lunexa Works",
              "A five-step pipeline from raw DICOM to a survival risk estimate.",
              HOW_HERO)
    steps = [
        ("Upload DICOM and RTSTRUCT",
         "The RTSTRUCT aligns to the CT series and the named ROI becomes a 3D tumour mask."),
        ("Deep CT embedding",
         "MedicalNet ResNet-10 (pretrained on medical volumes) produces a 512-dim CT embedding."),
        ("Radiomics extraction",
         "PyRadiomics computes shape, first-order, and texture features. 16 selected descriptors are scaled."),
        ("Clinical encoding",
         "Age, T/N/M, overall stage, histology, and gender are one-hot encoded and normalised."),
        ("Fusion and survival estimate",
         "A DeepSurv-style head fuses all three streams into a risk score; a baseline hazard converts it to survival probabilities."),
    ]
    for i, (title, body) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="step-card">
            <div class="step-num">{i}</div>
            <div><h4>{title}</h4><p>{body}</p></div>
        </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def page_about():
    page_hero("About Lunexa",
              "A multimodal research tool for lung cancer survival risk assessment.",
              ABOUT_HERO)

    lcol, rcol = st.columns([1, 2.2])
    with lcol:
        st.markdown('<div class="about-logo">🫁</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align:center'>"
                    "<div style='font-size:1.5rem;font-weight:800;color:#0F766E'>Lunexa</div>"
                    "<div style='color:#64748B'>Lung Cancer Prognosis</div>"
                    "</div>", unsafe_allow_html=True)
    with rcol:
        st.write("Lunexa is a multimodal research prototype estimating relative survival risk in "
                 "lung cancer. It combines CT imaging, radiomics, and structured clinical variables "
                 "into one coherent risk estimate.")
        st.write("The goal is educational. Lunexa is **not** a certified medical device and must "
                 "never replace qualified clinical judgment, pathology, or guideline-based care.")
        m1, m2 = st.columns(2)
        m1.metric("Validation C-index", "0.665")
        m2.metric("Test C-index", "0.598")

    st.markdown('<p class="sect-title">Model overview</p>', unsafe_allow_html=True)
    ov1, ov2, ov3 = st.columns(3)
    ov1.markdown('<div class="info-card"><h4>CT branch</h4><p>MedicalNet ResNet-10 embeddings of the full DICOM volume, projected into a compact hidden layer before fusion.</p></div>', unsafe_allow_html=True)
    ov2.markdown('<div class="info-card"><h4>Radiomics branch</h4><p>16 PyRadiomics features from the RTSTRUCT-defined tumour, scaled to match training statistics.</p></div>', unsafe_allow_html=True)
    ov3.markdown('<div class="info-card"><h4>Fusion head</h4><p>Concatenated features feed a DeepSurv-style head outputting a scalar relative risk score.</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sect-title">How to interpret outputs</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
    <ul>
      <li><strong>Risk score</strong> is relative within the training cohort, not an absolute probability of death.</li>
      <li><strong>Risk band</strong> (lower / moderate / higher) is a visual guide based on a sigmoid of the score.</li>
      <li><strong>Median survival</strong> and <strong>1-/2-year probabilities</strong> come from combining the score with a baseline hazard curve.</li>
      <li><strong>C-index</strong> summarises ranking quality on validation and held-out test data during model development.</li>
    </ul>
    </div>""", unsafe_allow_html=True)

    st.markdown('<p class="sect-title">Intended audience</p>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    a1.markdown('<div class="info-card"><h4>Students</h4><p>Learn how multimodal survival models connect DICOM, radiomics, and clinical tables.</p></div>', unsafe_allow_html=True)
    a2.markdown('<div class="info-card"><h4>Researchers</h4><p>Prototype workflows needing CT + RTSTRUCT + structured clinical fields.</p></div>', unsafe_allow_html=True)
    a3.markdown('<div class="info-card"><h4>Educators</h4><p>Demonstrate transparent risk outputs without presenting them as bedside advice.</p></div>', unsafe_allow_html=True)

    st.warning("**Disclaimer:** Lunexa is a research prototype, not a certified medical device. "
               "Never use it alone for clinical decisions. Always rely on qualified professionals.")
    st.caption("Group 7 · Multimodal Cancer Prognosis · University research project")


# ---------------------------------------------------------------------------
# Router + footer
# ---------------------------------------------------------------------------
if   page == "Home":        page_home()
elif page == "Predict":     page_predict()
elif page == "Symptoms":    page_symptoms()
elif page == "Help":        page_help()
elif page == "How it Works":page_how()
else:                       page_about()

st.markdown("""
<div class="footer-bar">
  <strong>Lunexa</strong> · Lung Cancer Prognosis and Risk Assessment<br/>
  Home · Predict · Symptoms · Help · How it Works · About
</div>""", unsafe_allow_html=True)