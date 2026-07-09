from pathlib import Path
import pandas as pd


def validate_data(ti = None):

    #project_root = Path(__file__).resolve().parent.parent

    file_path = ti.xcom_pull( task_ids="download_from_s3", key="input_file_path" )

    print(f"Validating file: {file_path}")

    df = pd.read_csv(file_path)

    print(df)

    print(f"Total Records: {len(df)}")

    print("number of rows: ", df.shape[0])

    ti.xcom_push(key="row_count", value={len(df)})
    print(f"XCom pushed: row_count = {len(df)}")

    ti.xcom_push(key="validated_file_path", value=file_path)

    print("number of columns: ", df.shape[1])

    print("column names: ", df.columns.tolist())

    print("Null values in each columns: ", df.isnull().sum())

    print("Validation Successful")