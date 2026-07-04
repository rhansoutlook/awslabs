# Milestone 3

## End-to-End Translation API Successfully Tested

This milestone marks the completion of the first fully functional
version of the Serverless Translator. The request now travels through
API Gateway, Lambda and Amazon Translate before returning the translated
response to the client.

------------------------------------------------------------------------

# Lesson Learned -- The API Gateway "Merry-Go-Round"

> *We jokingly called it the "API merry-go-round", but the investigation
> was a serious engineering exercise.*

## Observation

Even after defining an explicit `AWS::Serverless::Api` with a `Prod`
stage, API Gateway consistently created **two stages**:

-   `Prod`
-   `Stage`

Deleting the stack and redeploying did **not** eliminate the extra
stage.

## Investigation

We verified:

-   Fresh CloudFormation stack creation
-   Explicit `AWS::Serverless::Api`
-   Correct `RestApiId`
-   Clean `sam build --no-cached`
-   Generated template
-   Processed CloudFormation template

## Root Cause

By default, whenever a Lambda function defines an API event, AWS SAM can
synthesize an internal API deployment using legacy behaviour.

Even though an explicit API with a `Prod` stage had been defined, the
older synthesis path created an additional deployment stage named
**Stage**.

## Resolution

Adding the following property switched SAM to its modern synthesis path:

``` yaml
TranslatorApi:
  Type: AWS::Serverless::Api
  Properties:
    Name: ServerlessTranslatorApi
    StageName: Prod
    OpenApiVersion: '3.0'
```

## Result

Only the intended **Prod** stage was created.

## Engineering Lesson

Never accept unexpected infrastructure as "just how AWS works."
Investigate, verify, isolate the cause, and only then move on.

------------------------------------------------------------------------

# Useful Pattern -- Testing a REST API with curl

``` bash
curl -X POST "<API_ENDPOINT>" \
  -H "Content-Type: application/json" \
  -d '{
        "text":"Hello",
        "sourceLanguage":"en",
        "targetLanguage":"fr"
      }'
```

### Expected Response

``` json
{
  "translatedText": "Bonjour"
}
```

This validates the complete request path:

``` text
curl
  │
  ▼
API Gateway
  │
  ▼
Lambda
  │
  ▼
Amazon Translate
  │
  ▼
Lambda
  │
  ▼
API Gateway
  │
  ▼
Client
```

------------------------------------------------------------------------

**Milestone Status:** ✅ Complete
