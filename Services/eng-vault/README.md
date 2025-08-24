# eng-vault Service

## Purpose

The `eng-vault` service is the secure document storage solution for the AssetArc platform. It is responsible for:

*   Handling file uploads from authenticated users.
*   Storing files securely in a configurable backend (e.g., local file system, S3, Google Cloud Storage).
*   Associating uploaded files with the user who uploaded them.
*   Serving files back to authorized users for download.
*   Ensuring that users can only access their own files.

## API Endpoints

*   `POST /vault/upload`: Uploads a file to the vault. The user is identified by their access token.
*   `GET /vault/files`: Lists all the files owned by the currently authenticated user.
*   `GET /vault/download/<file_id>`: Downloads a specific file by its ID. The service checks that the requester is the owner of the file.

## Environment Variables

*   `SQLALCHEMY_DATABASE_URI`: The connection string for the database, used to store file metadata (owner, filename, etc.).
*   `UPLOAD_FOLDER`: The path to the directory where uploaded files will be stored (for local storage).
*   `ENG_IDENTITY_URL`: The URL for the `eng-identity` service, used to validate access tokens.
*   **(Cloud Storage Variables)**: Depending on the storage backend configured, you may also need variables for cloud credentials (e.g., `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME`).

## Running Locally

1.  Create a `.env` file in the `app/` directory and populate it with the required environment variables.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the Flask development server: `python app.py`.

The service will be available at `http://localhost:5002`.
