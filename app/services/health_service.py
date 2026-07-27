import pandas as pd

from services.outlier_service import analyze_outliers

def calculate_health_score(
        df: pd.DataFrame
):
    try:
        if df is None or df.empty:
            return{
                "success" : False,
                "score":0,
                "grade":"poor",
                "summary": "Dataset is empty."
            }

        score = 100
        missing = int(df.isnull().sum().sum())
        if missing > 0:
            score -= 30
        duplicates = int(df.duplicated().sum())

        if duplicates > 0:
            score -= 20
        outlier_result = analyze_outliers(df)

        total_outliers = 0

        for info in outlier_result["report"].values():
            total_outliers += info["outliers"]
        if total_outliers > 0:
            score -= 20
        for column in df.columns:
            missing_percent = (
                df[column].isnull().sum()
                /
                len(df)

            ) * 100

            if missing_percent > 80:
                score -= 20
                break

        score = max(score,0)

        if score >=90:
            grade = "Excellent"
        elif score >= 75:
            grade = "Good"
        elif score >=50:
            grade = "Average"
        else:
            grade = "Poor"
        return {
            "success":True,
            "score":score,
            "grade":grade
        }
    except Exception as e:
        return{
            "success": False,
            "message": str(e),
            "score":0,
            "grade": "Poor"
        }
