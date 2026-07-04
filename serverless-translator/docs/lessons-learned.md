
# Lessons Learned
## Building the Serverless Translator

> **Purpose**
>
> This document captures the technical lessons learned while building the Serverless Translator project.
> It is intentionally focused on engineering discoveries, design decisions, troubleshooting, and AWS behavior.
> It is **not** a project diary or documentation guide.

---

# Lesson 1 - Validate before you build

## Observation

Run `sam validate` before `sam build`.

## Why

Validation is fast and catches template errors before spending time building or deploying.

---

# Lesson 2 - Build before you deploy

## Workflow

```text
sam validate
sam build
sam local invoke
sam deploy
```

This workflow minimizes deployment failures and provides rapid feedback.

---

# Lesson 3 - `sam build` does not require AWS credentials

## Observation

`sam build` packages the application locally.

It does not communicate with AWS.

---

# Lesson 4 - `sam deploy` requires AWS credentials

Deployment communicates with AWS CloudFormation and therefore requires valid credentials.

---

# Lesson 5 - Docker simulates Lambda, not IAM

## Observation

`sam local invoke` executes inside a Docker container.

## Important Discovery

Docker simulates the Lambda runtime.

It **does not** assume the Lambda execution role.

AWS SDK calls use the AWS credentials currently configured on the local machine.

### Local execution

```text
sam local invoke
        │
        ▼
Docker Container
        │
        ▼
Your AWS Credentials
        │
        ▼
AWS Services
```

### Deployed execution

```text
API Gateway
      │
      ▼
Lambda
      │
      ▼
Lambda Execution Role
      │
      ▼
AWS Services
```

---

# Lesson 6 - SAM creates two CloudFormation stacks

Deploying a SAM application creates:

1. A SAM-managed infrastructure stack.
2. The application stack.

The managed stack contains the deployment S3 bucket.

The application stack contains Lambda, API Gateway, IAM roles and related resources.

---

# Lesson 7 - `ROLLBACK_COMPLETE` is terminal

A CloudFormation stack in `ROLLBACK_COMPLETE` cannot be updated.

Delete it before deploying again.

---

# Lesson 8 - Least privilege is an iterative process

The deployment role was intentionally built with least privilege.

Missing permissions were discovered during deployment and added only after understanding why they were required.

Examples included:

- CloudFormation Change Sets
- IAM tagging
- Lambda tagging
- S3 tagging
- S3 encryption configuration

---

# Lesson 9 - Lambda already contains boto3

AWS Lambda includes `boto3`.

Installing `boto3` locally is primarily for development tooling and editor support.

---

# Lesson 10 - API naming vs Python naming

External JSON:

- camelCase

Internal Python:

- snake_case

Example:

```json
{
    "sourceLanguage": "en"
}
```

```python
source_language = body["sourceLanguage"]
```

---

# Lesson 11 - Test locally before testing through API Gateway

Current testing strategy:

1. `sam validate`
2. `sam build`
3. `sam local invoke`
4. `sam deploy`
5. Test the deployed API

---

# Lesson 12 - Every significant discovery belongs here

This document will continue to grow throughout the project.

Only genuine engineering lessons are included.
