import os
from google.cloud import secretmanager

# In-memory cache for secrets
_cache = {}

def get_secret(secret_id: str, project_id: str = None) -> str | None:
    """
    Retrieves a secret from Google Cloud Secret Manager.
    Caches the secret in memory to avoid repeated API calls.
    """
    if secret_id in _cache:
        return _cache[secret_id]

    gcp_project_id = project_id or os.getenv('GCP_PROJECT_ID')
    if not gcp_project_id:
        # This allows the app to function locally without real secrets
        # by falling back to environment variables if the project ID isn't set.
        return os.getenv(secret_id.upper())

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{gcp_project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        _cache[secret_id] = secret_value
        return secret_value
    except Exception as e:
        # In a real application, you'd want more robust logging here.
        print(f"Could not retrieve secret '{secret_id}'. Error: {e}")
        # Fallback to environment variable if secret retrieval fails
        return os.getenv(secret_id.upper())
