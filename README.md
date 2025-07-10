# Sales Data Analysis
This project focuses on analyzing sales data and trends using Python and various data analysis libraries. The goal is to provide insights into sales performance and forecast future sales based on historical data.

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

<img width="883" height="720" alt="Sales Data" src="https://github.com/user-attachments/assets/3f9934be-2284-4154-a105-9d4228aa22fe" />

## Setup Steps

### Install AWS CLI
1. Download the file using the curl command. The -o option specifies the file name that the downloaded package is written to. In this example, the file is written to AWSCLIV2.pkg in the current folder.
```
$ curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
```

2. Run the standard macOS installer program, specifying the downloaded .pkg file as the source. Use the -pkg parameter to specify the name of the package to install, and the -target / parameter for which drive to install the package to. The files are installed to /usr/local/aws-cli, and a symlink is automatically created in /usr/local/bin. You must include sudo on the command to grant write permissions to those folders.
```
$ sudo installer -pkg ./AWSCLIV2.pkg -target /
```

3. After installation is complete, debug logs are written to /var/log/install.log.
To verify that the shell can find and run the aws command in your $PATH, use the following commands.
```
$ which aws
/usr/local/bin/aws 
$ aws --version
aws-cli/2.19.1 Python/3.11.6 Darwin/23.3.0 botocore/2.4.5
```

### Configure AWS CLI

1. Create Access Keys and download them as .csv file
   <img width="1683" height="792" alt="image" src="https://github.com/user-attachments/assets/c407e197-2693-4a9a-b772-2535438ef817" />

2. If you have the AWS CLI installed:
```
aws configure --profile default
```

3. You'll be prompted to enter the following details:
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

### Create Dynamo DB tables
1. Create a Dynamo DB table where the mock sales data will be stored.
<img width="1701" height="571" alt="image" src="https://github.com/user-attachments/assets/a0df8038-fbef-484c-a639-255676e90ad0" />

2. Fill the details and click on `Create`
<img width="1636" height="1525" alt="image" src="https://github.com/user-attachments/assets/09e96809-a524-420f-aa51-17c43f99c612" />

3. The table details are as given below.
<img width="1636" height="1525" alt="image" src="https://github.com/user-attachments/assets/27b717b9-25a3-42c6-80e2-0d9df51041d3" />

4. Enable Dynamo DB Stream API
<img width="1374" height="971" alt="image" src="https://github.com/user-attachments/assets/b18d15a8-453a-4cc4-b032-2332d04df984" />

<img width="1675" height="521" alt="image" src="https://github.com/user-attachments/assets/3c852ce9-8090-458b-b395-669418aeb8a7" />
Basically, if I take the example of RDS, I wll get the entire row which is changed. Other options include getting only the changed attribute
which is similar to getting only the column name and value that is changed. Other options are intuive.

### Create Amazon Kinesis Instance
1. Create a data stream
   <img width="1660" height="1155" alt="image" src="https://github.com/user-attachments/assets/30d5b86a-0cc5-4c40-9724-8046c00d2ff7" />

2. View The Kinesis Instance details below
   <img width="1283" height="256" alt="image" src="https://github.com/user-attachments/assets/94c94cbe-8065-48ea-9ba1-9fbce084544c" />


### Create Event Bridge Pipe to listen to Dynamo DB Stream API for CDC and sent it to Kinesis

EventBridge Pipes is a fully managed service that makes it easy to connect event sources to targets with optional filtering, transformation, and enrichment.
Think of it as a low-code ETL pipeline for event-driven data — like "glue" between your services without needing custom Lambda functions or Step Functions.

How It Works
```
[Source] → [Filter] → [Enrichment (optional)] → [Transform (optional)] → [Target]
```
- Source: Where the event comes from (e.g., SQS)
- Filter: Only forward specific events
- Enrichment (Transform): Add more data via Lambda or Step Functions or transform the data
- Target: Final destination (e.g., another queue, Lambda, etc.)

**Why Use It?**
- No need to write Lambda code just to move or filter events
- Automatically scales and retries failed events
- Saves time in building event-driven apps


