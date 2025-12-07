import os
import json
import datetime
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
INSIGHTS_TABLE_NAME = os.getenv("INSIGHTS_TABLE_NAME", "")

def lambda_handler(event, context):
    """
    Stubbed cost analyzer:
    - Logs that it ran
    - Writes a simple 'heartbeat' item into DynamoDB so we know the schedule works
    """
    logger.info("CostAnalyzerFunction invoked with event: %s", json.dumps(event))

    if not INSIGHTS_TABLE_NAME:
        logger.error("INSIGHTS_TABLE_NAME env var is not set")
        return {"statusCode": 500, "body": "Configuration error"}

    table = dynamodb.Table(INSIGHTS_TABLE_NAME)

    run_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    item = {
        "pk": "run",
        "sk": run_date,
        "note": "Stub run - real cost analysis not implemented yet",
        "created_at": run_date,
    }

    table.put_item(Item=item)

    logger.info("Wrote stub run item to DynamoDB: %s", item)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Stub cost analysis complete", "run_date": run_date}),
    }
