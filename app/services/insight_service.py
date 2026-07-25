import pandas as pd

def generate_insights(df: pd.DataFrame) -> dict:
    """Generate Automatic Insights"""

    try:
        if df is None or df.empty:
            return {
                "success": False,  # Boolean False
                "message": "Empty Dataframe",
                "insights": []
            }

        # 1. FIX: Changed {} to [] (List banaya)
        insights = []

        rows = df.shape[0]
        columns = df.shape[1]
        insights.append(
            f"Dataset contains {rows:,} rows and {columns} columns."
        )

        missing = int(df.isnull().sum().sum())
        if missing > 0:
            insights.append(
                f"Dataset contains {missing:,} missing values."
            )
        else:
            insights.append(
                "Dataset has no missing values."
            )
        
        # 2. FIX: Added () in df.duplicated()
        duplicates = int(df.duplicated().sum())

        if duplicates > 0:
            insights.append(
                f"Dataset contains {duplicates} duplicate rows."
            )
        else:
            insights.append(
                "No Duplicate rows Detected."
            )

        num_cols = len(df.select_dtypes(include="number").columns)
        cat_cols = len(df.select_dtypes(exclude="number").columns)

        insights.append(f"Numerical Columns : {num_cols}")
        insights.append(f"Categorical Columns : {cat_cols}")

        return {
            "success": True,  # Boolean True
            "insights": insights
        }

    except Exception as e:
        return {
            "success": False,  # Boolean False
            "message": str(e),
            "insights": []
        }