import pandas as pd


def validate_required_columns(df, required_columns):
    """
    Check whether all required columns exist.
    """
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Validation failed!")
        print("Missing columns:", missing_columns)
        return False

    print("Required columns validation passed.")
    return True


def validate_order_id(df):
    """
    Validate the order_id column.
    Checks for missing and duplicate order IDs.
    """

    missing_ids = df["order_id"].isnull().sum()
    duplicate_ids = df["order_id"].duplicated().sum()

    print("\nOrder ID validation:")

    print(f"Missing order IDs: {missing_ids}")
    print(f"Duplicate order IDs: {duplicate_ids}")

    if missing_ids == 0 and duplicate_ids == 0:
        print("Order ID validation passed.")
        return True

    print("Order ID validation failed.")
    return False


def validate_order_status(df):
    """
    Validate order status values.
    """

    valid_statuses = {
        "delivered",
        "shipped",
        "canceled",
        "unavailable",
        "invoiced",
        "processing",
        "created",
        "approved"
    }

    actual_statuses = set(df["order_status"].dropna().unique())

    invalid_statuses = actual_statuses - valid_statuses

    print("\nOrder status validation:")

    print("Statuses found:", sorted(actual_statuses))

    if invalid_statuses:
        print("Invalid statuses found:", sorted(invalid_statuses))
        print("Order status validation failed.")
        return False

    print("Order status validation passed.")
    return True


def validate_order_dates(df):
    """
    Validate the logical order of purchase and delivery dates.
    """

    invalid_delivery_dates = (
        df["order_delivered_customer_date"].notna()
        & (
            df["order_delivered_customer_date"]
            < df["order_purchase_timestamp"]
        )
    )

    invalid_count = invalid_delivery_dates.sum()

    print("\nOrder date validation:")
    print(f"Invalid delivery dates: {invalid_count}")

    if invalid_count == 0:
        print("Order date validation passed.")
        return True

    print("Order date validation failed.")
    return False