# Lessons Learned
## Building the Serverless Translator

> A living technical journal capturing engineering discoveries made while building this project.
> Every lesson was learned through implementation, troubleshooting or design decisions.

---
# Lesson 1 - Validate before you build

Run `sam validate` before every build to catch template issues quickly.

---

# Lesson 2 - Build before you deploy

Use the workflow: validate → build → local invoke → deploy.

---

# Lesson 3 - `sam build` is local

`sam build` packages artifacts locally and does not require AWS credentials.

---

# Lesson 4 - `sam deploy` needs credentials

Deployment interacts with CloudFormation and requires valid AWS credentials.

---

# Lesson 5 - Docker simulates Lambda

SAM Local simulates the Lambda runtime using Docker.

---

# Lesson 6 - Docker does not simulate IAM

AWS SDK calls use your local credentials, not the Lambda execution role.

---

# Lesson 7 - Two CloudFormation stacks

SAM creates a managed infrastructure stack and the application stack.

---

# Lesson 8 - Managed stack purpose

The managed stack stores deployment artifacts in an S3 bucket.

---

# Lesson 9 - Application stack purpose

The application stack contains Lambda, API Gateway and IAM resources.

---

# Lesson 10 - ROLLBACK_COMPLETE

Stacks in `ROLLBACK_COMPLETE` must be deleted before redeployment.

---

# Lesson 11 - Least privilege is iterative

Missing permissions are discovered incrementally during deployment.

---

# Lesson 12 - Read CloudFormation events

Stack events usually identify the missing permission precisely.

---

# Lesson 13 - Assume role again

After changing a role policy, re-assume the role to refresh credentials.

---

# Lesson 14 - Lambda includes boto3

The runtime already includes boto3.

---

# Lesson 15 - Install boto3 locally

Install boto3 in the virtual environment for IDE support.

---

# Lesson 16 - Virtual environments matter

Create `.venv` before serious development.

---

# Lesson 17 - Separate local and cloud

Local development and AWS execution use different environments.

---

# Lesson 18 - Use Globals

SAM Globals reduce duplication.

---

# Lesson 19 - One resource first

Build one API resource completely before expanding.

---

# Lesson 20 - Keep milestones small

Finish one feature end-to-end before adding another.

---

# Lesson 21 - Design the API first

Agree on request/response contracts before coding.

---

# Lesson 22 - camelCase externally

JSON and JavaScript use camelCase.

---

# Lesson 23 - snake_case internally

Python variables follow PEP 8.

---

# Lesson 24 - Translate only

Grant only `translate:TranslateText` for Version 1.

---

# Lesson 25 - Policies belong to the function

Execution policies live under the Lambda resource.

---

# Lesson 26 - Validate policy syntax

Run `sam validate` after IAM changes.

---

# Lesson 27 - Local test events

Store sample payloads under `events/`.

---

# Lesson 28 - Proxy integration

API Gateway passes the body as a JSON string.

---

# Lesson 29 - Parse request body

Use `json.loads(event['body'])`.

---

# Lesson 30 - Reuse boto3 clients

Create SDK clients outside the handler.

---

# Lesson 31 - Handle client errors

Return HTTP 400 for invalid requests.

---

# Lesson 32 - Handle server errors

Return HTTP 500 for unexpected failures.

---

# Lesson 33 - Cloud outputs help

Expose useful values through CloudFormation Outputs.

---

# Lesson 34 - Commit by milestone

Commit stable checkpoints, not every experiment.

---

# Lesson 35 - Treat errors as documentation

AWS errors often tell you exactly what is missing.

---

# Lesson 36 - Avoid AdministratorAccess

Understand permissions before broadening them.

---

# Lesson 37 - Test locally first

Fix logic before involving deployment.

---

# Lesson 38 - Deployment validates infrastructure

Cloud deployment verifies IAM and resource creation.

---

# Lesson 39 - Understand before optimizing

Clarity beats cleverness in early milestones.

---

# Lesson 40 - Keep the architecture simple

Add one AWS service at a time.

---

# Lesson 41 - Document discoveries

Record lessons while they are fresh.

---

# Lesson 42 - Repository organization matters

A clean structure speeds development.

---

# Lesson 43 - Use diagrams

Architecture diagrams clarify every milestone.

---

# Lesson 44 - One responsibility per function

Keep Lambda focused.

---

# Lesson 45 - Security is part of development

Least privilege is designed, not added later.

---

# Lesson 46 - Small successes compound

End-to-end working increments build confidence.

---

# Lesson 47 - Naming consistency

Follow each language's conventions.

---

# Lesson 48 - Infrastructure first

A stable foundation accelerates feature development.

---

# Lesson 49 - Engineering is learning

Every deployment teaches something if investigated.

---
