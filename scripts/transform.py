from pathlib import Path
import pandas as pd
def transform_data(ti = None):
    project_root = Path(__file__).resolve().parent.parent
    #input_file = project_root / "data" / "sales.csv"
    input_file = ti.xcom_pull(task_ids="validate_data", key="validated_file_path")

    output_file = project_root / "output" / "sales_processed.csv"

    row_count = ti.xcom_pull(task_ids="validate_data", key="row_count")

    print(f"Received from XCom: row_count = {row_count}")
    print(f"Transforming file: {input_file}")

    #read the downloaded file
    df = pd.read_csv(input_file)

    # Convert date column
    df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])

    # Convert text columns to uppercase
    df["Sales_Rep"] = df["Sales_Rep"].str.upper()
    df["Region"] = df["Region"].str.upper()
    df["Customer_Type"] = df["Customer_Type"].str.upper()
    df["Payment_Method"] = df["Payment_Method"].str.upper()
    df["Sales_Channel"] = df["Sales_Channel"].str.upper()

    # Calculate profit per unit
    df["Profit_Per_Unit"] = ( df["Unit_Price"] - df["Unit_Cost"] ).round(2)

    # Calculate total profit
    df["Total_Profit"] = ( df["Profit_Per_Unit"] * df["Quantity_Sold"] ).round(2)

    # Calculate discounted sales amount
    df["Discounted_Sales"] = ( df["Sales_Amount"] * (1 - df["Discount"]) ).round(2)

    # Add month and year columns
    df["Sale_Month"] = df["Sale_Date"].dt.month_name()
    df["Sale_Year"] = df["Sale_Date"].dt.year

    # Save output
    df.to_csv(output_file, index=False)
    print(f"Output written to: {output_file}")
    print(df.head())