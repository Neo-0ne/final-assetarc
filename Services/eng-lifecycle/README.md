# eng-lifecycle Service

## Purpose

The `eng-lifecycle` service acts as the primary orchestrator for complex, multi-step workflows within the AssetArc platform. It is responsible for:

*   Handling requests for document pack generation (`/lifecycle/pack`). This involves coordinating calls to `eng-drafting` to render individual documents and `eng-vault` to store the final zipped package.
*   Managing the business logic for corporate structure design (`/lifecycle/design`).
*   Handling public-facing form submissions, such as the contact form (`/api/v1/contact`) and newsletter subscriptions (`/api/v1/subscribe`), and delegating the necessary actions to other services.
*   Serving as the source of truth for client lifecycle data for the Advisor Dashboard (though this part is still under development).

## API Endpoints

### Core Lifecycle
*   `POST /lifecycle/design`: Designs a corporate structure based on user goals and jurisdiction.
*   `POST /lifecycle/pack`: Generates a complete document package for a given workflow. This is a protected endpoint that requires user authentication.

### Public Forms
*   `POST /api/v1/contact`: Handles submissions from the public contact form. Protected by an internal API key.
*   `POST /api/v1/subscribe`: Handles newsletter subscription requests. Protected by an internal API key.

### Advisor Data
*   `GET /api/v1/clients`: Returns a list of clients for a given advisor. Protected by an internal API key. (Currently returns placeholder data).

## Environment Variables

*   `DRAFTING_SERVICE_URL`: The URL for the `eng-drafting` service.
*   `VAULT_SERVICE_URL`: The URL for the `eng-vault` service.
*   `ENG_ANALYTICS_URL`: The URL for the `eng-analytics` service.
*   `SQLALCHEMY_DATABASE_URI`: The connection string for the database (used for storing newsletter subscribers and lifecycle data).
*   `INTERNAL_SERVICE_API_KEY`: A secret key for protecting internal system-to-system API calls.
*   `ENG_IDENTITY_URL`: The URL for the `eng-identity` service (used for delegating email sending).
*   `ADMIN_EMAIL`: The email address to which contact form submissions are sent.

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5005`.
