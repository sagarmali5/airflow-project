from pathlib import Path
import pandas as pd

# Define your expected columns here as a placeholder list
EXPECTED_COLUMNS = ["Product_ID",	"Sale_Date",	"Sales_Rep",	"Region",	"Sales_Amount",	"Quantity_Sold",
                    "Product_Category",	"Unit_Cost",	"Unit_Price",	"Customer_Type",	"Discount",
                    "Payment_Method",	"Sales_Channel",	"Region_and_Sales_Rep"
]


def validate_data(ti=None):
    # 1. Pull the input file path from the upstream S3 download task
    file_path = ti.xcom_pull(task_ids="download_from_s3", key="input_file_path")
    print(f"Validating file: {file_path}")

    # Load data
    df = pd.read_csv(file_path)

    # 2. Schema Validation (Column Check)
    actual_columns = df.columns.tolist()
    print(f"Actual columns in file: {actual_columns}")
    print(f"Expected columns: {EXPECTED_COLUMNS}")

    # Find any columns that are missing from the file
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in actual_columns]

    if missing_columns:
        error_msg = f"Validation Failed: Missing required columns: {missing_columns}"
        print(error_msg)
        # Raising an exception immediately fails the Airflow task and stops downstream execution
        raise ValueError(error_msg)

    print("Schema Validation Passed: All expected columns are present.")

    # 3. Print Data Insights
    row_count = df.shape[0]
    col_count = df.shape[1]

    print(f"Total Records / Number of rows: {row_count}")
    print(f"Number of columns: {col_count}")
    print("Null values in each column:\n", df.isnull().sum())

    # 4. Push Metadata to XCom (Fixed the set bug here)
    ti.xcom_push(key="row_count", value=row_count)
    print(f"XCom pushed: row_count = {row_count}")

    ti.xcom_push(key="validated_file_path", value=file_path)
    print(f"XCom pushed: validated_file_path = {file_path}")

    print("Validation Successful")