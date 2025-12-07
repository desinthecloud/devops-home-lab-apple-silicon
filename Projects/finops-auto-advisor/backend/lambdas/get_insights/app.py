import os
import json
import logging
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
INSIGHTS_TABLE_NAME = os.getenv("INSIGHTS_TABLE_NAME", "")

def _get_latest_insights():
    if not INSIGHTS_TABLE_NAME:
        logger.error("INSIGHTS_TABLE_NAME env var is not set")
        return None

    table = dynamodb.Table(INSIGHTS_TABLE_NAME)

    resp = table.query(
        KeyConditionExpression=Key("pk").eq("run_insights"),
        ScanIndexForward=False,  # newest first
        Limit=1,
    )

    items = resp.get("Items", [])
    if not items:
        return None

    return items[0]

def _decimal_to_float(obj):
    """
    Recursively convert Decimal objects to float so json.dumps doesn't explode.
    """
    if isinstance(obj, list):
        return [_decimal_to_float(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    logger.info("GetInsightsFunction invoked with event: %s", json.dumps(event))

    item = _get_latest_insights()

    if not item:
        body = {
            "error": "NO_DATA",
            "message": "No insights found yet. Run the cost analyzer first."
        }
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(body)
        }

    # Build response body from DynamoDB item
    response_body = {
        "run_date": item.get("run_date"),
        "total_spend": item.get("total_spend", 0),
        "previous_period_spend": item.get("previous_period_spend", 0),
        "spend_delta_pct": item.get("spend_delta_pct", 0),
        "summary": item.get("summary", ""),
        "top_recommendations": item.get("top_recommendations", []),
        "raw_findings": item.get("raw_findings", {"by_service": [], "anomalies": []}),
    }

    # Normalize all Decimals → float
    response_body = _decimal_to_float(response_body)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_body)
    }
