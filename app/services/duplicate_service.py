import pandas as pd


def handle_duplicates(
    df: pd.DataFrame,
    method: str
):

    try:

        if df is None or df.empty:

            return {

                "success": False,

                "message": "Empty DataFrame.",

                "dataframe": None

            }

        cleaned_df = df.copy()

        if method == "Keep First":

            cleaned_df = cleaned_df.drop_duplicates(
                keep="first"
            )

        elif method == "Drop All":

            cleaned_df = cleaned_df.drop_duplicates(
                keep=False
            )

        else:

            return {

                "success": False,

                "message": "Invalid Method.",

                "dataframe": df

            }

        return {

            "success": True,

            "message": "Duplicates removed successfully.",

            "dataframe": cleaned_df

        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e),

            "dataframe": df

        }