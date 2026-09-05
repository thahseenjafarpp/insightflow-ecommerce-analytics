from pathlib import Path

import pandas as pd


def calculate_delivery_time(df):
    """
    Calculate delivery time in days.

    Delivery time is the difference between
    customer delivery date and purchase timestamp.
    """

    df = df.copy()

    df["delivery_time_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 60 * 60)

    print("\nDelivery time calculated successfully.")

    return df


def create_purchase_time_features(df):
    """
    Create time-based features from the order purchase timestamp.
    """

    df = df.copy()

    df["purchase_year"] = (
        df["order_purchase_timestamp"].dt.year
    )

    df["purchase_month"] = (
        df["order_purchase_timestamp"].dt.month
    )

    df["purchase_month_name"] = (
        df["order_purchase_timestamp"].dt.month_name()
    )

    df["purchase_day_of_week"] = (
        df["order_purchase_timestamp"].dt.day_name()
    )

    print("\nPurchase time features created successfully.")

    return df


def transform_orders(df):
    """
    Apply all transformations to the orders dataset.
    """

    print("\nStarting orders transformation...")

    df = calculate_delivery_time(df)
    df = create_purchase_time_features(df)

    print("\nOrders transformation completed!")

    return df


def save_processed_data(df, file_name):
    """
    Save a processed DataFrame to the processed data directory.
    """

    output_path = Path("data/processed")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / file_name

    df.to_csv(file_path, index=False)

    print(f"\nProcessed data saved to: {file_path}")

    return file_path


