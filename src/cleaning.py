import pandas as pd


def remove_duplicates(df):
    """
    Remove duplicate rows from a DataFrame.
    """
    before = len(df)

    df = df.drop_duplicates().copy()

    after = len(df)

    removed = before - after

    print(f"Rows before removing duplicates: {before}")
    print(f"Duplicate rows removed: {removed}")
    print(f"Rows after removing duplicates: {after}")

    return df


def check_missing_values(df):
    """
    Check the number of missing values in each column.
    """
    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values found.")
    else:
        print("Missing values:")
        print(missing)

    return missing


def convert_date_columns(df):
    """
    Convert order date columns to Pandas datetime format.
    Invalid dates are converted to missing values.
    """
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    print("\nDate columns converted successfully.")

    return df


def standardize_column_names(df):
    """
    Standardize DataFrame column names.

    Rules:
    - Remove leading and trailing spaces
    - Convert to lowercase
    - Replace spaces with underscores
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\nColumn names standardized successfully.")

    return df


def clean_orders(df):
    """
    Apply all cleaning steps to the orders dataset.
    """
    print("Starting orders cleaning...")

    df = remove_duplicates(df)

    print("\nChecking missing values...")
    check_missing_values(df)

    df = convert_date_columns(df)

    df = standardize_column_names(df)

    print("\nOrders cleaning completed!")

    return df


def clean_basic_dataset(df):
    """
    Apply basic cleaning to datasets that do not
    require special processing.
    """

    df = df.copy()

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    # Standardize column names
    df = standardize_column_names(df)

    return df


def clean_geolocation(df):
    """
    Clean the geolocation dataset.
    """

    print("\nStarting geolocation cleaning...")

    before = len(df)

    df = df.drop_duplicates().copy()

    after = len(df)

    print(f"Rows before removing duplicates: {before}")
    print(f"Duplicate rows removed: {before - after}")
    print(f"Rows after removing duplicates: {after}")

    df = standardize_column_names(df)

    print("Geolocation cleaning completed!")

    return df


def clean_order_items(df):
    """
    Clean the order items dataset.
    """

    print("\nStarting order items cleaning...")

    df = df.drop_duplicates().copy()

    # Convert shipping limit date
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    df = standardize_column_names(df)

    print("Order items cleaning completed!")

    return df


def clean_reviews(df):
    """
    Clean the order reviews dataset.
    """

    print("\nStarting reviews cleaning...")

    df = df.drop_duplicates().copy()

    # Convert review dates
    df["review_creation_date"] = pd.to_datetime(
        df["review_creation_date"],
        errors="coerce"
    )

    df["review_answer_timestamp"] = pd.to_datetime(
        df["review_answer_timestamp"],
        errors="coerce"
    )

    df = standardize_column_names(df)

    print("Review cleaning completed!")

    return df


def clean_products(df):
    """
    Clean the products dataset.

    Missing product attributes are preserved because
    missing values may represent unavailable source data.
    """

    print("\nStarting products cleaning...")

    df = df.drop_duplicates().copy()

    df = standardize_column_names(df)

    print("Missing product values:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    print("Product cleaning completed!")

    return df