# Sales Data Analysis and Projection
This project focuses on analyzing sales data and projecting future sales trends using Python and various data analysis libraries. The goal is to provide insights into sales performance and forecast future sales based on historical data.

## Technologies Used
- Python
- AWS S3 for data storage
- AWS DynamoDB for NoSQL database
- AWS DynamoDb Streams for real-time data processing
- AWS Lambda for serverless computing
- AWS Glue for ETL (Extract, Transform, Load) processes
- AWS GLue Data Catalog for metadata management
- AWS Kinesis for real-time data streaming
- AWS Firehose for data delivery
- AWS Athena for querying data
- AWS EventBridge Pipe for event-driven architecture


## Architecture Overview
The architecture consists of several AWS services working together to handle data ingestion, processing, storage, and analysis. The flow of data is as follows:

1. **Data Generation**: Mock sales data is generated.
2. **Data Storage**: The generated data is stored in AWS DynamoDB.
3. **Event-Driven Processing**: AWS DynamoDB Streams captures changes to the data and triggers AWS EventBridge Pipe.
4. **Real-Time Processing**: Data is ingested into AWS Kinesis for real-time processing.
5. **Data Delivery**: AWS Firehose delivers the processed data to AWS S3.
6. **Data Transformation**: Data is transformed using AWS Lambda and put back into AWS firehose.
7. **Data Cataloging**: AWS Glue Data Catalog stores metadata about the data in S3.
8. **Data Querying**: AWS Athena is used to query the data stored in S3.


## 