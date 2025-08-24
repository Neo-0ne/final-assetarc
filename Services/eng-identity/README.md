# eng-identity Service

## Purpose

The `eng-identity` service is the central identity and authentication provider for the AssetArc platform. It is responsible for:

*   User management (creation, roles, status).
*   Authentication via One-Time Passwords (OTPs) sent over email.
*   Issuing and validating JWTs (access and refresh tokens).
*   Securely managing user sessions.
*   Providing a secure endpoint for other backend services to send system-level emails.
*   Handling advisor-specific functionality, such as requesting and managing client access tokens.
*   Serving as a data aggregator for the Advisor Dashboard.

## API Endpoints

### Authentication
*   `POST /auth/request-otp`: Initiates the login process by sending an OTP to the user's email.
*   `POST /auth/verify-otp`: Verifies the OTP and, if successful, returns JWTs in secure cookies.
*   `POST /auth/refresh`: Refreshes an expired access token using a valid refresh token.
*   `POST /auth/logout`: Logs the user out by invalidating their refresh token.
*   `GET /auth/user`: Returns the details of the currently authenticated user.

### Advisor Tools
*   `POST /api/v1/advisor/request-client-token`: Allows an authenticated advisor to request a single-use access token for a client.
*   `GET /api/v1/advisor/dashboard`: Provides aggregated data for the advisor dashboard, including client lists and stats.

### System
*   `POST /api/v1/send-system-email`: A protected endpoint for other backend services to send emails (e.g., contact form submissions).

### Gateway
*   `GET /gateway/routes`: Provides a service discovery map for the API gateway.

## Environment Variables

*   `JWT_SECRET`: A secret key for signing JWTs.
*   `ACCESS_TOKEN_TTL_MIN`: The time-to-live for access tokens in minutes.
*   `REFRESH_TOKEN_TTL_DAYS`: The time-to-live for refresh tokens in days.
*   `OTP_TTL_MIN`: The time-to-live for OTPs in minutes.
*   `COOKIE_SECURE`: Set to `True` in production to send cookies over HTTPS only.
*   `COOKIE_DOMAIN`: The domain for the cookies.
*   `POSTGRES_URI` or `SQLALCHEMY_DATABASE_URI`: The connection string for the database.
*   `SENDER_EMAIL`: The "From" address for emails sent by the service.
*   `AWS_REGION`: The AWS region for the SES service.
*   `INTERNAL_SERVICE_API_KEY`: A secret key for protecting internal system-to-system API calls.
*   `ADMIN_EMAIL`: The email address to which contact form submissions are sent.
*   `ENG_*_URL`: URLs for the other backend services (used for data aggregation).

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5000`.
