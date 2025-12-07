import json
import datetime

def lambda_handler(event, context):
    """
    Stubbed insights handler:
    Returns a hard-coded sample insights payload for now.
    """
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    sample_response = {
        "run_date": now,
        "total_spend": 1234.56,
        "previous_period_spend": 1100.00,
        "spend_delta_pct": 12.25,
        "summary": "Your AWS spend increased 12% compared to the previous period, mainly driven by EC2 and S3.",
        "top_recommendations": [
            {
                "id": "rec-ec2-1",
                "category": "EC2 Right-Sizing",
                "description": "Downsize three t3.2xlarge instances in the prod-app cluster to t3.xlarge based on <10% average CPU.",
                "estimated_savings_monthly": 245.30,
                "urgency": "HIGH",
                "confidence": 0.87
            },
            {
                "id": "rec-s3-1",
                "category": "S3 Storage Class Optimization",
                "description": "Move infrequently accessed objects from s3://logs-prod-archive to S3 Glacier Instant Retrieval.",
                "estimated_savings_monthly": 80.00,
                "urgency": "MEDIUM",
                "confidence": 0.78
            }
        ],
        "raw_findings": {
            "by_service": [
                { "service": "AmazonEC2", "cost": 765.43 },
                { "service": "AmazonRDS", "cost": 250.11 },
                { "service": "AmazonS3", "cost": 120.10 }
            ],
            "anomalies": [
                {
                    "service": "AmazonS3",
                    "delta_pct": 45.2,
                    "reason": "Cost increased after enabling access logs on logs-prod-archive."
                }
            ]
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(sample_response)
    }
