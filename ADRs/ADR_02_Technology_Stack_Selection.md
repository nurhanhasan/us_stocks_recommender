# Architecture Decision Record 02 - Technology Stack Selection

## Date

2025-12-27

## Status

<!-- What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.? -->

Proposed: 2025-12-21

Accepted: 2025-12-27


## Context

<!-- What is the issue that we're seeing that is motivating this decision or change? -->

* **Requirements analysis and App Classification**
    - Type of application
        - [ ] Web API
        - [ ] Web app
        - [x] Background job
        - [ ] CLI
        - [x] Data pipeline

    - Scale / performance needs
        - [ ] High throughput
        - [x] Low concurrency

    - Skillset
        - [x] Familiar with vanilla Python
        - [x] Familiar with Python async (FastAPI)
        - [x] Familiar with Django
        - [x] Familiar with Flask
        - [ ] Chalice
        - [x] Serverless
        - [ ] Other frameworks?!

    - Extensibility
        - [x] Integration with ORMs (in the pipeline, not in the mvp phase)
        - [x] Integration with auth systems (in the pipeline, not in the mvp phase)
        - [x] Integration with LLMs (in the pipeline, not in the mvp phase)



* **Development Technology Options**
    - Vendor-locked framework
      * Chalice           - Limited features, AWS-specific
      * FastAPI + Mangum  - Not AWS-native


    - Vendor-agnostic framework
      * Serverless Framework                    - Huge ecosystem, More config-heavy
      * Vanilla Python script in a Container    - Deploy anywhere: VPS, AWS ECS/Fargate, Google Cloud Run, Azure Container Apps
      * FastAPI in a Container                  - Deploy anywhere: VPS, AWS ECS/Fargate, Google Cloud Run, Azure Container Apps


* **Deployment and Hosting options**
    1. A serverless container Service. Billing based on execution time and resource allocation (CPU/memory).
    2. A VPS hosting the containers. Degraded performance, but fixed monthly cost (5-10$ monthly). 


## Decision

<!-- What is the change that we're proposing and/or doing? -->

* I'll go with Vanilla Python script in a Container alongside n8n and maybe ngrok for the MVP.
    - Core logic:
      * Vanilla Python script/fastAPI simple app.

    - Scheduling:
      * n8n cron/workflow node where n8n scheduler triggers the script periodically according to the configured cron.

    - Notification:
      - n8n Telegram node sends a message based on the python script condition check.

* Deploy as docker/docker-compose on an AWS Lightsail VPS.


## Consequences

<!-- What becomes easier or more difficult to do because of this change? -->

### Positive Consequences:
* This stack is simple enough to support the first feature (getting notified by a screener based on specific criteria).

### Negative / Future Considerations:
* The currently selected stack, however, will not be sufficient for the next steps, which may require integration with LLMs and secured layer for authentication with the broker for orders execution.