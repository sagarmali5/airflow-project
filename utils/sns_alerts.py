import boto3
def failure_alert(context):
    task_id = context["task_instance"].task_id
    exception = context.get("exception")

    if task_id == "validate_data":
        subject = "Validation Failed"
        message = "Missing required columns or data validation failed in the input file."

    elif task_id == "spark_transform":
        subject = "Spark Job Failed"
        message = f"Spark transformation failed. Error: {exception}"

    else:
        subject = f"Task Failed - {task_id}"
        message = f"Task {task_id} failed with error: {exception}"

    sns = boto3.client("sns", region_name="ap-south-1")

    sns.publish(
        TopicArn="arn:aws:sns:ap-south-1:762038223499:etl-alerts",
        Subject=subject,
        Message=message)