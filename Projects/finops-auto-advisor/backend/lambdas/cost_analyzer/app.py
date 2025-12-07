import os
import json
import datetime
import logging
from decimal import Decimal, ROUND_HALF_UP

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
INSIGHTS_TABLE_NAME = os.getenv("INSIGHTS_TABLE_NAME", "")

def to_decimal(value: float) -> Decimal:
    """
    Helper to safely convert floats to Decimal with 2 decimal places.
    """
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def lambda_handler(event, context):
    """
    Cost analyzer (MVP stub):
    - Pretends to analyze costs
    - Writes a full 'run_insights' document into DynamoDB
      that the API and dashboard can read.
    """
    logger.info("CostAnalyzerFunction invoked with event: %s", json.dumps(event))

    if not INSIGHTS_TABLE_NAME:
        logger.error("INSIGHTS_TABLE_NAME env var is not set")
        return {"statusCode": 500, "body": "Configuration error"}

    table = dynamodb.Table(INSIGHTS_TABLE_NAME)

    # Use date-based key so we can query latest run easily
    run_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Stubbed values for now, but all as Decimal
    total_spend = to_decimal(1234.56)
    previous_period_spend = to_decimal(1100.00)
    spend_delta_pct = ((total_spend - previous_period_spend) / previous_period_spend * Decimal(100)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    item = {
        "pk": "run_insights",
        "sk": run_date,
        "run_date": run_date,
        "total_spend": total_spend,
        "previous_period_spend": previous_period_spend,
        "spend_delta_pct": spend_delta_pct,
        "summary": "Your AWS spend increased 12% compared to the previous period, mainly driven by EC2 and S3.",
        "top_recommendations": [
            {
                "id": "rec-ec2-1",
                "category": "EC2 Right-Sizing",
                "description": "Downsize three t3.2xlarge instances in the prod-app cluster to t3.xlarge based on <10% average CPU.",
                "estimated_savings_monthly": to_decimal(245.30),
                "urgency": "HIGH",
                "confidence": to_decimal(0.87),
            },
            {
                "id": "rec-s3-1",
                "category": "S3 Storage Class Optimization",
                "description": "Move infrequently accessed objects from s3://logs-prod-archive to S3 Glacier Instant Retrieval.",
                "estimated_savings_monthly": to_decimal(80.00),
                "urgency": "MEDIUM",
                "confidence": to_decimal(0.78),
            }
        ],
        "raw_findings": {
            "by_service": [
                { "service": "AmazonEC2", "cost": to_decimal(765.43) },
                { "service": "AmazonRDS", "cost": to_decimal(250.11) },
                { "service": "AmazonS3", "cost": to_decimal(120.10) },
            ],
            "anomalies": [
                {
                    "service": "AmazonS3",
                    "delta_pct": to_decimal(45.2),
                    "reason": "Cost increased after enabling access logs on logs-prod-archive.",
                }
            ]
        }
    }

    table.put_item(Item=item)
    logger.info("Wrote insights item to DynamoDB: %s", item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Stub cost analysis complete",
            "run_date": run_date
        }),
    }
