import pandas as pd

def generate_profile(df:pd.DataFrame) -> dict:
    """
    Generate basic inforamtion about the dataset
    """

    profile = {
        "Rows": df.shape[0],
        "columns": df.shape[1],
        "Missing values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum(),
        "Memory usage(in kb)": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }
    return profile



