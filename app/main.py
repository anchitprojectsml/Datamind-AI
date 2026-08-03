import streamlit as st

from services.validation_service import validate_file
from services.profile_service import generate_profile
from services.cleaning_service import analyze_cleaning
from services.missing_value_service import handle_missing_values
from services.visualization_service import generate_visualizations
from services.insight_service import generate_insights
from services.duplicate_service import handle_duplicates
from services.outlier_service import analyze_outliers
from services.download_service import (
    dataframe_to_csv,
    dataframe_to_excel
)
from services.health_service import calculate_health_score
from services.ai_summary_service import generate_ai_summary
from services.pdf_report_service import generate_pdf_report


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

if "clean_success_msg" not in st.session_state:
    st.session_state.clean_success_msg = None

# --------------------------------------------------
# Title & Platform Branding
# --------------------------------------------------
st.title("📊 DataMind AI")
st.subheader("Your Intelligent Data Analysis Assistant")
st.write("Upload your dataset and let AI inspect it before analysis.")

st.info(
    "🚀 AI-powered Data Analysis Platform | Validate • Clean • Visualize • Generate Insights"
)

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
# Main Dashboard Logic (Triggers when Data is Loaded)
# --------------------------------------------------
if st.session_state.df is not None:

    df = st.session_state.df

    # ==============================================
    # 1. Validation Report
    # ==============================================
    st.subheader("📋 Validation Report")
    st.caption("Verify file integrity before analysis.")
    report = st.session_state.validation_report

    st.success("Dataset validation completed successfully.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "File Uploaded",
            "✅ Valid" if report.get("File Uploaded") else "❌ Invalid"
        )
        st.metric(
            "CSV Format",
            "✅ Valid CSV" if report.get("CSV Format") else "❌ Invalid Format"
        )
        st.metric(
            "File Size",
            "✅ Within Limit" if report.get("File Size") else "❌ Exceeds Limit"
        )
        st.metric(
            "Dataset Loaded",
            "✅ Successfully Loaded" if report.get("Dataset Loaded") else "❌ Error Loading"
        )

    with col2:
        st.metric(
            "Encoding",
            report.get("Encoding", "UTF-8")
        )
        st.metric(
            "Delimiter",
            f"'{report.get('Delimiter', ',')}'"
        )
        st.metric(
            "Missing Values Status",
            "⚠️ Detected" if report.get("Missing Values", 0) > 0 else "✅ None"
        )
        st.metric(
            "Duplicate Rows Status",
            "⚠️ Detected" if report.get("Duplicate Rows", 0) > 0 else "✅ None"
        )

    st.caption("All validation checks completed before profiling and AI analysis.")
    st.markdown("---")

    # ==============================================
    # 2. Dataset Profile
    # ==============================================
    profile = {}
    profile_result = generate_profile(df)

    if profile_result["success"]:
        profile = profile_result["profile"]

        st.subheader("📈 Dataset Profile")
        st.caption("Quick overview of your uploaded dataset.")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", profile.get("rows", 0))

        with col2:
            st.metric("Columns", profile.get("columns", 0))

        with col3:
            st.metric("Missing Values", profile.get("total_missing_values", 0))

        with col4:
            st.metric("Duplicate Rows", profile.get("total_duplicate_rows", 0))
    else:
        st.error(profile_result["message"])

    st.markdown("---")

    # ==============================================
    # 3. Dataset Health Score
    # ==============================================
    health = calculate_health_score(df)
    if health["success"]:
        st.subheader("🏥 Dataset Health Score")
        st.caption("Overall quality assessment of the dataset.")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Health Score",
                f"{health['score']}/100"
            )

        with col2:
            st.metric(
                "Grade",
                health["grade"]
            )

    st.markdown("---")

    # ==============================================
    # 4. 🤖 AI Consultant Summary & Recommendations (Shifted to Top Level)
    # ==============================================
    summary_result = generate_ai_summary(df)

    if summary_result["success"]:
        st.subheader("🤖 AI Consultant Summary")
        st.caption("Automatically generated insights and recommendations.")

        st.write("### Key Findings")
        for item in summary_result["summary"]:
            st.write(item)

        st.markdown("---")

        st.write("### AI Recommendations")
        for index, item in enumerate(summary_result["recommendations"], start=1):
            st.info(f"{index}. {item}")

    st.markdown("---")

    # ==============================================
    # 5. Dataset Preview
    # ==============================================
    st.subheader("👀 Dataset Preview")
    st.caption("First five rows of the current dataset.")
    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.markdown("---")

    # ==============================================
    # 6. 🧹 Data Cleaning Center (Grouped Together)
    # ==============================================
    st.subheader("🧹 Data Cleaning Center")
    st.caption("Resolve duplicates and missing values to improve dataset health.")

    tab1, tab2 = st.tabs(["🗑️ Duplicate Handling", "🛠️ Missing Value Imputation"])

    # --- TAB 1: Duplicate Handling ---
    with tab1:
        duplicates = df.duplicated().sum()
        st.write(f"**Duplicate Rows Detected:** {duplicates}")

        if duplicates > 0:
            method = st.selectbox(
                "Select Duplicate Handling Method",
                ["Keep First", "Drop All"]
            )
            if st.button("Remove Duplicates"):
                result = handle_duplicates(st.session_state.df, method)

                if result["success"]:
                    st.session_state.df = result["dataFrame"]
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
        else:
            st.success("✅ No duplicate rows found in dataset.")

    # --- TAB 2: Missing Value Cleaning ---
    with tab2:
        cleaning = analyze_cleaning(df)

        if cleaning["success"]:
            missing_columns = list(cleaning["report"].keys())

            if len(missing_columns) > 0:
                for column, data in cleaning["report"].items():
                    st.write(f"**Column:** `{column}` | **Missing:** {data['missing_values']} ({data['missing_percentage']}%)")
                    st.caption(f"Suggested Action: {data['recommended_method']}")

                st.markdown("---")

                if st.session_state.clean_success_msg:
                    st.success(st.session_state.clean_success_msg)
                    st.session_state.clean_success_msg = None

                selected_column = st.selectbox(
                    "Select Column to Clean",
                    missing_columns
                )

                recommendation = cleaning["report"][selected_column]["recommended_method"]
                st.info(f"AI Recommended Method for '{selected_column}': **{recommendation}**")

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

                if st.button("Apply Cleaning Method"):
                    clean_result = handle_missing_values(
                        st.session_state.df,
                        selected_column,
                        method
                    )

                    if clean_result["success"]:
                        st.session_state.df = clean_result["dataframe"]
                        st.session_state.clean_success_msg = f"✅ Success: Column **'{selected_column}'** cleaned using **{method}**!"
                        st.toast(f"Column '{selected_column}' cleaned!", icon="✅")
                        st.rerun()
                    else:
                        st.error(clean_result["message"])
            else:
                if st.session_state.clean_success_msg:
                    st.success(st.session_state.clean_success_msg)
                    st.session_state.clean_success_msg = None

                st.success("🎉 Excellent! Dataset has no missing values.")

    st.markdown("---")

    # ==============================================
    # 7. Outlier Detection
    # ==============================================
    st.subheader("📈 Outlier Detection")
    st.caption("Identify extreme values across numerical variables.")
    outlier_result = analyze_outliers(st.session_state.df)

    if outlier_result["success"]:
        has_outliers = False
        for column, info in outlier_result["report"].items():
            st.write(f"### {column}")
            st.write(f"Outliers: {info['outliers']}")
            st.write(f"Lower Bound: {info['lower_bound']}")
            st.write(f"Upper Bound: {info['upper_bound']}")
            if info["outliers"] > 0:
                has_outliers = True

        if has_outliers:
            st.warning("⚠️ Outliers Detected")
            st.info("AI Recommendation: Review these values before training ML models.")
        else:
            st.success("✅ No Outliers Found.")

    st.markdown("---")

    # ==============================================
    # 8. Automatic Visualization Engine
    # ==============================================
    st.subheader("📊 Automatic Visualization Engine")
    st.caption("Automatic charts generated from your dataset.")
    visual_result = generate_visualizations(df)

    if not visual_result["success"]:
        st.error(visual_result["message"])

    st.markdown("---")

    # ==============================================
    # 9. AI Insights
    # ==============================================
    st.subheader("🧠 Deep AI Insights")
    st.caption("In-depth statistical patterns and data relationships.")
    insight_result = generate_insights(df)

    if insight_result["success"]:
        for insight in insight_result["insights"]:
            st.info(insight)
    else:
        st.error(insight_result["message"])

    st.markdown("---")

    # ==============================================
    # 10. Downloads Section (Clean Data & PDF Report)
    # ==============================================
    st.subheader("📥 Export Clean Data & Executive PDF")
    st.caption("Download your processed dataset and generated PDF summary report.")

    csv_file = dataframe_to_csv(st.session_state.df)
    excel_file = dataframe_to_excel(st.session_state.df)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download Clean CSV",
            data=csv_file,
            file_name="clean_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="📊 Download Clean Excel",
            data=excel_file,
            file_name="clean_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.markdown("### 📄 Full Executive PDF Report")

    pdf_buffer = generate_pdf_report(
        profile=profile,
        health=health,
        summary_result=summary_result,
        dataset_name=uploaded_file.name
    )

    if pdf_buffer:
        st.download_button(
            label="📥 Download Executive PDF Report",
            data=pdf_buffer,
            file_name="DataMind_AI_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("---")
    st.caption("DataMind AI • Version 1.0.0 • Built with Streamlit & Python")