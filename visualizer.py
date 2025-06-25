import plotly.express as px
import streamlit as st
import pandas as pd

def display_health_analytics(df):
    uploaded_file = st.file_uploader("Upload your health data (CSV or Excel)", type=['csv', 'xlsx'])

    if uploaded_file is not None:
       try:
          if uploaded_file.name.endswith('.csv'): 
            df = pd.read_csv(uploaded_file)
          else:
            df = pd.read_excel(uploaded_file)

          st.success("File uploaded successfully!")

        # Display file content
          st.subheader("📊 Raw Data")
          st.dataframe(df)

        # Quick stats
          st.subheader("📈 Data Summary")
          st.write(df.describe())

       except Exception as e:
        st.error(f"Error reading file: {e}")
    st.subheader("📈 Health Metrics Overview")

    fig1 = px.line(df, x='Date', y='HeartRate', title='Heart Rate Over Time', markers=True)
    st.plotly_chart(fig1)

    if 'BloodPressure' in df.columns:
        fig2 = px.line(df, x='Date', y='BloodPressure', title='Blood Pressure Over Time')
        st.plotly_chart(fig2)