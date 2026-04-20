import streamlit as st
import pandas as pd
import pickle
import time

# ==========================================
# 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="Travel Churn Predictor | Enterprise AI",
    page_icon="🛫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PREMIUM CSS & GLASSMORPHISM INJECTION
# ==========================================
st.markdown("""
    <style>
    /* Import modern SaaS font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Typography and Background */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    }

    /* Top Padding Adjustment */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Typography Styling */
    h1, h2, h3 {
        color: #102A43;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    
    /* Custom primary button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        margin-top: 1rem;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }

    /* Glassmorphism Result Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        animation: slide-up 0.5s ease-out;
    }

    /* Animations */
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Custom Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25em 0.75em;
        font-size: 0.875em;
        font-weight: 600;
        border-radius: 9999px;
    }
    .badge-safe { background-color: #d1fae5; color: #065f46; }
    .badge-risk { background-color: #fee2e2; color: #991b1b; }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
        font-size: 0.875rem;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MODEL LOADING WITH ERROR HANDLING
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
    st.error(f"⚠️ **Critical Error:** Unable to load model components. \n\nDetails: {e}")
    st.info("Ensure 'rf_model.pkl' and 'label_encoders.pkl' exist in the same directory as this script.")
    st.stop()


# ==========================================
# 4. SIDEBAR DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 12px; height: 12px; background-color: #10B981; border-radius: 50%;"></div>
            <span style="font-weight: 600; color: #334155;">System Online</span>
        </div>
        <br>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("## ⚙️ Control Panel")
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.write("**Algorithm:** Random Forest")
    st.write("**Target:** Customer Retention")
    
    with st.expander("ℹ️ Glossary & Info"):
        st.write("""
        **Churn Risk:** The calculated likelihood that a customer will abandon the service.
        * **Low Risk:** < 40%
        * **Moderate Risk:** 40% - 70%
        * **High Risk:** > 70%
        """)
        
    st.markdown("---")
    st.caption("© 2026 Enterprise AI Solutions")


# ==========================================
# 5. MAIN HEADER & HERO SECTION
# ==========================================
col_header1, col_header2 = st.columns([1, 8])
with col_header1:
    st.markdown("<h1 style='font-size: 3rem;'>✈️</h1>", unsafe_allow_html=True)
with col_header2:
    st.markdown("<h1>Travel Customer Retention AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #475569; margin-top: -10px;'>Real-time churn probability scoring powered by ensemble machine learning.</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #cbd5e1;'>", unsafe_allow_html=True)


# ==========================================
# 6. INPUT FORMS (Logically Grouped)
# ==========================================
st.markdown("### 👤 Input Customer Parameters")

# Grouping inputs logically into containers for better UX
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Demographics & Profile")
        age = st.number_input("🎂 Age", min_value=18, max_value=100, value=30, help="Customer's current age.")
        annual_income = st.selectbox("💰 Annual Income", ["Low Income", "Middle Income", "High Income"], index=1)
        frequent_flyer = st.selectbox("✈️ Frequent Flyer Status", ["Yes", "No"], index=1)

    with col2:
        st.markdown("#### Engagement & Behavior")
        services_opted = st.slider("🛎️ Services Opted", min_value=1, max_value=10, value=2, help="Total number of add-on services utilized.")
        social_media = st.selectbox("📱 Social Media Synced", ["Yes", "No"], index=1)
        booked_hotel = st.selectbox("🏨 Booked Hotel", ["Yes", "No"], index=1)


# ==========================================
# 7. PREDICTION ENGINE & VISUALIZATION
# ==========================================
if st.button("Initialize Prediction Analysis"):
    
    # Premium loading state
    with st.spinner('Aggregating data and computing ensemble predictions...'):
        time.sleep(1.2) # Smooth UI transition
        
    # Prepare Dataframe
    input_data = pd.DataFrame({
        'Age': [age],
        'FrequentFlyer': [frequent_flyer],
        'AnnualIncomeClass': [annual_income],
        'ServicesOpted': [services_opted],
        'AccountSyncedToSocialMedia': [social_media],
        'BookedHotelOrNot': [booked_hotel]
    })
    
    try:
        # Encode inputs safely
        for col in ['FrequentFlyer', 'AnnualIncomeClass', 'AccountSyncedToSocialMedia', 'BookedHotelOrNot']:
            input_data[col] = encoders[col].transform(input_data[col])
            
        # Execute ML Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        # UI Rendering for Results
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📈 Analysis Results")
        
        res_col1, res_col2 = st.columns([1, 1.5])
        
        # COLUMN 1: The Verdict Card
        with res_col1:
            if prediction == 1:
                st.markdown(f"""
                <div class="glass-card" style="border-top: 6px solid #ef4444;">
                    <div class="status-badge badge-risk" style="margin-bottom: 10px;">ACTION REQUIRED</div>
                    <h2 style="color: #991b1b; margin-top: 0;">High Churn Risk</h2>
                    <p style="color: #475569;">This customer exhibits behavioral patterns strongly correlated with account abandonment.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="border-top: 6px solid #10b981;">
                    <div class="status-badge badge-safe" style="margin-bottom: 10px;">HEALTHY ACCOUNT</div>
                    <h2 style="color: #065f46; margin-top: 0;">Customer Retained</h2>
                    <p style="color: #475569;">This customer shows high loyalty indicators and is unlikely to churn in the near term.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                
        # COLUMN 2: Data Metrics
        with res_col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="margin-top: 0; color: #334155;">Probability Breakdown</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Using Streamlit's native metric component for a SaaS look
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
                    label="Retention Probability", 
                    value=f"{(1 - probability):.1%}", 
                    delta="Optimal" if (1 - probability) > 0.6 else "Warning"
                )
            
            # Visual Progress Bar
            st.caption("Risk Indicator Tracker")
            if probability >= 0.7:
                st.progress(float(probability))
                st.error("🚨 Immediate intervention recommended.")
            elif probability >= 0.4:
                st.progress(float(probability))
                st.warning("⚠️ Monitor customer engagement closely.")
            else:
                st.progress(float(probability))
                st.success("✅ Customer health score is optimal.")

    except Exception as e:
        st.error(f"Prediction Pipeline Error: {e}")

# ==========================================
# 8. FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        Powered by Streamlit & Scikit-Learn | Designed for high-performance ML deployments.
    </div>
""", unsafe_allow_html=True)
