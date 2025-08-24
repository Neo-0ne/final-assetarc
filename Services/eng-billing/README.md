# eng-billing Service

## Purpose

The `eng-billing` service is responsible for all pricing, quoting, and payment-related functionality within the AssetArc platform. Its key responsibilities include:

*   Providing real-time and cached foreign exchange (FX) rates.
*   Generating quotes for services.
*   Creating and managing price locks for quotes, stored in Redis with a 24-hour TTL.
*   Handling payment processing via Stripe for one-off payments.
*   Providing an endpoint for Stripe webhooks to confirm payment success.
*   Managing advisor token balances (this functionality is under development).

## API Endpoints

### Pricing & Quotes
*   `POST /pricing/quote`: Generates a quote with FX conversion.
*   `POST /pricing/lock/create`: Creates a 24-hour price lock for a quote. This is a protected endpoint.
*   `GET /pricing/lock/<lock_id>`: Retrieves a price lock by its ID.

### Payments
*   `POST /checkout/session`: Creates a Stripe checkout session for a one-time payment.
*   `POST /webhooks/stripe`: Handles incoming webhooks from Stripe to confirm payment events.

### Advisor Tokens
*   `GET /api/v1/tokens/balance`: Returns the token balance for a given advisor. Protected by an internal API key. (Currently returns placeholder data).

## Environment Variables

*   `STRIPE_API_KEY`: Your secret API key for Stripe.
*   `STRIPE_WEBHOOK_SECRET`: The secret for verifying Stripe webhooks.
*   `REDIS_URL`: The connection URL for the Redis server.
*   `ENG_ANALYTICS_URL`: The URL for the `eng-analytics` service.
*   `SQLALCHEMY_DATABASE_URI`: The connection string for the database (used for storing advisor token balances).
*   `INTERNAL_SERVICE_API_KEY`: A secret key for protecting internal system-to-system API calls.

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Ensure you have a Redis server running and accessible.
4.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5003`.