1. Create a Event Bride Pipe
   <img width="1670" height="789" alt="image" src="https://github.com/user-attachments/assets/9b5bbb84-9489-48d7-9c15-f0f2418aca7b" />

2. Select the source
   <img width="1669" height="783" alt="image" src="https://github.com/user-attachments/assets/c06e27b6-60ad-4f9c-9e31-68a4e66b95dc" />
   <img width="826" height="392" alt="image" src="https://github.com/user-attachments/assets/aac9bcd7-96d3-429e-b1c0-74b0bdc4c0c6" />

3. Select the target
   Remove the intermediate steps like `Filtering` and `Enrichment` by clicking on the `Remove` button.
   <img width="1677" height="701" alt="image" src="https://github.com/user-attachments/assets/0ba91fb8-574e-480d-ab80-85544483367b" />
4. Click on `Create Pipe`
   <img width="1151" height="748" alt="image" src="https://github.com/user-attachments/assets/61f5643a-2430-4e9d-a79f-682f0a3387f8" />

5. Give Write Access to Event Bridge Pipe
<img width="959" height="528" alt="image" src="https://github.com/user-attachments/assets/b9fe3a94-070f-4bbd-8641-b3ad9b76a63a" />
<img width="1078" height="685" alt="image" src="https://github.com/user-attachments/assets/d6fc0416-70d2-42c3-a349-ebbf627c1a64" />

6. The pipe is successfully created.
   <img width="1368" height="257" alt="image" src="https://github.com/user-attachments/assets/5f0b3838-9424-4f50-9c05-397d14f257b2" />

In the Kinesis, the data will look like this as shown below
<img width="1348" height="692" alt="image" src="https://github.com/user-attachments/assets/34047788-e89d-4bee-bb11-80c66015e06e" />

```
{
    "eventID": "c199a649301a602afc9f5e6332f3d9f7",
    "eventName": "INSERT",
    "eventVersion": "1.1",
    "eventSource": "aws:dynamodb",
    "awsRegion": "us-east-1",
    "dynamodb": {
        "ApproximateCreationDateTime": 1752158591,
        "Keys": {
            "orderId": {
                "S": "921"
            }
        },
        "NewImage": {
            "quantity": {
                "N": "1"
            },
            "orderId": {
                "S": "921"
            },
            "price": {
                "N": "146.37"
            },
            "product_name": {
                "S": "Laptop"
            }
        },
        "SequenceNumber": "149600003405850623541670",
        "SizeBytes": 57,
        "StreamViewType": "NEW_IMAGE"
    },
    "eventSourceARN": "arn:aws:dynamodb:us-east-1:692018623807:table/GadgetOrders_Ritayan/stream/2025-07-10T14:05:24.903"
}
```

### Create a S3 bucket
1. Create a S3 bucket by giving it a unique name and create it with default settings.
<img width="3312" height="4301" alt="image" src="https://github.com/user-attachments/assets/a6c77805-3601-4631-aacf-7a81128d0914" />

2. Click on `Create bucket`
<img width="743" height="306" alt="image" src="https://github.com/user-attachments/assets/087be08d-5c9b-4f21-a96e-f518a554f573" />

### Create a Lambda Function to apply transformation on the streaming data
1. Create a Lambda Function
<img width="1379" height="450" alt="image" src="https://github.com/user-attachments/assets/9c439767-2b21-4443-a61f-624fe8e84141" />
<img width="1139" height="361" alt="image" src="https://github.com/user-attachments/assets/85c9c43b-0fc5-4bb0-b249-533a7548622e" />

2. Apply the Transformation code `kinesis_data_transformer_using_lambda.py`
3. Click on `Deploy` after adding the code to code source.
<img width="1132" height="629" alt="image" src="https://github.com/user-attachments/assets/ff8648be-d688-467b-bc6d-af6a4e93c1d7" />

