import streamlit as st
import pandas as pd
import pickle
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Travel Churn Predictor",
    page_icon="✈️",
    layout="wide",
)

# ---------------- MODERN UI CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #F1F5F9;
}

/* Glass container */
.block-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Headings */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700;
}

/* Labels */
label, .stMarkdown {
    color: #E2E8F0 !important;
}

/* Inputs */
.stSelectbox div, .stNumberInput div, .stSlider {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px;
}

/* Button */
div.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1E40AF);
    color: white;
    border-radius: 12px;
    font-weight: bold;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(37,99,235,0.5);
}

/* Result Cards */
.result-card {
    background: rgba(30, 41, 59, 0.85);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
    color: white;
    margin-top: 20px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
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
    st.error(f"Error loading model files: {e}")
    st.stop()

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>✈️ Smart Travel Customer Retention AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#CBD5F5;'>Real-time churn prediction powered by machine learning</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.write("Enter customer data to predict churn.")

    st.markdown("#### 📊 Model Info")
    st.write("**Algorithm:** Random Forest")
    st.write("**Target:** Customer Retention")

    with st.expander("ℹ️ What is Churn?"):
        st.write("Customers who stop using services.")

# ---------------- INPUT SECTION ----------------
st.markdown("## 👤 Customer Input")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("🎂 Age", 18, 100, 30)
    frequent_flyer = st.selectbox("✈️ Frequent Flyer", ["Yes", "No"])

with col2:
    annual_income = st.selectbox("💰 Income", ["Low Income", "Middle Income", "High Income"])
    services_opted = st.slider("🛎️ Services", 1, 10, 2)

with col3:
    social_media = st.selectbox("📱 Social Media", ["Yes", "No"])
    booked_hotel = st.selectbox("🏨 Booked Hotel", ["Yes", "No"])

st.markdown("")

# ---------------- PREDICTION ----------------
if st.button("🚀 Analyze Risk"):

    with st.spinner("Analyzing..."):
        time.sleep(1)

    input_data = pd.DataFrame({
        'Age': [age],
        'FrequentFlyer': [frequent_flyer],
        'AnnualIncomeClass': [annual_income],
        'ServicesOpted': [services_opted],
        'AccountSyncedToSocialMedia': [social_media],
        'BookedHotelOrNot': [booked_hotel]
    })

    try:
        for col in ['FrequentFlyer', 'AnnualIncomeClass', 'AccountSyncedToSocialMedia', 'BookedHotelOrNot']:
            input_data[col] = encoders[col].transform(input_data[col])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        st.markdown("## 📊 Results")

        colA, colB = st.columns([1, 2])

        # Result Card
        with colA:
            if prediction == 1:
                st.markdown(f"""
                <div class="result-card" style="border-top: 5px solid #EF4444;">
                    <h2>🚨 HIGH RISK</h2>
                    <p>Customer likely to churn</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card" style="border-top: 5px solid #10B981;">
                    <h2>✅ SAFE</h2>
                    <p>Customer likely to stay</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

        # Probability Section
        with colB:
            st.subheader("Churn Probability")

            st.progress(float(probability))

            if probability > 0.7:
                st.error(f"High Risk: {probability:.1%}")
            elif probability > 0.4:
                st.warning(f"Moderate Risk: {probability:.1%}")
            else:
                st.success(f"Low Risk: {probability:.1%}")

    except Exception as e:
        st.error(f"Error: {e}")
