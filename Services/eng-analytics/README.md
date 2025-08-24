# eng-analytics Service

## Purpose

The `eng-analytics` service is the central event tracking and metrics aggregation service for the AssetArc platform. It provides a single point for other services to send events and for the frontend to query analytics data.

Its key responsibilities are:
*   Ingesting events from all other microservices.
*   Storing events in a database.
*   Providing endpoints to query aggregated analytics data and Key Performance Indicators (KPIs).
*   Serving a simple HTML dashboard to visualize the KPIs.

## API Endpoints

*   `POST /events/ingest`: The main endpoint for ingesting events from other services.
*   `GET /analytics/kpi`: Returns a set of key performance indicators.
*   `GET /analytics/dashboard`: Returns an HTML dashboard visualizing the KPIs.

## Environment Variables

*   `SQLALCHEMY_DATABASE_URI`: The connection string for the database where events are stored.

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5007`.
