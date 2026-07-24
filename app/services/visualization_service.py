import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def generate_visualizations(df: pd.DataFrame) -> dict:
    """
    Automatically generate charts
    for numerical columns.
    """

    try:

        if df is None or df.empty:

            return {
                "success": False,
                "message": "Empty DataFrame."
            }

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        

        if len(numeric_columns) == 0:

            return {
                "success": False,
                "message": "No numerical columns found."
            }
        categorical_columns = df.select_dtypes(include=["object", "string"]).columns


        if len(categorical_columns) == 0:

            return{
                "success":False,
                "message":  "No Categorical columns found. "
            }

        for column in numeric_columns:

            st.subheader(f"📊 {column}")

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.hist(
                df[column].dropna(),
                bins=20,
                edgecolor="black"
            )

            ax.set_title(f"{column} Distribution")

            ax.set_xlabel(column)

            ax.set_ylabel("Frequency")

            st.pyplot(fig)

            plt.close(fig)
        
            st.subheader(f"📦 {column} - Box Plot")

            fig, ax = plt.subplots(figsize=(8, 2))

            ax.boxplot(
            df[column].dropna(),
            vert=False
)

            ax.set_title(f"{column} Box Plot")

            st.pyplot(fig)

            plt.close(fig)

        for column in categorical_columns:

            st.subheader(f"📊 {column} - Bar Chart")

            counts = df[column].value_counts()

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.bar(
            counts.index,
            counts.values
    )

            ax.set_title(f"{column} Distribution")

            ax.set_xlabel(column)

            ax.set_ylabel("Count")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            plt.close(fig)

        return {

            "success": True,

            "message": "Visualizations generated successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }