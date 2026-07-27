import pandas as pd
import io


def dataframe_to_csv(
    df: pd.DataFrame
):

    if df is None or df.empty:

        return None

    csv = df.to_csv(
        index=False
    )

    return csv


def dataframe_to_excel(
    df: pd.DataFrame
):

    if df is None or df.empty:

        return None

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Clean_Data"
        )

    return output.getvalue()