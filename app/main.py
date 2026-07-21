import pandas as pd
import streamlit as st
from services.profile_service import generate_profile
from services.validation_service import validate_file

st.set_page_config(page_title="DataMind AI", page_icon="📊", layout="wide")


def render_validation_report(report: dict):
    """Render validation report dictionary as clean, UI-friendly status items."""
    # Boolean Status Checks
    boolean_checks = [
        ("File Uploaded", "File Uploaded"),
        ("CSV Format", "CSV Format"),
        ("Dataset Loaded", "Dataset Loaded"),
        ("Ready For Analysis", "Ready For Analysis"),
    ]

    # Display Boolean Checks
    for key, label in boolean_checks:
        if report.get(key):
            st.success(f"✅ **{label}**")
        else:
            st.error(f"❌ **{label} Failed**")

    # Display Text Attributes (Encoding & Delimiter)
    if report.get("Encoding") != "Unknown":
        st.info(f"ℹ️ **Encoding Detected:** `{report['Encoding'].upper()}`")

    if report.get("Delimiter") != "Unknown":
        delim_display = "Comma (,)" if report['Delimiter'] == ',' else report['Delimiter']
        st.info(f"ℹ️ **Delimiter Identified:** `{delim_display}`")

    # Display Missing Values Warning
    missing_count = report.get("Missing Values", 0)
    if missing_count > 0:
        st.warning(f"⚠️ **Missing Values Found:** {missing_count:,}")
    else:
        st.success("✅ **No Missing Values Found**")

    # Display Duplicates Warning
    dup_count = report.get("Duplicate Rows", 0)
    if dup_count > 0:
        st.warning(f"⚠️ **Duplicate Rows Found:** {dup_count:,}")
    else:
        st.success("✅ **No Duplicate Rows Found**")


# ----------------------------------------------------
# Main Streamlit App UI
# ----------------------------------------------------
st.title("📊 DataMind AI")
st.subheader("Your Intelligent Data Analysis Assistant")
st.write("Welcome! Upload your dataset to begin intelligent analysis.")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

result = validate_file(uploaded_file)

if not result["success"]:
    if uploaded_file is not None:
        st.error(result["message"])

else:
    st.success(result["message"])
    df = result["dataframe"]

    # ----------------------------------------------------
    # 1. Professional Validation Report Section
    # ----------------------------------------------------
    st.subheader("📋 Validation Report")

    # Replacing st.json() with custom visual component
    render_validation_report(result["report"])

    st.markdown("---")

    # ----------------------------------------------------
    # 2. Dataset Profile Section
    # ----------------------------------------------------
    st.subheader("📈 Dataset Profile")
    profile_res = generate_profile(df)

    if profile_res["success"]:
        prof = profile_res["profile"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Rows", value=f"{prof['rows']:,}")
        with col2:
            st.metric(label="Total Columns", value=prof["columns"])
        with col3:
            st.metric(label="Numerical Columns", value=prof["numerical_summary"]["count"])
        with col4:
            st.metric(label="Categorical Columns", value=prof["categorical_summary"]["count"])

        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric(
                label="Missing Values",
                value=prof["total_missing_values"],
                delta="Clean Data" if prof["total_missing_values"] == 0 else f"{prof['total_missing_values']} Issues",
                delta_color="normal" if prof["total_missing_values"] == 0 else "inverse",
            )
        with col6:
            st.metric(
                label="Duplicate Rows",
                value=prof["total_duplicate_rows"],
                delta="No Duplicates" if prof["total_duplicate_rows"] == 0 else f"{prof['total_duplicate_rows']} Duplicates",
                delta_color="normal" if prof["total_duplicate_rows"] == 0 else "inverse",
            )
        with col7:
            id_count = len(prof.get("potential_id_columns", []))
            st.metric(
                label="Potential ID Columns",
                value=id_count,
                help="Columns that look like IDs/Keys rather than continuous numbers.",
            )

    st.markdown("---")

    # ----------------------------------------------------
    # 3. Dataset Preview Section
    # ----------------------------------------------------
    st.subheader("👀 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)