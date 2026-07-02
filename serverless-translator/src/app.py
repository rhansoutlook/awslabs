import json


def lambda_handler(event, context):
    """
    Entry point for the Serverless Translator API.
    """

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Serverless Translator API is alive"
            }
        ),
    }