import json
from google.cloud import storage
from datetime import datetime

BUCKET_NAME = "yojana-bucket-yojana-setu-logs"
LOG_FILE_PATH = "logs/yojana_logs.json"

storage_client = storage.Client()

def _get_bucket():
    return storage_client.bucket(BUCKET_NAME)

def _get_blob():
    bucket = _get_bucket()
    return bucket.blob(LOG_FILE_PATH)

def initialize_log_file():
    blob = _get_blob()
    if not blob.exists():
        blob.upload_from_string("[]", content_type="application/json")

def append_log_entry(query, scheme, eligible, state, language):
    initialize_log_file()
    blob = _get_blob()

    raw = blob.download_as_text()
    logs = json.loads(raw) if raw.strip() else []

    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "scheme": scheme,
        "eligible": eligible,
        "state": state,
        "language": language
    }

    logs.append(new_entry)

    blob.upload_from_string(
        json.dumps(logs, indent=2),
        content_type="application/json"
    )

def fetch_all_logs():
    initialize_log_file()
    blob = _get_blob()

    raw = blob.download_as_text()
    logs = json.loads(raw) if raw.strip() else []

    return logs
