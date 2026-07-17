from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from airflow.providers.amazon.aws.operators.sns import SnsPublishOperator

from airflow_project.scripts.validate import validate_data
from airflow_project.scripts.transform import transform_data
from airflow_project.scripts.download import download_from_s3
from airflow_project.scripts.upload import upload_to_s3
from airflow_project.utils.sns_alerts import failure_alert



def start():
    print("Pipeline Started")

def end():
    print("Pipeline Finished")

with DAG(
        dag_id="first_airflow_dag",
        start_date=datetime(2025, 1, 1),
        schedule=None,
        catchup=False,
        tags=["learning", "etl"], )as dag:

    notify_start = SnsPublishOperator(
        task_id="notify_pipeline_start",
        target_arn="arn:aws:sns:ap-south-1:762038223499:etl-alerts",
        subject="ETL Pipeline Started",
        message="Sales ETL pipeline has started processing.",
        aws_conn_id="aws_default" )

    download_task = PythonOperator(
        task_id="download_from_s3",
        python_callable=download_from_s3)

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
        on_failure_callback=failure_alert)

    '''
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data )
    '''

    spark_task = BashOperator( task_id="spark_transform",
                               bash_command=""" export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && 
                               export PATH=$JAVA_HOME/bin:$PATH && 
                               export PYTHONPATH="/mnt/c/Users/ASUS/DBDA Python/airflow:$PYTHONPATH" && 
                               /home/sagar/airflow-project/.venv/bin/spark-submit "/mnt/c/Users/ASUS/DBDA Python/airflow/airflow_project/spark_jobs/spark_transform.py" """,
                               on_failure_callback=failure_alert)


    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3)

    notify_success = SnsPublishOperator(
        task_id="notify_pipeline_success",
        target_arn="arn:aws:sns:ap-south-1:762038223499:etl-alerts",
        subject="ETL Pipeline Completed",
        message="Sales ETL completed successfully. "
                "Processed records and output file were generated successfully.",
        aws_conn_id="aws_default" )

    notify_start >> download_task >> validate_task >> spark_task >> upload_task >> notify_success