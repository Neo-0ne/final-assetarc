# eng-drafting Service

## Purpose

The `eng-drafting` service is a specialized microservice responsible for rendering documents and email templates for the AssetArc platform. It takes a template ID and a JSON data payload, and returns a rendered document.

Its key features are:
*   It supports rendering from `.docx` and `.html` templates using the Jinja2 templating engine.
*   It uses a `templates.json` file to map template IDs to template files and output content types.
*   It is a stateless service that can be scaled horizontally.

## API Endpoints

*   `POST /doc/render`: Renders a document by its `template_id`. The request body should contain the `template_id` and a `data` object with the context for rendering. The service responds with the rendered file and the appropriate `Content-Type` and `Content-Disposition` headers.

## Environment Variables

This service has no required environment variables, as it is self-contained. The template mapping is defined in the `templates.json` file within the service.

## Running Locally

1.  Install the dependencies: `pip install -r requirements.txt`.
2.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5001`.
