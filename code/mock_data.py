# ============================================
# Script: Insert Random Gadget Orders to DynamoDB
# Author: [Your Name]
# Description: Generates and inserts random orders into a DynamoDB table in real-time.
# ============================================

import boto3                    # AWS SDK for Python to interact with AWS services
import random                   # Used to generate random numbers and choices
import time                     # Used for introducing delay between insertions
from decimal import Decimal     # Required for precise numeric representation in DynamoDB

# -------------------------------
# Step 1: Initialize DynamoDB Resource
# -------------------------------

# Create a Boto3 session using a configured AWS CLI profile and region.
# Make sure your AWS CLI is configured with the `default` profile.
session = boto3.Session(
    profile_name='default',     # The AWS profile to use (from ~/.aws/credentials)
    region_name='us-east-1'     # The AWS region where DynamoDB is hosted
)

# Get a DynamoDB service resource using the session
dynamodb = session.resource('dynamodb')

# Reference to the DynamoDB table named 'GadgetOrders'
table = dynamodb.Table('GadgetOrders_Ritayan')

# -------------------------------
# Step 2: Generate Random Order Data
# -------------------------------

def generate_order_data():
    """
    Generate a random order record.

    Returns:
        dict: A dictionary with keys:
            - orderid (str): Random order ID between 1 and 10,000
            - product_name (str): Random product from a predefined list
            - quantity (int): Random quantity between 1 and 5
            - price (Decimal): Random price between 10.00 and 500.00
    """
    orderid = str(random.randint(1, 10000))  # Random integer as string
    product_name = random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones', 'Charger'])  # Random product
    quantity = random.randint(1, 5)  # Random quantity
    price = Decimal(str(round(random.uniform(10.0, 500.0), 2)))  # Price with 2 decimal places using Decimal

    return {
        'orderId': orderid,
        'product_name': product_name,
        'quantity': quantity,
        'price': price
    }

# -------------------------------
# Step 3: Insert Data into DynamoDB Table
# -------------------------------

def insert_into_dynamodb(data):
    """
    Insert a dictionary item into the DynamoDB table.

    Args:
        data (dict): A dictionary representing a single order.

    This function uses `put_item`, which replaces the existing item
    if an item with the same primary key already exists.
    """
    try:
        print(data)
        table.put_item(Item=data)
        print(f"✅ Inserted data: {data}")
    except Exception as e:
        print(f"❌ Error inserting data: {str(e)}")

# -------------------------------
# Step 4: Main Execution Loop
# -------------------------------

if __name__ == '__main__':
    try:
        print("🚀 Starting to insert random gadget orders into DynamoDB...")
        while True:
            data = generate_order_data()      # Step 1: Generate a new random order
            insert_into_dynamodb(data)        # Step 2: Insert into DynamoDB table
            time.sleep(2)                     # Step 3: Wait for 2 seconds (simulating streaming)
    except KeyboardInterrupt:
        print("\n🛑 Script stopped manually via KeyboardInterrupt (Ctrl+C)")
