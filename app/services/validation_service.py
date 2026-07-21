import csv
import io
import pandas as pd


def validate_file(uploaded_file):
    """
    Validate uploaded CSV file before analysis.

    Returns
    -------
    dict
        {
            success: bool,
            message: str,
            dataframe: DataFrame | None,
            report: dict
        }
    """

    report = {
        "File Uploaded": False,
        "CSV Format": False,
        "File Size": False,
        "Encoding": "Unknown",
        "Delimiter": "Unknown",
        "Dataset Loaded": False,
        "Missing Values": 0,
        "Duplicate Rows": 0,
        "Ready For Analysis": False
    }

    # ----------------------------------------------------
    # 1. File Uploaded
    # ----------------------------------------------------

    if uploaded_file is None:

        return {
            "success": False,
            "message": "Please upload a CSV file.",
            "dataframe": None,
            "report": report
        }

    report["File Uploaded"] = True

    # ----------------------------------------------------
    # 2. File Extension
    # ----------------------------------------------------

    if not uploaded_file.name.lower().endswith(".csv"):

        return {
            "success": False,
            "message": "Only CSV files are supported.",
            "dataframe": None,
            "report": report
        }

    report["CSV Format"] = True

    # ----------------------------------------------------
    # 3. File Size
    # ----------------------------------------------------

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > 100:

        return {
            "success": False,
            "message": f"Large file detected ({file_size_mb:.2f} MB). Maximum supported size is 100 MB in Version 1.",
            "dataframe": None,
            "report": report
        }

    report["File Size"] = True

    # ----------------------------------------------------
    # 4. Read Bytes
    # ----------------------------------------------------

    file_bytes = uploaded_file.getvalue()

    # ----------------------------------------------------
    # 5. Encoding Detection
    # ----------------------------------------------------

    encodings = [
        "utf-8",
        "utf-16",
        "latin-1",
        "cp1252"
    ]

    decoded_text = None

    for encoding in encodings:

        try:

            decoded_text = file_bytes.decode(encoding)

            report["Encoding"] = encoding

            break

        except UnicodeDecodeError:

            continue

    if decoded_text is None:

        return {
            "success": False,
            "message": "Unable to detect file encoding.",
            "dataframe": None,
            "report": report
        }

    # ----------------------------------------------------
    # 6. Delimiter Detection
    # ----------------------------------------------------

    try:

        sample = decoded_text[:5000]

        dialect = csv.Sniffer().sniff(sample)

        delimiter = dialect.delimiter

    except Exception:

        delimiter = ","

    report["Delimiter"] = delimiter

    # ----------------------------------------------------
    # 7. Load Dataset
    # ----------------------------------------------------

    try:

        df = pd.read_csv(
            io.StringIO(decoded_text),
            delimiter=delimiter
        )

    except Exception as e:

        return {

            "success": False,

            "message": f"Unable to read CSV : {e}",

            "dataframe": None,

            "report": report
        }

    report["Dataset Loaded"] = True

    # ----------------------------------------------------
    # 8. Dataset Validation
    # ----------------------------------------------------

    report["Missing Values"] = int(
        df.isnull().sum().sum()
    )

    report["Duplicate Rows"] = int(
        df.duplicated().sum()
    )

    report["Ready For Analysis"] = True

    # ----------------------------------------------------
    # Final Result
    # ----------------------------------------------------

    return {

        "success": True,

        "message": "Dataset validated successfully.",

        "dataframe": df,

        "report": report
    }