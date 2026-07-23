import pandas as pd


def handle_missing_values(
    df: pd.DataFrame,
    column: str,
    method: str,
    custom_value=None
):
    """
    Apply the selected missing value handling method
    on a specific column and return a cleaned DataFrame.
    """

    try:

        if df is None or df.empty:

            return {
                "success": False,
                "message": "Empty DataFrame.",
                "dataframe": None
            }

        cleaned_df = df.copy()

        if method == "Mean":

            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].mean()
            )

        elif method == "Median":

            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].median()
            )

        elif method == "Mode":

            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].mode()[0]
            )

        elif method == "Forward Fill":

            cleaned_df[column] = cleaned_df[column].ffill()

        elif method == "Backward Fill":

            cleaned_df[column] = cleaned_df[column].bfill()

        elif method == "Custom":

            cleaned_df[column] = cleaned_df[column].fillna(
                custom_value
            )

        elif method == "Drop Rows":

            cleaned_df = cleaned_df.dropna(
                subset=[column]
            )

        elif method == "Drop Column":

            cleaned_df = cleaned_df.drop(
                columns=[column]
            )

        else:

            return {
                "success": False,
                "message": "Invalid cleaning method.",
                "dataframe": df
            }

        return {
            "success": True,
            "message": f"{column} cleaned successfully.",
            "dataframe": cleaned_df
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e),
            "dataframe": df
        }