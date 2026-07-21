import streamlit as st

from services.validation_service import validate_file
from services.profile_service import generate_profile


st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)


st.title("📊 DataMind AI")
st.subheader("Your Intelligent Data Analysis Assistant")
st.write(
    "Upload your dataset and let AI inspect it before analysis."
)


uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


if uploaded_file is None:

    st.info("Please upload a CSV file to continue.")

    st.stop()


result = validate_file(uploaded_file)


if not result["success"]:

    st.error(result["message"])

    st.stop()


st.success(result["message"])


df = result["dataframe"]


st.subheader("📋 Validation Report")

st.write(result["report"])


profile_result = generate_profile(df)


if profile_result["success"]:

    profile = profile_result["profile"]

    st.subheader("📈 Dataset Profile")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            profile["rows"]
        )

    with col2:

        st.metric(
            "Columns",
            profile["columns"]
        )

    with col3:

        st.metric(
            "Missing Values",
            profile["total_missing_values"]
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            profile["total_duplicate_rows"]
        )

else:

    st.error(profile_result["message"])


st.markdown("---")

st.subheader("👀 Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)


st.markdown("---")

st.info(
    "🧹 Smart Data Cleaning Module Coming Soon..."
)