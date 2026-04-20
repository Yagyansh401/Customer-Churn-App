import streamlit as st
import pandas as pd
import pickle
import time

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Travel Churn Predictor | Enterprise AI",
    page_icon="🛫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PREMIUM CSS — DARK LUXE AVIATION THEME
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Base Reset ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #E8EDF5;
    }

    /* ── Deep Space Background ── */
    .stApp {
        background: #080D1A;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(30, 80, 180, 0.35), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0, 180, 140, 0.12), transparent),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231a2540' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }

    /* ── Block padding ── */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px;
    }

    /* ── Headings ── */
    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }

    h1 { font-size: 2.6rem !important; font-weight: 800 !important; }
    h3 { font-size: 1.35rem !important; font-weight: 700 !important; color: #CBD5FF !important; }
    h4 { font-size: 1.05rem !important; font-weight: 600 !important; color: #94A3CC !important; text-transform: uppercase; letter-spacing: 0.08em; }

    /* ── Paragraph / label text ── */
    p, label, .stMarkdown, div[data-testid="stText"],
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #C8D0E8 !important;
        font-size: 0.95rem !important;
    }

    /* ── Input widget backgrounds ── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(100,130,255,0.25) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        transition: border 0.25s ease, box-shadow 0.25s ease;
    }
    .stSelectbox > div > div:hover,
    .stNumberInput > div > div > input:hover {
        border-color: rgba(100,160,255,0.55) !important;
        box-shadow: 0 0 0 3px rgba(80,130,255,0.12) !important;
    }

    /* Dropdown arrow and option text */
    .stSelectbox svg { color: #6B8EFF !important; }
    .stSelectbox div[role="listbox"] { background: #111827 !important; }
    .stSelectbox div[role="option"] { color: #E8EDF5 !important; }

    /* ── Slider ── */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #3B6FFF, #00D4AA) !important;
    }
    .stSlider > div > div > div > div > div {
        background: #FFFFFF !important;
        border: 2px solid #3B6FFF !important;
        box-shadow: 0 0 12px rgba(59,111,255,0.5) !important;
    }
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] { color: #6B7FB8 !important; }

    /* ── Number input stepper buttons ── */
    .stNumberInput button {
        background: rgba(59,111,255,0.18) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
    }
    .stNumberInput button:hover { background: rgba(59,111,255,0.4) !important; }

    /* ── CTA Button ── */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563EB 0%, #0EA5E9 50%, #06B6D4 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2rem;
        font-family: 'Syne', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em;
        box-shadow: 0 4px 20px rgba(37,99,235,0.45), 0 0 0 1px rgba(255,255,255,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        margin-top: 1.5rem;
        text-transform: uppercase;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(37,99,235,0.55), 0 0 0 1px rgba(255,255,255,0.15);
    }
    div.stButton > button:first-child:active { transform: translateY(0); }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080D1A 0%, #0D1529 100%) !important;
        border-right: 1px solid rgba(59,111,255,0.2) !important;
    }
    section[data-testid="stSidebar"] * { color: #C8D0E8 !important; }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] strong { color: #6B8EFF !important; }
    section[data-testid="stSidebar"] .stExpander {
        background: rgba(59,111,255,0.08) !important;
        border: 1px solid rgba(59,111,255,0.2) !important;
        border-radius: 10px !important;
    }

    /* ── HR divider ── */
    hr { border-color: rgba(59,111,255,0.2) !important; margin: 1.5rem 0; }

    /* ── Metric cards ── */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(59,111,255,0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    [data-testid="metric-container"] label { color: #94A3CC !important; font-size: 0.8rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

    /* ── Progress bar ── */
    .stProgress > div > div { background: rgba(255,255,255,0.08) !important; border-radius: 99px; }
    .stProgress > div > div > div { 
        background: linear-gradient(90deg, #3B6FFF, #00D4AA) !important;
        border-radius: 99px !important;
    }

    /* ── Alert / info boxes ── */
    .stSuccess { background: rgba(0,212,150,0.12) !important; border-color: #00D496 !important; color: #A7F3D0 !important; }
    .stWarning { background: rgba(251,191,36,0.12) !important; border-color: #FBBF24 !important; color: #FDE68A !important; }
    .stError   { background: rgba(239,68,68,0.12)  !important; border-color: #EF4444 !important; color: #FCA5A5 !important; }
    .stInfo    { background: rgba(59,111,255,0.12) !important; border-color: #3B6FFF !important; color: #BAC8FF !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #3B6FFF !important; }

    /* ── Caption / small text ── */
    .stCaption, small, caption { color: #6B7FB8 !important; }

    /* ── Custom glass cards ── */
    .glass-card {
        background: rgba(20, 35, 70, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(59,111,255,0.25);
        padding: 1.75rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06);
        animation: slide-up 0.5s cubic-bezier(0.22, 1, 0.36, 1);
    }

    /* ── Input section panels ── */
    .input-panel {
        background: rgba(15, 25, 55, 0.7);
        border: 1px solid rgba(59,111,255,0.18);
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }

    /* ── Hero subtitle ── */
    .hero-sub {
        color: #7B92CC !important;
        font-size: 1.1rem;
        margin-top: -0.5rem;
        font-weight: 300;
        letter-spacing: 0.01em;
    }

    /* ── Status badges ── */
    .status-badge {
        display: inline-block;
        padding: 0.3em 0.9em;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        letter-spacing: 0.08em;
        font-family: 'DM Sans', sans-serif;
        text-transform: uppercase;
    }
    .badge-safe {
        background: rgba(0,212,150,0.18);
        color: #34D399;
        border: 1px solid rgba(0,212,150,0.35);
    }
    .badge-risk {
        background: rgba(239,68,68,0.18);
        color: #F87171;
        border: 1px solid rgba(239,68,68,0.35);
    }

    /* ── Model info chips ── */
    .chip {
        display: inline-block;
        background: rgba(59,111,255,0.15);
        border: 1px solid rgba(59,111,255,0.3);
        color: #93AAFF !important;
        padding: 0.25rem 0.7rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 2px;
    }

    /* ── Glowing dot ── */
    .dot-online {
        display: inline-block;
        width: 10px; height: 10px;
        background: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981, 0 0 16px rgba(16,185,129,0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 8px #10B981, 0 0 16px rgba(16,185,129,0.4); }
        50%       { box-shadow: 0 0 4px #10B981, 0 0 8px rgba(16,185,129,0.2); }
    }

    /* ── Animations ── */
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Section label ── */
    .section-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #3B6FFF !important;
        margin-bottom: 0.2rem;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(59,111,255,0.15);
        color: #3D4F7A !important;
        font-size: 0.8rem;
        letter-spacing: 0.04em;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #080D1A; }
    ::-webkit-scrollbar-thumb { background: #1E3A7A; border-radius: 3px; }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MODEL LOADING
# ==========================================
@st.cache_resource
def load_components():
    with open('rf_model.pkl', 'rb') as file:
        model = pickle.load(file)
    with open('label_encoders.pkl', 'rb') as file:
        encoders = pickle.load(file)
    return model, encoders

try:
    model, encoders = load_components()
except Exception as e:
    st.error(f"⚠️ **Critical Error:** Unable to load model components.\n\nDetails: {e}")
    st.info("Ensure `rf_model.pkl` and `label_encoders.pkl` exist in the same directory.")
    st.stop()


# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
            <span class="dot-online"></span>
            <span style="font-weight:600;font-size:0.9rem;color:#A0B4D6;letter-spacing:0.05em;">SYSTEM ONLINE</span>
        </div>
    """, unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=72)

    st.markdown("""
        <div style="margin:1rem 0;">
            <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#FFFFFF;">
                ⚙️ Control Panel
            </div>
        </div>
        <hr style="border-color:rgba(59,111,255,0.2);">
        <div class="section-label" style="margin-top:1rem;">Model Information</div>
        <div style="margin-top:0.6rem;">
            <div style="margin-bottom:0.4rem;"><span class="chip">🌲 Random Forest</span></div>
            <div><span class="chip">🎯 Customer Retention</span></div>
        </div>
        <hr style="border-color:rgba(59,111,255,0.2);margin-top:1.2rem;">
    """, unsafe_allow_html=True)

    with st.expander("📖 Glossary & Risk Levels"):
        st.markdown("""
        <div style="color:#C8D0E8;font-size:0.88rem;line-height:1.7;">
        <strong style="color:#6B8EFF;">Churn Risk</strong> — The likelihood a customer will abandon the service.<br><br>
        🟢 <strong style="color:#34D399;">Low Risk</strong> — Below 40%<br>
        🟡 <strong style="color:#FBBF24;">Moderate Risk</strong> — 40% – 70%<br>
        🔴 <strong style="color:#F87171;">High Risk</strong> — Above 70%
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer" style="margin-top:2rem;">
            © 2026 Enterprise AI Solutions
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 5. HERO HEADER
# ==========================================
st.markdown("""
    <div style="display:flex;align-items:center;gap:1.2rem;margin-bottom:0.25rem;">
        <div style="font-size:3rem;line-height:1;">✈️</div>
        <div>
            <h1 style="margin:0;background:linear-gradient(135deg,#FFFFFF 30%,#6B8EFF 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                Travel Customer Retention AI
            </h1>
            <p class="hero-sub">Real-time churn probability scoring powered by ensemble machine learning.</p>
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)


# ==========================================
# 6. INPUT SECTION HEADER
# ==========================================
st.markdown("""
    <div class="section-label" style="margin-bottom:0.3rem;">Customer Profile</div>
    <h3 style="margin-top:0;">👤 Input Customer Parameters</h3>
""", unsafe_allow_html=True)

# ==========================================
# 7. INPUT FORM
# ==========================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown('<h4>🧑 Demographics & Profile</h4>', unsafe_allow_html=True)
    age = st.number_input("🎂 Age", min_value=18, max_value=100, value=30,
                          help="Customer's current age.")
    annual_income = st.selectbox("💰 Annual Income Class",
                                 ["Low Income", "Middle Income", "High Income"], index=1)
    frequent_flyer = st.selectbox("✈️ Frequent Flyer Status", ["Yes", "No"], index=1)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    st.markdown('<h4>📊 Engagement & Behavior</h4>', unsafe_allow_html=True)
    services_opted = st.slider("🛎️ Services Opted", min_value=1, max_value=10, value=2,
                               help="Total number of add-on services utilized by the customer.")
    social_media = st.selectbox("📱 Social Media Synced", ["Yes", "No"], index=1)
    booked_hotel = st.selectbox("🏨 Booked Hotel", ["Yes", "No"], index=1)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 8. PREDICT BUTTON
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🚀 Initialize Prediction Analysis")


# ==========================================
# 9. RESULTS
# ==========================================
if run:
    with st.spinner("Aggregating data and computing ensemble predictions…"):
        time.sleep(1.2)

    input_data = pd.DataFrame({
        'Age': [age],
        'FrequentFlyer': [frequent_flyer],
        'AnnualIncomeClass': [annual_income],
        'ServicesOpted': [services_opted],
        'AccountSyncedToSocialMedia': [social_media],
        'BookedHotelOrNot': [booked_hotel]
    })

    try:
        for col in ['FrequentFlyer', 'AnnualIncomeClass',
                    'AccountSyncedToSocialMedia', 'BookedHotelOrNot']:
            input_data[col] = encoders[col].transform(input_data[col])

        prediction   = model.predict(input_data)[0]
        probability  = model.predict_proba(input_data)[0][1]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="section-label" style="margin-bottom:0.3rem;">Prediction Output</div>
            <h3 style="margin-top:0;">📈 Analysis Results</h3>
        """, unsafe_allow_html=True)

        res_col1, res_col2 = st.columns([1, 1.5], gap="large")

        with res_col1:
            if prediction == 1:
                st.markdown(f"""
                <div class="glass-card" style="border-left:5px solid #EF4444;">
                    <div class="status-badge badge-risk" style="margin-bottom:12px;">⚡ ACTION REQUIRED</div>
                    <h2 style="color:#FCA5A5 !important;margin:0.4rem 0 0.6rem;">High Churn Risk</h2>
                    <p style="color:#9BAAC8;font-size:0.9rem;line-height:1.6;margin:0;">
                        This customer exhibits behavioral patterns strongly correlated with account abandonment.
                        Immediate retention intervention is recommended.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="border-left:5px solid #10B981;">
                    <div class="status-badge badge-safe" style="margin-bottom:12px;">✅ HEALTHY ACCOUNT</div>
                    <h2 style="color:#6EE7B7 !important;margin:0.4rem 0 0.6rem;">Customer Retained</h2>
                    <p style="color:#9BAAC8;font-size:0.9rem;line-height:1.6;margin:0;">
                        This customer shows strong loyalty indicators and is unlikely to churn in the near term.
                        Continue standard engagement protocols.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

        with res_col2:
            met_col1, met_col2 = st.columns(2)
            with met_col1:
                st.metric(
                    label="Churn Probability",
                    value=f"{probability:.1%}",
                    delta="Critical Risk" if probability > 0.6 else "Stable",
                    delta_color="inverse"
                )
            with met_col2:
                st.metric(
                    label="Retention Score",
                    value=f"{(1 - probability):.1%}",
                    delta="Optimal" if (1 - probability) > 0.6 else "Warning"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("📡 Risk Level Indicator")
            st.progress(float(probability))

            if probability >= 0.7:
                st.error("🚨 Immediate intervention recommended — churn is highly likely.")
            elif probability >= 0.4:
                st.warning("⚠️ Monitor engagement closely — moderate churn risk detected.")
            else:
                st.success("✅ Customer health is optimal — low churn probability.")

    except Exception as e:
        st.error(f"Prediction Pipeline Error: {e}")


# ==========================================
# 10. FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        Powered by Streamlit & Scikit-Learn &nbsp;·&nbsp; Designed for high-performance ML deployments &nbsp;·&nbsp; © 2026 Enterprise AI Solutions
    </div>
""", unsafe_allow_html=True)
