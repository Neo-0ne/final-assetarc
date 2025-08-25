# Guide: Setting Up Google Cloud Secret Manager for AssetArc

This guide provides step-by-step instructions to configure Google Cloud Secret Manager for the AssetArc platform. Following these steps will allow the application to securely access necessary credentials (like API keys and database URIs) in a production environment.

## Prerequisites

1.  A Google Cloud Platform (GCP) account.
2.  A GCP project created for the AssetArc application.
3.  The `gcloud` command-line tool installed and authenticated on your local machine (optional, but recommended for creating secrets).

---

## Step 1: Enable the Secret Manager API

Before you can use Secret Manager, you must enable the API for your project.

1.  Navigate to the [Secret Manager API page](https://console.cloud.google.com/apis/library/secretmanager.googleapis.com) in the Google Cloud Console.
2.  Select your AssetArc project from the dropdown menu.
3.  Click the **"Enable"** button.

---

## Step 2: Create a Dedicated Service Account

It is a best practice to create a dedicated service account for applications to access cloud resources, rather than using your personal account.

1.  In the Cloud Console, navigate to **IAM & Admin > Service Accounts**.
2.  Click **"+ CREATE SERVICE ACCOUNT"**.
3.  **Service account name:** `assetarc-secrets-accessor`
4.  **Service account ID:** This will be automatically generated.
5.  **Description:** "Service account for AssetArc backend services to access secrets."
6.  Click **"CREATE AND CONTINUE"**.

---

## Step 3: Grant Permissions

Grant the newly created service account the necessary permissions to access secrets.

1.  In the "Grant this service account access to project" step, click the **"Role"** dropdown.
2.  Search for and select the **"Secret Manager Secret Accessor"** role. This role provides the minimum required permissions for the application to read secret values.
3.  Click **"CONTINUE"**, and then click **"DONE"**.

---

## Step 4: Generate a Service Account Key

The application will use a JSON key file to authenticate as the service account.

1.  Go back to the **Service Accounts** page.
2.  Find the `assetarc-secrets-accessor` service account and click on it.
3.  Go to the **"KEYS"** tab.
4.  Click **"ADD KEY" > "Create new key"**.
5.  Select **"JSON"** as the key type and click **"CREATE"**.
6.  A JSON file will be downloaded to your computer. **Treat this file like a password; it is highly sensitive.** Do not commit it to version control.

---

## Step 5: Configure the Application Environment

The application needs two environment variables to be set to use this key:

1.  **`GCP_PROJECT_ID`**: Set this to the ID of your Google Cloud project (e.g., `assetarc-platform-12345`).
2.  **`GOOGLE_APPLICATION_CREDENTIALS`**: Set this to the absolute path of the JSON key file you downloaded in the previous step.

When running with Docker, you will need to mount the key file into the containers and set these environment variables. The `docker-compose.integrated.yml` should be modified to support this.

Example `docker-compose.yml` service definition:

```yaml
services:
  eng-identity:
    # ... other service config
    environment:
      - GCP_PROJECT_ID=your-gcp-project-id
      - GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcp_service_account.json
    volumes:
      - /path/to/your/downloaded-key.json:/run/secrets/gcp_service_account.json:ro
```
*Note: The `:ro` flag makes the mounted file read-only inside the container, which is a good security practice.*

---

## Step 6: Create the Necessary Secrets

You must create the following secrets in Secret Manager. You can do this via the Cloud Console or the `gcloud` CLI. The secret names (Secret ID) must match exactly.

**Command to create a secret:**
`gcloud secrets create [SECRET_ID] --replication-policy="automatic" --data-file="/path/to/file/with/secret/value.txt"`
Or to pipe the value directly:
`echo "my-secret-value" | gcloud secrets create [SECRET_ID] --replication-policy="automatic" --data-file=-`

**Required Secrets:**

*   `jwt-secret`: A long, random string for signing JWTs.
*   `access-token-ttl-min`: Default: `15`
*   `refresh-token-ttl-days`: Default: `30`
*   `otp-ttl-min`: Default: `10`
*   `cookie-secure`: `True` for production, `False` for local.
*   `cookie-domain`: Your production domain (e.g., `.asset-arc.com`).
*   `postgres-uri`: The connection string for the production PostgreSQL database.
*   `sender-email`: The email address for sending transactional emails (e.g., `noreply@asset-arc.com`).
*   `aws-region`: The AWS region for SES/S3 if used.
*   `eng-analytics-url`: The public URL of the analytics service.
*   `internal-service-api-key`: A shared secret for internal service-to-service communication.
*   `analytics-db-uri`: The connection string for the analytics database.
*   `sqlalchemy-database-uri`: (Alternative to `postgres-uri`).
