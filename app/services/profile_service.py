import pandas as pd


def generate_profile(df: pd.DataFrame) -> dict:
    """
    Generate dataset profile.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
    """
    try:
        # Base validation check
        if df is None or df.empty:
            return {
                "success": False,
                "message": "DataFrame is empty or None.",
                "profile": {}
            }

        profile = {}

        # 1. Dimensions (Rows & Columns)
        profile["rows"] = df.shape[0]
        profile["columns"] = df.shape[1]

        # 2. Missing Values & Duplicate Rows (Added () after methods)
        profile["total_missing_value"] = int(df.isnull().sum().sum())
        profile["total_duplicated_rows"] = int(df.duplicated().sum())

        # 3. Numerical Summary
        numerical_cols = df.select_dtypes(include="number").columns
        profile["numerical_summary"] = {
            "count": len(numerical_cols),  # Fixed: colon (:) instead of =
            "columns": list(numerical_cols)
        }

        # 4. Categorical Summary
        categorical_cols = df.select_dtypes(exclude="number").columns
        profile["categorical_summary"] = {
            "count": len(categorical_cols),
            "columns": list(categorical_cols)
        }

        # 5. Memory Usage Calculation
        memory = df.memory_usage(deep=True).sum()
        profile["memory_usage_kb"] = round(memory / 1024, 2)

        # 6. Potential ID Columns Identification
        potential_ids = []
        for col in df.columns:
            if "id" in col.lower():
                potential_ids.append(col)

        profile["potential_id_columns"] = potential_ids

        # 7. Final Success Return (Outside the loop)
        return {
            "success": True,
            "profile": profile
        }

    except Exception as e:
        # Error handling block
        return {
            "success": False,
            "message": str(e),
            "profile": {}
        }