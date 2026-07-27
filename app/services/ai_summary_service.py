import pandas as pd

from services.outlier_service import analyze_outliers


def generate_ai_summary(
    df: pd.DataFrame
):

    try:

        if df is None or df.empty:

            return {

                "success": False,

                "summary": [],

                "recommendations": []

            }

        summary = []

        recommendations = []

        missing = int(df.isnull().sum().sum())

        if missing == 0:

            summary.append(
                "✅ No missing values detected."
            )

        else:

            summary.append(
                f"⚠ Dataset contains {missing} missing values."
            )

            recommendations.append(
                "Fill missing values using Median (numerical) and Mode (categorical)."
            )

        duplicates = int(
            df.duplicated().sum()
        )

        if duplicates == 0:

            summary.append(
                "✅ No duplicate rows detected."
            )

        else:

            summary.append(
                f"⚠ Dataset contains {duplicates} duplicate rows."
            )

            recommendations.append(
                "Remove duplicate records before modelling."
            )

        outlier_result = analyze_outliers(df)

        total_outliers = 0

        for data in outlier_result["report"].values():

            total_outliers += data["outliers"]

        if total_outliers == 0:

            summary.append(
                "✅ No significant outliers detected."
            )

        else:

            summary.append(
                f"⚠ {total_outliers} potential outliers detected."
            )

            recommendations.append(
                "Review or treat outliers before Machine Learning."
            )

        rows = len(df)

        if rows >= 1000:

            summary.append(
                "✅ Dataset size is sufficient for most ML tasks."
            )

        else:

            summary.append(
                "⚠ Dataset is relatively small."
            )

            recommendations.append(
                "Collect more records if possible."
            )

        numerical = len(
            df.select_dtypes(
                include="number"
            ).columns
        )

        categorical = len(
            df.select_dtypes(
                exclude="number"
            ).columns
        )

        summary.append(
            f"Dataset contains {numerical} numerical and {categorical} categorical columns."
        )

        if len(recommendations) == 0:

            recommendations.append(
                "Dataset looks clean and is ready for exploratory analysis and Machine Learning."
            )

        return {

            "success": True,

            "summary": summary,

            "recommendations": recommendations

        }

    except Exception as e:

        return {

            "success": False,

            "summary": [],

            "recommendations": [],

            "message": str(e)

        }