import os
import sys
import uuid
import datetime
from flask import Flask, jsonify, request
from google.cloud import storage
from sqlalchemy import create_engine, text
from auth_decorator import require_auth_from_identity

app = Flask(__name__)

# --- Add common module to path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'common')))
from secrets import get_secret

# --- Configuration ---
GCS_BUCKET_NAME = get_secret('gcs-bucket-name') or 'assetarc-vault-dev'
DB_URI = get_secret('postgres-uri') or get_secret('sqlalchemy-database-uri') or 'sqlite:///eng_vault.db'

# --- Service Initialization ---
try:
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
except Exception as e:
    storage_client = None
    bucket = None
    app.logger.error(f"Could not initialize Google Cloud Storage client: {e}")

engine = create_engine(DB_URI, future=True)

# --- Database Setup ---
def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                gcs_path TEXT NOT NULL,
                filename TEXT NOT NULL,
                content_type TEXT,
                uploaded_at DATETIME
            )
        """))

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True


@app.route('/')
def index():
    return jsonify({
        "service": "eng-vault",
        "status": "running",
        "gcs_initialized": storage_client is not None
    })

@app.route('/vault/upload', methods=['POST'])
@require_auth_from_identity()
def upload_file():
    if not bucket:
        return jsonify({"error": "Storage service not initialized"}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    user_id = request.current_user.get('email')
    if not user_id:
        # This should not happen if the decorator is working
        return jsonify({"error": "Could not identify user from token"}), 401

    file_id = str(uuid.uuid4())
    gcs_filename = f"uploads/{user_id}/{file_id}/{file.filename}"

    try:
        blob = bucket.blob(gcs_filename)
        blob.upload_from_file(file.stream, content_type=file.content_type)

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO files (id, user_id, gcs_path, filename, content_type, uploaded_at)
                VALUES (:id, :user_id, :gcs_path, :filename, :content_type, :uploaded_at)
            """), {
                "id": file_id,
                "user_id": user_id,
                "gcs_path": gcs_filename,
                "filename": file.filename,
                "content_type": file.content_type,
                "uploaded_at": datetime.datetime.now(datetime.timezone.utc)
            })

        return jsonify({"file_id": file_id}), 201

    except Exception as e:
        app.logger.error(f"Error uploading file to GCS: {e}")
        return jsonify({"error": "Failed to upload file"}), 500


@app.route('/vault/file/<string:id>', methods=['GET'])
@require_auth_from_identity()
def get_file_url(id):
    if not bucket:
        return jsonify({"error": "Storage service not initialized"}), 503

    user_id = request.current_user.get('email')

    with engine.connect() as conn:
        file_info = conn.execute(
            text("SELECT gcs_path, user_id FROM files WHERE id = :id"),
            {"id": id}
        ).first()

    if not file_info:
        return jsonify({"error": "File not found"}), 404

    # Authorization check: ensure the user owns the file
    if file_info.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    try:
        blob = bucket.blob(file_info.gcs_path)

        # Generate a signed URL that is valid for 1 hour.
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(hours=1),
            method="GET",
        )

        return jsonify({"url": signed_url})

    except Exception as e:
        app.logger.error(f"Error generating signed URL for file {id}: {e}")
        return jsonify({"error": "Could not generate file URL"}), 500

if __name__ == '__main__':
    # For local development. Gunicorn will be used in production.
    app.run(debug=True, host='0.0.0.0', port=5002)
