import json
import boto3

translate_client = boto3.client("translate")


def translate_text(text, source_language, target_language):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )

    return response["TranslatedText"]


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        text = body["text"]
        source_language = body["sourceLanguage"]
        target_language = body["targetLanguage"]

        translated_text = translate_text(
            text,
            source_language,
            target_language
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "translatedText": translated_text
            })
        }

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Missing field: {e.args[0]}"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }