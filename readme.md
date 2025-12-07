# **AWS IAM Policies for DynamoDB, EC2, and Lambda**

This document summarizes the custom IAM policies created for managing permissions across AWS DynamoDB, EC2, and Lambda services.

## **Policies**

| Policy Name | Purpose | Permissions Granted | Target Resource(s) |
| :---- | :---- | :---- | :---- |
| DynamoDb reader | Grants read-only access to DynamoDB tables. | dynamodb:BatchGetItem, dynamodb:GetItem, dynamodb:Query, dynamodb:Scan, dynamodb:DescribeTable | All DynamoDB Tables (\*) |
| DynamoDb writer | Grants write access to a specific DynamoDB table. | dynamodb:PutItem, dynamodb:UpdateItem, dynamodb:DeleteItem, dynamodb:BatchWriteItem | Specific Table: orders |
| EC2handler | Grants full administrative access to EC2. | ec2:\* (All EC2 actions) | All EC2 resources (\*) |
| noScans | Grants all DynamoDB actions **except** dynamodb:Scan. | dynamodb:\* (All actions) **excluding** dynamodb:Scan | All DynamoDB Tables (\*) |
| Lambda and DynamoDB Policy | Grants full Lambda access and DynamoDB read access. | lambda:\* and DynamoDB read actions (e.g., dynamodb:GetItem, dynamodb:Query). | All Lambda and DynamoDB resources (\*) |

## **IAM Role Configuration**

### **LambdaHandler Role**

* **Purpose:** To be assumed by AWS Lambda functions.  
* **Attached Policies:** The custom Lambda and DynamoDB Policy (from above) and typically the AWS managed policy AWSLambdaBasicExecutionRole for logging.  
* **Trust Relationship:** Allows the lambda.amazonaws.com service principal to assume the role.

## **IAM Group Configuration**

### **Admins Group**

* **Purpose:** Provides broad administrative access while explicitly restricting a specific service.  
* **Attached Policies:**  
  1. AWS Managed Policy: AdministratorAccess (Grants full access to all services).  
  2. Custom Policy: Admins EC2 Deny Policy (Explicitly denies all ec2:\* actions).

**Result:** Members of the Admins group have full administrative control over the AWS account, **except** they are explicitly prevented from performing any actions on Amazon EC2 resources. This is achieved because an explicit Deny always overrides an Allow in IAM policy evaluation.