4. Increase Timeout and add required Firehose permissions
<img width="1380" height="675" alt="image" src="https://github.com/user-attachments/assets/dbf13233-e246-4f38-9dd3-35b669a8da52" />
<img width="1101" height="686" alt="image" src="https://github.com/user-attachments/assets/1fdf8161-b816-497c-be4d-5fcf364915a9" />


### Create Kinesis Firehose

Kinesis Data Firehose is a fully managed data delivery service used to capture, transform, and load streaming data into storage and analytics services in near real-time, such as:

- Amazon S3
- Amazon Redshift
- Amazon OpenSearch Service
- Amazon Data Firehose for Splunk, Datadog, New Relic, etc.
- Generic HTTP endpoints

Serverless: No need to manage clusters, scaling, or batching.

```
  [ Amazon Kinesis ]
         ↓
  ┌─────────────────────┐
  │   Kinesis Firehose  │
  └─────────────────────┘
         ↓       ↓       ↓
   [ Transform ] [ Buffer ] [ Compress/Encrypt ] (Using AWS Lambda)
         ↓
     [ Destination ]
        └── S3 / Redshift / OpenSearch / Splunk
```

1. Create a Firehose Instance.
2. Add the necessary details while creation.
<img width="3328" height="7171" alt="image" src="https://github.com/user-attachments/assets/3e8f020f-dfad-491c-ae6f-24f217cf9988" />

3. If there is an issue in the permissions. Check the role and the following below.
<img width="1287" height="771" alt="image" src="https://github.com/user-attachments/assets/2b3ddebf-c95a-4f1a-bf9b-f17a6f6348da" />

After a performing a test,
As you can see below, the transformed data is generated in S3
<img width="1045" height="733" alt="image" src="https://github.com/user-attachments/assets/1fb58fe5-ac7f-4164-aa7c-a0af827f81c8" />

```
{"orderid": "2044", "product_name": "Tablet", "quantity": 4, "price": 200.44, "event_type": "INSERT", "creation_time": 1752161982}
{"orderid": "4997", "product_name": "Laptop", "quantity": 4, "price": 311.9, "event_type": "INSERT", "creation_time": 1752161990}
```

### Create a Glue Crawler

What is **AWS Glue Crawler**?

A **Glue Crawler**:

* Connects to a **data source** (e.g., S3, JDBC, DynamoDB)
* **Reads the structure** of the data (CSV, JSON, Parquet, etc.)
* Infers:

  * Column names
  * Data types
  * Partitions
* Automatically **creates or updates** tables in the **Glue Data Catalog**

**Example**:
You have JSON files in `s3://my-bucket/sales/`. A crawler can scan the data and create a table `sales_data` with columns like `customer_id`, `order_id`, `amount`.

What is **AWS Glue Data Catalog**?

The **Glue Data Catalog** is:

* A **centralized metadata repository** for all your datasets
* Stores:

  * Databases (logical grouping of tables)
  * Tables (schema: column names, types, location in S3)
  * Job definitions and partitions

**Used by:**

* **AWS Glue Jobs** to process data
* **Athena** to query S3 files using SQL
* **Redshift Spectrum** to read external S3 data
* **EMR, Presto, Hive** for table lookups

**Think of it like a "Hive Metastore" for all AWS analytics services**.

**How They Work Together?**

1. You run a **Glue Crawler**
2. It scans data in your source (e.g., S3)
3. It creates a **table** in the **Data Catalog**
4. You query or process the data using Glue, Athena, Redshift, etc.

**Summary Table**

| Feature              | Glue Crawler                    | Glue Data Catalog                    |
| -------------------- | ------------------------------- | ------------------------------------ |
| Role                 | Scans & infers schema           | Stores metadata (schemas, tables)    |
| Output               | Tables in Data Catalog          | Metadata used by analytics services  |
| Used For             | Automated schema detection      | Querying and managing datasets       |
| Services That Use It | Glue ETL jobs, Athena, Redshift | Glue, Athena, Redshift Spectrum, EMR |


