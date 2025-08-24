# eng-engagement Service

## Purpose

The `eng-engagement` service is responsible for managing user engagement, primarily through booking and calendar integrations. Its main function is to handle requests for booking consultation slots.

This service integrates with Cal.com to create unique booking links for users, ensuring a seamless scheduling experience.

## API Endpoints

*   `POST /engage/booking/slot`: Creates a unique Cal.com booking link for a consultation. This is a protected endpoint that requires user authentication.

## Environment Variables

*   `CAL_COM_API_KEY`: Your API key for the Cal.com service.
*   `ENG_IDENTITY_URL`: The URL for the `eng-identity` service, used to validate access tokens.
*   `ENG_ANALYTICS_URL`: The URL for the `eng-analytics` service.

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5006`.
