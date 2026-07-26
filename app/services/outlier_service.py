import pandas as pd


def analyze_outliers(
    df: pd.DataFrame
):

    try:

        if df is None or df.empty:

            return {

                "success": False,

                "message": "Empty DataFrame.",

                "report": {}

            }

        report = {}

        numerical_columns = df.select_dtypes(
            include="number"
        ).columns

        for column in numerical_columns:

            data = df[column].dropna()

            q1 = data.quantile(0.25)

            q3 = data.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)

            upper_bound = q3 + (1.5 * iqr)

            outliers = data[
                (data < lower_bound)
                |
                (data > upper_bound)
            ]

            report[column] = {

                "outliers": len(outliers),

                "lower_bound": round(lower_bound,2),

                "upper_bound": round(upper_bound,2)

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