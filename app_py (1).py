import streamlit as st
import pandas as pd
import pickle
import time

# 1. PAGE CONFIGURATION (Must be the first Streamlit command)
st.set_page_config(
    page_title="Travel Churn Predictor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS FOR STYLING
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Headers */
    h1 {
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Customizing the predict button */
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Style the result cards */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. LOAD COMPONENTS
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
    st.error(f"Error loading model files: {e}. Ensure 'rf_model.pkl' and 'label_encoders.pkl' are in the same folder.")
    st.stop()

# 4. APP HEADER
st.title("✈️ Smart Travel Customer Retention AI")
st.markdown("<p style='text-align: center; font-size: 18px; color: #4B5563;'>Predict customer churn instantly using advanced Random Forest Machine Learning.</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. SIDEBAR DESIGN
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.header("⚙️ App Settings")
    st.write("Fill in the customer's details on the main page to get a live churn prediction.")
    
    with st.expander("ℹ️ What is Churn?"):
        st.write("""
        **Customer Churn** is the percentage of customers who stop using a company's services. 
        Predicting this helps businesses retain valuable customers by taking proactive measures!
        """)
    st.markdown("---")
    st.caption("Developed for B.Tech Gen AI Final Project")

# 6. MAIN LAYOUT (Using columns for a clean grid)
st.markdown("### 👤 Customer Profile Input")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("🎂 Age", min_value=18, max_value=100, value=30)
    frequent_flyer = st.selectbox("✈️ Frequent Flyer?", ["Yes", "No"])

with col2:
    annual_income = st.selectbox("💰 Annual Income Class", ["Low Income", "Middle Income", "High Income"])
    services_opted = st.slider("🛎️ Services Opted", min_value=1, max_value=10, value=1)

with col3:
    social_media = st.selectbox("📱 Social Media Synced?", ["Yes", "No"])
    booked_hotel = st.selectbox("🏨 Booked Hotel?", ["Yes", "No"])

st.markdown("<br>", unsafe_allow_html=True)

# 7. PREDICTION LOGIC & ANIMATIONS
if st.button("🚀 Analyze Customer Churn Risk"):
    
    # Fake loading animation for a premium feel
    with st.spinner('Running data through Random Forest Ensembles...'):
        time.sleep(1.5)
        
    # Prepare data
    input_data = pd.DataFrame({
        'Age': [age],
        'FrequentFlyer': [frequent_flyer],
        'AnnualIncomeClass': [annual_income],
        'ServicesOpted': [services_opted],
        'AccountSyncedToSocialMedia': [social_media],
        'BookedHotelOrNot': [booked_hotel]
    })
    
    try:
        # Encode inputs
        for col in ['FrequentFlyer', 'AnnualIncomeClass', 'AccountSyncedToSocialMedia', 'BookedHotelOrNot']:
            input_data[col] = encoders[col].transform(input_data[col])
            
        # Predict
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        # Display highly visual results
        st.markdown("---")
        st.markdown("### 📊 Prediction Results")
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            if prediction == 1:
                st.markdown("""
                <div class="result-card" style="border-top: 5px solid #EF4444;">
                    <h2 style="color: #EF4444;">🚨 CHURN RISK</h2>
                    <p>Customer is likely to leave.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card" style="border-top: 5px solid #10B981;">
                    <h2 style="color: #10B981;">✅ SAFE</h2>
                    <p>Customer is likely to stay.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons() # Fun animation for positive result
                
        with res_col2:
            st.markdown("#### Churn Probability Level")
            # Dynamic progress bar color based on risk
            if probability > 0.7:
                st.progress(float(probability))
                st.error(f"High Risk: **{probability:.1%}** chance of churning.")
            elif probability > 0.4:
                st.progress(float(probability))
                st.warning(f"Moderate Risk: **{probability:.1%}** chance of churning.")
            else:
                st.progress(float(probability))
                st.success(f"Low Risk: **{probability:.1%}** chance of churning.")
                
    except Exception as e:
        st.error(f"An error occurred: {e}")
