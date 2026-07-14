# Airflow PySpark ETL Pipeline 
## Overview This project demonstrates an end-to-end ETL pipeline using: 
- Apache Airflow 
- PySpark 
- Amazon S3 
- XCom 
- Data validation and transformation 
- 
- ## Pipeline Flow 
1. Download input CSV from S3 
2. Validate the file 
3. Pass metadata using XCom 
4. Process data with PySpark 
5. Generate curated output 
6. Upload processed file back to S3 

## Project Structure 

airflow_project/ 
├── dags/ 
│ └── etl_pipeline.py 
├── scripts/ 
│ ├── download.py 
│ ├── validate.py 
│ ├── upload.py 
│ └── transform.py 
├── spark_jobs/ 
│ └── spark_transform.py 
├── data/ 
├── output/ 
└── README.md 

## Technologies Used 
- Python 3.10 
- Apache Airflow 2.10 
- Apache Spark 4.x 
- Pandas 
- AWS S3 

## Key Features 
- Airflow orchestration 
- XCom-based metadata sharing 
- PySpark transformations 
- Automated S3 integration 
- Modular ETL design 

## Future Enhancements 
- EMR Serverless integration 
- Event-driven execution 
- Lambda trigger from S3 
- Production monitoring
