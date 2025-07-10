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
