import streamlit as st

from services.validation_service import validate_file
from services.profile_service import generate_profile
from services.cleaning_service import analyze_cleaning
from services.missing_value_service import handle_missing_values
from services.visualization_service import generate_visualizations
from services.insight_service import generate_insights
from services.duplicate_service import handle_duplicates


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "validation_report" not in st.session_state:
    st.session_state.validation_report = None

# Cleaning success message persistence ke liye
if "clean_success_msg" not in st.session_state:
    st.session_state.clean_success_msg = None

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 DataMind AI")
st.subheader("Your Intelligent Data Analysis Assistant")
st.write("Upload your dataset and let AI inspect it before analysis.")

# --------------------------------------------------
# File Upload & Validation
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    if st.session_state.df is None:
        validation_result = validate_file(uploaded_file)

        if validation_result["success"]:
            st.session_state.df = validation_result["dataframe"]
            st.session_state.validation_report = validation_result["report"]
            st.success(validation_result["message"])
        else:
            st.error(validation_result["message"])
            st.stop()
else:
    st.session_state.df = None
    st.session_state.validation_report = None
    st.session_state.clean_success_msg = None
    st.info("Please upload a CSV file to continue.")
    st.stop()

# --------------------------------------------------
# Continue only if DataFrame exists
# --------------------------------------------------
if st.session_state.df is not None:

    df = st.session_state.df

    # ==============================================
    # 1. Validation Report
    # ==============================================
    st.subheader("📋 Validation Report")
    st.write(st.session_state.validation_report)

    st.markdown("---")

    # ==============================================
    # 2. Dataset Profile
    # ==============================================
    profile_result = generate_profile(df)

    if profile_result["success"]:
        profile = profile_result["profile"]

        st.subheader("📈 Dataset Profile")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", profile["rows"])

        with col2:
            st.metric("Columns", profile["columns"])

        with col3:
            st.metric("Missing Values", profile.get("total_missing_values", 0))

        with col4:
            st.metric("Duplicate Rows", profile.get("total_duplicate_rows", 0))

    else:
        st.error(profile_result["message"])

    st.markdown("---")

    # ==============================================
    # 3. Dataset Preview
    # ==============================================
    st.subheader("👀 Dataset Preview")
    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.markdown("---")

    st.markdown("---")

    st.subheader("🗑 Duplicate Handling")

    duplicates = df.duplicated().sum()

    st.write(f"Duplicate Rows : {duplicates}")

    if duplicates > 0:
        method = st.selectbox(
            "Duplicate Handling Method",
            [
                "Keep First",
                "Drop All"
            ]
        )
        if st.button("Remove Duplicates"):
            result = handle_duplicates(
            st.session_state.df,
            method
        )

        if result["success"]:
            st.session_state.df = result["dataFrame"]
            st.success(result["message"])
            st.rerun()

        else:
            st.error(result["message"])

    else:

        st.success("No duplicate rows found.")

   









    # ==============================================
    # 4. Cleaning Recommendations & Action Section
    # ==============================================
    cleaning = analyze_cleaning(df)

    st.subheader("🧹 AI Cleaning Recommendations")

    if cleaning["success"]:
        # Column level analysis show karein
        for column, data in cleaning["report"].items():
            st.write(f"### {column}")
            st.write(f"**Missing Values :** {data['missing_values']}")
            st.write(f"**Missing Percentage :** {data['missing_percentage']}%")
            st.success(f"Recommended Method : {data['recommended_method']}")

        st.markdown("---")

        # Interactive Action Section
        missing_columns = list(cleaning["report"].keys())

        if len(missing_columns) > 0:
            
            # Action Section ke upar Green Success Banner
            if st.session_state.clean_success_msg:
                st.success(st.session_state.clean_success_msg)
                st.session_state.clean_success_msg = None

            st.subheader("🛠️ Take Action & Clean Data")

            selected_column = st.selectbox(
                "Select Column to Clean",
                missing_columns
            )

            recommendation = cleaning["report"][selected_column]["recommended_method"]

            st.info(f"AI Recommended Method : {recommendation}")

            method = st.selectbox(
                "Choose Cleaning Method",
                [
                    "Median",
                    "Mean",
                    "Mode",
                    "Forward Fill",
                    "Backward Fill",
                    "Drop Rows",
                    "Drop Column"
                ]
            )

            if st.button("Apply Cleaning"):
                clean_result = handle_missing_values(
                    st.session_state.df,
                    selected_column,
                    method
                )

                if clean_result["success"]:
                    st.session_state.df = clean_result["dataframe"]
                    st.session_state.clean_success_msg = f"✅ Success: Column **'{selected_column}'** has been successfully cleaned using **{method}**!"
                    st.toast(f"Column '{selected_column}' cleaned!", icon="✅")
                    st.rerun()
                else:
                    st.error(clean_result["message"])
        else:
            if st.session_state.clean_success_msg:
                st.success(st.session_state.clean_success_msg)
                st.session_state.clean_success_msg = None

            st.success("🎉 Dataset has no missing values.")

    st.markdown("---")

    # ==============================================
    # 5. Automatic Visualization Engine
    # ==============================================
    st.subheader("📊 Automatic Visualization Engine")

    visual_result = generate_visualizations(df)

    if not visual_result["success"]:
        st.error(visual_result["message"])

    st.markdown("---")

    # ==============================================
    # 6. AI Insights
    # ==============================================
    st.subheader("🧠 AI Insights")

    insight_result = generate_insights(df)

    if insight_result["success"]:
        for insight in insight_result["insights"]:
            st.info(insight)
    else:
        st.error(insight_result["message"])