from pathlib import Path
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def upload_to_s3():
    bucket_name = "map-dev-s3-output"
    s3_key = "output/sales_processed.csv"

    project_root = Path(__file__).resolve().parent.parent
    local_file = project_root / "output" / "sales_processed.csv"

    hook = S3Hook(aws_conn_id="aws_default")

    hook.load_file(
        filename=str(local_file),
        key=s3_key,
        bucket_name=bucket_name,
        replace=True )

    print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")