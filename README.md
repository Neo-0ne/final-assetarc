# AssetArc - Legal & Structuring Automation Suite

AssetArc is a comprehensive legal-tech platform designed to automate and streamline the process of corporate and trust structuring, tax compliance, and asset protection. It is built on a modern microservices architecture, providing a scalable and maintainable solution for entrepreneurs, advisors, and HNWIs.

## Architecture Overview

The platform is composed of a set of independent, single-responsibility services (the `eng-*` services) that communicate with each other via REST APIs. This architecture allows for independent development, deployment, and scaling of each component of the system.

A WordPress frontend provides the user interface, interacting with the backend services through an API gateway (though the gateway is not yet fully implemented in the current phase).

## Services

The backend is comprised of the following 8 core microservices:

*   **eng-identity:** Manages user identity, authentication (OTP, JWT), and system-wide email sending.
*   **eng-lifecycle:** Orchestrates complex, multi-step workflows like document pack generation and form submissions.
*   **eng-billing:** Handles all pricing, quoting, subscriptions, and payment integrations (Stripe, Yoco).
*   **eng-vault:** Provides secure, authenticated storage and retrieval of user documents.
*   **eng-drafting:** Renders `.docx` and `.html` templates with dynamic data.
*   **eng-engagement:** Manages user engagement, primarily through booking and calendar integrations (Cal.com).
*   **eng-analytics:** A central service for ingesting events and tracking metrics across the platform.
*   **eng-compliance:** Handles various compliance checks and business logic related to legal and financial regulations.

Each service has its own detailed `README.md` file with information about its API, environment variables, and how to run it individually.

## Getting Started

### Prerequisites

*   Docker and Docker Compose
*   Python 3.10+ and `pip`
*   A running Redis instance
*   AWS credentials configured for SES (for email sending)
*   API keys for any third-party services you wish to use (e.g., Stripe, Yoco, Cal.com).

### Running the Platform

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Set up environment variables:**
    Each service in the `eng-*` directories requires its own `.env` file. Copy the `.env.example` file (if one exists) to `.env` in each service's `app/` directory and fill in the required values. At a minimum, you will need to set up the `INTERNAL_SERVICE_API_KEY` and the database URIs.

3.  **Run the services with Docker Compose:**
    The `Docker-compose.integrated.yml` file is configured to run all the `eng-*` services together.
    ```bash
    docker-compose -f Docker-compose.integrated.yml up --build
    ```
    This will build the Docker images for each service and start them. The services will be available on their respective ports (e.g., `eng-identity` on `localhost:5000`, `eng-billing` on `localhost:5003`, etc.).

### Running Tests

To run the tests for all services, you can run the following command from the root of the repository. This will discover and run all tests in the `eng-*/tests/` directories.

```bash
python -m pytest eng-*/tests/
```

Note: This may cause import issues due to the test files all being named `test_app.py`. It is more reliable to run the tests for each service individually:

```bash
cd eng-identity
python -m pytest
cd ../eng-billing
python -m pytest
# ... and so on for all services
```

## WordPress Theme

The WordPress frontend is located in the `assetarc-theme` directory. See the `WordPress_Deployment_Guide.docx` file for instructions on how to set up and deploy the theme.
