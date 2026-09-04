from pathlib import Path
import pandas as pd


PROCESSED_DATA_PATH = Path("data/processed")


def check_file_exists(file_name):
    """
    Check whether a processed dataset exists.
    """

    file_path = PROCESSED_DATA_PATH / file_name

    if file_path.exists():
        print(f"PASS: {file_name} exists")
        return True

    print(f"FAIL: {file_name} is missing")
    return False


def check_required_columns(file_name, required_columns):
    """
    Check whether a dataset contains all required columns.
    """

    file_path = PROCESSED_DATA_PATH / file_name
    df = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if not missing_columns:
        print(f"PASS: Required columns present in {file_name}")
        return True

    print(
        f"FAIL: Missing columns in {file_name}: "
        f"{missing_columns}"
    )
    return False


def check_missing_ids(file_name, id_column):
    """
    Check whether an important ID column contains missing values.
    """

    file_path = PROCESSED_DATA_PATH / file_name
    df = pd.read_csv(file_path)

    missing_count = df[id_column].isnull().sum()

    if missing_count == 0:
        print(f"PASS: No missing {id_column} in {file_name}")
        return True

    print(
        f"FAIL: {missing_count} missing {id_column} "
        f"in {file_name}"
    )
    return False


def check_non_negative_values(file_name, columns):
    """
    Check that specified numeric columns do not contain
    negative values.
    """

    file_path = PROCESSED_DATA_PATH / file_name
    df = pd.read_csv(file_path)

    passed = True

    for column in columns:

        negative_count = (df[column] < 0).sum()

        if negative_count == 0:
            print(
                f"PASS: No negative values in "
                f"{file_name} -> {column}"
            )
        else:
            print(
                f"FAIL: {negative_count} negative values in "
                f"{file_name} -> {column}"
            )
            passed = False

    return passed


def check_duplicate_rows(file_name):
    """
    Check for completely duplicated rows.
    """

    file_path = PROCESSED_DATA_PATH / file_name
    df = pd.read_csv(file_path)

    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:
        print(f"PASS: No duplicate rows in {file_name}")
        return True

    print(
        f"FAIL: {duplicate_count} duplicate rows "
        f"in {file_name}"
    )
    return False


print("=" * 70)
print("INSIGHTFLOW FINAL DATA VALIDATION")
print("=" * 70)


# --------------------------------------------------
# 1. Check processed files
# --------------------------------------------------

processed_files = [
    "orders_processed.csv",
    "customers_processed.csv",
    "geolocation_processed.csv",
    "order_items_processed.csv",
    "payments_processed.csv",
    "reviews_processed.csv",
    "products_processed.csv",
    "sellers_processed.csv",
    "category_translation_processed.csv"
]

print("\n1. CHECKING PROCESSED FILES")

for file_name in processed_files:
    check_file_exists(file_name)


# --------------------------------------------------
# 2. Required columns
# --------------------------------------------------

print("\n2. CHECKING REQUIRED COLUMNS")

check_required_columns(
    "orders_processed.csv",
    [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp"
    ]
)

check_required_columns(
    "customers_processed.csv",
    [
        "customer_id",
        "customer_unique_id"
    ]
)

check_required_columns(
    "order_items_processed.csv",
    [
        "order_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value"
    ]
)

check_required_columns(
    "payments_processed.csv",
    [
        "order_id",
        "payment_type",
        "payment_value"
    ]
)

check_required_columns(
    "products_processed.csv",
    [
        "product_id",
        "product_category_name"
    ]
)


# --------------------------------------------------
# 3. Important ID validation
# --------------------------------------------------

print("\n3. CHECKING IMPORTANT IDs")

check_missing_ids(
    "orders_processed.csv",
    "order_id"
)

check_missing_ids(
    "customers_processed.csv",
    "customer_id"
)

check_missing_ids(
    "order_items_processed.csv",
    "order_id"
)

check_missing_ids(
    "products_processed.csv",
    "product_id"
)

check_missing_ids(
    "sellers_processed.csv",
    "seller_id"
)


# --------------------------------------------------
# 4. Numeric value validation
# --------------------------------------------------

print("\n4. CHECKING NUMERIC VALUES")

check_non_negative_values(
    "order_items_processed.csv",
    [
        "price",
        "freight_value"
    ]
)

check_non_negative_values(
    "payments_processed.csv",
    [
        "payment_value",
        "payment_installments"
    ]
)


# --------------------------------------------------
# 5. Duplicate validation
# --------------------------------------------------

print("\n5. CHECKING DUPLICATES")

for file_name in processed_files:
    check_duplicate_rows(file_name)


print("\n" + "=" * 70)
print("FINAL DATA VALIDATION COMPLETED")
print("=" * 70)