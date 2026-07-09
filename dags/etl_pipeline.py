from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow_project.scripts.validate import validate_data
from airflow_project.scripts.transform import transform_data
from airflow_project.scripts.download import download_from_s3
from airflow_project.scripts.upload import upload_to_s3
from airflow.operators.bash import BashOperator


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

    start_task = PythonOperator(
        task_id="start",
        python_callable=start)

    download_task = PythonOperator(
        task_id="download_from_s3",
        python_callable=download_from_s3)

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data )

    '''
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data )
    '''

    spark_task = BashOperator( task_id="spark_transform",
                               bash_command=""" export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && 
                               export PATH=$JAVA_HOME/bin:$PATH && 
                               export PYTHONPATH="/mnt/c/Users/ASUS/DBDA Python/airflow:$PYTHONPATH" && 
                               /home/sagar/airflow-project/.venv/bin/spark-submit "/mnt/c/Users/ASUS/DBDA Python/airflow/airflow_project/spark_jobs/spark_transform.py" """ )

    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3)

    end_task = PythonOperator(
        task_id="end",
        python_callable=end )

    start_task >> download_task >> validate_task >> spark_task >> upload_task >> end_task