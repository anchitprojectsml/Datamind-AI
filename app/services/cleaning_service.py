import pandas as pd


def analyze_cleaning(df: pd.DataFrame) -> dict:
    """
    Analyze the dataset and generate cleaning recommendations.
    """

    try:

        if df is None or df.empty:

            return {
                "success": False,
                "message": "Empty DataFrame.",
                "report": {}
            }

        report = {}

        missing = df.isnull().sum()

        for column in df.columns:

            missing_count = int(missing[column])

            if missing_count == 0:
                continue

            missing_percent = round(
                (missing_count / len(df)) * 100,
                2
            )

            if pd.api.types.is_numeric_dtype(df[column]):

                recommendation = "Median"

            else:

                recommendation = "Mode"

            report[column] = {

                "missing_values": missing_count,

                "missing_percentage": missing_percent,

                "recommended_method": recommendation

            }

        return {

            "success": True,

            "report": report

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e),

            "report": {}

        }
     