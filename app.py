import streamlit as st
import pandas as pd
from utils.ai import get_ai_response
from utils.core import predict_disease, generate_treatment_plan
from utils.visualizer import display_health_analytics

# ---- Page Config ----
st.set_page_config(page_title="🧠 HealthAI", layout="wide")
st.markdown("<h1 style='text-align: center;'>🩺 HealthAI - Intelligent Healthcare Assistant</h1>", unsafe_allow_html=True)

# ---- Sidebar Navigation ----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=80)
    menu = st.radio("📋 Navigation", ["🏥 Patient Chat", "🔍 Disease Prediction", "💊 Treatment Plan", "📈 Health Analytics"])
    st.markdown("---")
    st.markdown("👤 Developed by Divya Reddy")
    st.caption("🔐 Data Secure · IBM Watsonx Powered")

# ---- Session for Patient Profile ----
if "profile" not in st.session_state:
    st.session_state.profile = {}

# ---- Left Panel: Patient Profile Form ----
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## 👤 Patient Profile")
    with st.form("profile_form"):
        name = st.text_input("Name", st.session_state.profile.get("name", ""))
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.profile.get("age", 30))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.profile.get("gender", "Male")))
        history = st.text_area("Medical History", st.session_state.profile.get("history", ""))
        medications = st.text_area("Current Medications", st.session_state.profile.get("medications", ""))
        allergies = st.text_input("Allergies", st.session_state.profile.get("allergies", ""))

        submitted = st.form_submit_button("💾 Save Profile")
        if submitted:
            st.session_state.profile = {
                "name": name,
                "age": age,
                "gender": gender,
                "history": history,
                "medications": medications,
                "allergies": allergies
            }
            st.success("✅ Profile saved!")

    if st.session_state.profile:
        st.markdown("#### 🧾 Saved Info")
        st.json(st.session_state.profile)

# ---- Right Panel: Functional Modules ----
with col2:

    profile = st.session_state.profile
    profile_summary = f"""
    Patient Info:
    - Age: {profile.get('age')}
    - Gender: {profile.get('gender')}
    - History: {profile.get('history')}
    - Medications: {profile.get('medications')}
    - Allergies: {profile.get('allergies')}
    """

    # ---- Patient Chat ----
    if menu == "🏥 Patient Chat":
        st.subheader("💬 Patient Chat Assistant")
        user_input = st.text_area("📝 Ask a medical question:")

        if st.button("🧠 Get AI Response"):
            if user_input.strip():
                with st.spinner("Consulting HealthAI..."):
                    prompt = f"You are a healthcare assistant. Respond based on the following profile and question:\n{profile_summary}\n\nQuestion: {user_input}"
                    response = get_ai_response(prompt)
                    st.success(response)
            else:
                st.warning("❗ Please enter a question.")

    # ---- Disease Prediction ----
    elif menu == "🔍 Disease Prediction":
        st.subheader("🧾 Disease Prediction Based on Symptoms & Profile")
        symptoms = st.text_input("🔬 Enter symptoms (comma-separated):")

        if st.button("🔎 Predict Disease"):
            if symptoms.strip():
                with st.spinner("Analyzing symptoms..."):
                    prompt = f"Given the patient profile:\n{profile_summary}\n\nSymptoms: {symptoms}\n\nPredict possible diseases and next steps."
                    result = get_ai_response(prompt)
                    st.success(result)
            else:
                st.warning("❗ Please enter symptoms.")

    # ---- Treatment Plan ----
    elif menu == "💊 Treatment Plan":
        st.subheader("📋 Generate Personalized Treatment Plan")
        disease = st.text_input("🏷️ Enter diagnosed condition:")

        if st.button("📄 Get Treatment Plan"):
            if disease.strip():
                with st.spinner("Creating treatment guidance..."):
                    prompt = f"Generate a treatment plan for this patient:\n{profile_summary}\n\nCondition: {disease}"
                    plan = get_ai_response(prompt)
                    st.success(plan)
            else:
                st.warning("❗ Enter a condition to continue.")

    # ---- Health Analytics ----
    elif menu == "📈 Health Analytics":
        st.subheader("📊 Patient Health Analytics")

        try:
            df = pd.read_csv("data/patient_data.csv")
            metric = st.selectbox("📌 Select a metric to visualize", df.columns[1:])
            st.line_chart(df.set_index(df.columns[0])[metric])

            if st.button("🧠 Generate AI Insight"):
                summary = df[metric].describe().to_string()
                prompt = f"Given the patient's profile:\n{profile_summary}\n\nAnd health data summary:\n{summary}\n\nProvide analysis and health advice."
                ai_insight = get_ai_response(prompt)
                st.info(ai_insight)
        except FileNotFoundError:
            st.error("❌ `data/patient_data.csv` not found.")

# ---- Footer ----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center><small>© 2025 HealthAI · Built with ❤️ using Streamlit and IBM Watsonx</small></center>", unsafe_allow_html=True)
