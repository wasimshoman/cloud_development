# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Deploy & Teardown

```bash
serverless deploy                        # deploy to AWS (us-east-1)
serverless remove                        # tear down all AWS resources
serverless remove --region eu-north-1   # tear down from a specific region
```

## Live API

```
https://vg3pvmuaoc.execute-api.us-east-1.amazonaws.com
```

## Architecture

Serverless Framework app on AWS. One `serverless.yml` drives everything — Lambda functions, API Gateway routes, DynamoDB table, and EventBridge rule are all provisioned via CloudFormation on deploy.

**Request flow:** Thunder Client / curl → API Gateway HTTP API → Lambda function → DynamoDB

**Event flow:** notes-app source event → EventBridge default bus → `logEvent` Lambda → CloudWatch Logs

## Project Structure

- `serverless.yml` — single config file that defines all infrastructure and wires functions to routes
- `functions/` — one `.py` file per Lambda function, each exports a `handler(event, context)` function

## Key Details

- Runtime: Python 3.9
- Database: DynamoDB table `notes-table`, partition key `id` (String), on-demand billing
- All Lambda functions share the same IAM role defined in `serverless.yml` under `provider.iam`
- `logEvent.py` is the only function not triggered by HTTP — it responds to EventBridge events with `source: notes-app`
- DynamoDB access uses `boto3.resource` (not `boto3.client`) — the table object is initialized at module level outside the handler so it's reused across warm invocations