1. Create a Database
<img width="1686" height="504" alt="image" src="https://github.com/user-attachments/assets/996f8280-0032-4ae7-b8b7-60dfc4467e0b" />
2. Create a Glue Crawler
<img width="1699" height="601" alt="image" src="https://github.com/user-attachments/assets/0941fd1e-828c-4a1d-b6a1-0dd9434daf7c" />
   - Add a classifier to extarct the fields from JSON file
     <img width="1692" height="651" alt="image" src="https://github.com/user-attachments/assets/f612899a-5f1a-48af-a66f-2a61cde9e530" />
3. Add the necessaru details for crawler creation
<img width="1643" height="932" alt="image" src="https://github.com/user-attachments/assets/f202e51f-63d2-46c3-ad7e-b511f8b55e0d" />

### Open AWS Athena to query the Glue Catelog
- Amazon Athena is a serverless, interactive query service that lets you analyze data stored in Amazon S3 using standard SQL.
- No servers, no ETL pipelines — just point to your S3 data, define a schema, and start querying with SQL.

- You store your raw or processed data in S3 — files can be CSV, JSON, Parquet, ORC, Avro, etc.
- You define a schema for that data:
- Manually via SQL DDL (CREATE EXTERNAL TABLE)
- Or Automatically using AWS Glue Crawlers
- You run SQL queries on it using Athena's query editor or API.
- Athena scans the S3 data in-place (no data movement) and returns the results.



<img width="968" height="682" alt="image" src="https://github.com/user-attachments/assets/38a92a01-495f-4255-9300-49748ddf5010" />


## Results

1. Insert Mock Data
   <img width="1317" height="974" alt="image" src="https://github.com/user-attachments/assets/e00a34cf-1bac-411c-b054-07c19ac1cb78" />

2. Check S3 For data avalability after transformation using Lambda
   <img width="1678" height="756" alt="image" src="https://github.com/user-attachments/assets/dbb83a9c-36dd-4b4f-bdde-90736b9681cf" />
3. Download the data to local to check the correct transformation
   <img width="1195" height="210" alt="image" src="https://github.com/user-attachments/assets/933c4676-da4f-4cc5-9f5c-3ffe99914998" />
4. Check Glue Crawler

   <img width="1369" height="621" alt="image" src="https://github.com/user-attachments/assets/4586cf63-aa9a-4e15-8210-8e637c9a5d7b" />
   The table is created and populated.
   <img width="1412" height="772" alt="image" src="https://github.com/user-attachments/assets/64b66a27-6c06-49f9-a4e3-8b5325329ca3" />
   The partitions are the subfolders in S3
   <img width="1301" height="695" alt="image" src="https://github.com/user-attachments/assets/78ca0b8b-b6fb-4fdf-a4d7-a9dc691712f2" />

5. Lets Query the Table using Athena
   Athena asks a S3 location to store the results it runs. So assign a folder in S3 bucket.
   <img width="1110" height="330" alt="image" src="https://github.com/user-attachments/assets/cf6a7218-40ed-4b98-858c-4eaa6aae0b1d" />
   <img width="1409" height="424" alt="image" src="https://github.com/user-attachments/assets/b7c458c8-ef96-422e-9caa-27834d2104b5" />

   - Now query the files.
     <img width="1609" height="1117" alt="image" src="https://github.com/user-attachments/assets/1282b1cc-390a-461d-bb81-b0724868f7c2" />
   - Give total sales order by product
     <img width="1575" height="970" alt="image" src="https://github.com/user-attachments/assets/3eee8a74-6246-4a3c-b3f5-cb47d476633c" />
   - The number of Unique Products and their names
     <img width="1315" height="783" alt="image" src="https://github.com/user-attachments/assets/2e83772f-dbb3-4752-96e9-b89f2afcc4bd" />


6. When a change is made on a record in Dynamo DB. The cahgned record is only propagated via Kinesis streaming and stored in S3
   which can again be queried after crawling using AWS Glue and Athena.
   <img width="1118" height="420" alt="image" src="https://github.com/user-attachments/assets/7d293a65-8542-49ad-a970-b8c3768072f3" />




