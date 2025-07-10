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

<img width="834" height="720" alt="Sales Data" src="https://github.com/user-attachments/assets/0ac9a4f1-7c74-4335-b29b-882badb23be7" />


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


### Create a S3 bucket
1. Create a S3 bucket by giving it a unique name and create it with default settings.
<img width="3312" height="4301" alt="image" src="https://github.com/user-attachments/assets/a6c77805-3601-4631-aacf-7a81128d0914" />

2. Click on `Create bucket`
<img width="743" height="306" alt="image" src="https://github.com/user-attachments/assets/087be08d-5c9b-4f21-a96e-f518a554f573" />

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
   [ Transform ] [ Buffer ] [ Compress/Encrypt ]
         ↓
     [ Destination ]
        └── S3 / Redshift / OpenSearch / Splunk
```
