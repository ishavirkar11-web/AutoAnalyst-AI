import pandas as pd


def load_data(file):

    if file is None:
        raise ValueError("No file was uploaded.")

    try:

        if file.name.lower().endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.lower().endswith(".xlsx"):
            df = pd.read_excel(file)

        else:
            raise ValueError(
                "Unsupported file format. Please upload CSV or Excel."
            )

    except Exception as e:

        raise ValueError(
            f"Could not read the uploaded file: {e}"
        )

    # Check empty dataset
    if df.empty:
        raise ValueError(
            "The uploaded dataset is empty."
        )

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Check again
    if df.shape[1] == 0:
        raise ValueError(
            "The dataset does not contain any usable columns."
        )

    return df