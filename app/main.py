import streamlit as st
import pandas as pd
from services.profile_service import generate_profile


st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataMind AI")
uploaded_file = st.file_uploader(
"📂 Upload your CSV file",
    type=["csv"]

)
if uploaded_file is not None:
    
    st.success("✅ File uploaded successfully!")
    df = pd.read_csv(uploaded_file)
    profile = generate_profile(df)

    st.subheader("📊 Dataset Profile")
    st.write(profile)

    st.subheader("📋 Dataset Preview")

    st.dataframe(df.head())

st.subheader("Your Intelligent Data Analysis Assistant")

st.write("Welcome! Upload your dataset to begin intelligent analysis.")