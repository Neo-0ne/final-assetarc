# common/secrets.py

import os

# In-memory cache for mock secrets
_mock_secrets = {
    "jwt-secret": "mock-jwt-secret-key-for-dev",
    "access-token-ttl-min": "15",
    "refresh-token-ttl-days": "30",
    "otp-ttl-min": "10",
    "cookie-secure": "False",
    "cookie-domain": "localhost",
    "postgres-uri": "sqlite:///eng_identity.db",
    "sqlalchemy-database-uri": "sqlite:///eng_identity.db",
    "analytics-db-uri": "sqlite:///eng_analytics.db",
    "sender-email": "noreply@localhost.dev",
    "aws-region": "us-east-1",
    "eng-analytics-url": "http://localhost:5007",
    "internal-service-api-key": "mock-internal-api-key"
}

def get_secret(secret_id: str, project_id: str = None) -> str | None:
    """
    Retrieves a secret from the mock secret store.
    This function is a mock for local development and testing.
    It completely bypasses Google Cloud Secret Manager.
    """
    # For development, we can also check environment variables as a fallback,
    # which can be useful for overriding specific mock values without changing the code.
    value = os.getenv(secret_id.upper())
    if value:
        return value

    return _mock_secrets.get(secret_id)
