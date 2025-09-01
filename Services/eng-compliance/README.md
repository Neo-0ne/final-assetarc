# eng-compliance Service

## Purpose

The `eng-compliance` service is responsible for handling various compliance checks and business logic related to legal and financial regulations. It is designed to be a modular service where new compliance checks can be added easily.

Its current responsibilities include:
*   Assessing eligibility for SARS Section 47 rollover relief.
*   Performing FICA risk tiering based on client data (e.g., PEP status, transaction volume).
*   (Future) Performing a simplified Solvency and Liquidity test as per the Companies Act.

## API Endpoints

*   `POST /compliance/run`: Runs a specific compliance module. The request body should contain the `module_id` and the necessary `data` for the check.

## Environment Variables

*   `ENG_ANALYTICS_URL`: The URL for the `eng-analytics` service.

## Running Locally

1.  Install the dependencies: `pip install -r requirements.txt`.
2.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5004`.
