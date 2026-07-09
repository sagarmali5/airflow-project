from pathlib import Path
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import shutil

def download_from_s3(ti=None):
    bucket_name = "map-dev-s3-input"
    s3_key = "input/sales_data.csv"

    project_root = Path(__file__).resolve().parent.parent
    local_dir = project_root / "data"

    hook = S3Hook(aws_conn_id="aws_default")

    downloaded_file = hook.download_file(
        key=s3_key,
        bucket_name=bucket_name,
        local_path=str(local_dir) )

    # Final fixed filename
    final_file = local_dir / "sales.csv"

    # Replace old file with newly downloaded file
    shutil.copy(downloaded_file, final_file)

    ti.xcom_push(key="input_file_path", value=str(final_file))

    print(f"Downloaded file: {downloaded_file}")
    print(f"Copied to: {final_file}")









































