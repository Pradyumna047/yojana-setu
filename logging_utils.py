import json
import random
from datetime import datetime, timedelta

BUCKET_NAME = "yojana-bucket-yojana-setu-logs"
LOG_FILE_PATH = "logs/yojana_logs.json"

_local_fallback_logs = []
_use_gcs = True
storage_client = None

# Attempt GCS initialization; fall back gracefully to memory if offline/unauthorized
try:
    from google.cloud import storage
    storage_client = storage.Client()
except Exception as e:
    _use_gcs = False
    print(f"[Yojana Setu] GCS Client failed to initialize. Offline fallback active: {e}")

def _get_bucket():
    if not _use_gcs or storage_client is None:
        return None
    return storage_client.bucket(BUCKET_NAME)

def _get_blob():
    bucket = _get_bucket()
    if bucket is None:
        return None
    return bucket.blob(LOG_FILE_PATH)

def initialize_log_file():
    if not _use_gcs:
        return
    try:
        blob = _get_blob()
        if blob and not blob.exists():
            blob.upload_from_string("[]", content_type="application/json")
    except Exception as e:
        print(f"[Yojana Setu] Failed to initialize log file on GCS: {e}")

def generate_seed_data(count=100):
    """Generates mock historical data to populate the charts initially."""
    schemes = ["PM-JAY", "PMUY", "Sukanya Samriddhi", "General Inquiry"]
    states = ["Maharashtra", "Delhi", "Uttar Pradesh", "Bihar", "Karnataka", "Tamil Nadu"]
    languages = ["English", "Hindi", "Marathi", "Kannada", "Tamil"]
    
    seed_logs = []
    base_time = datetime.utcnow()
    
    for _ in range(count):
        timestamp = (base_time - timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )).isoformat()
        
        seed_logs.append({
            "timestamp": timestamp,
            "query": "Seed Inquiry",
            "scheme": random.choice(schemes),
            "eligible": random.choice([True, True, False]), # ~66% eligibility
            "state": random.choice(states),
            "language": random.choice(languages)
        })
    return seed_logs

def append_log_entry(query, scheme, eligible, state, language):
    global _local_fallback_logs
    
    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "scheme": scheme,
        "eligible": eligible,
        "state": state,
        "language": language
    }

    if _use_gcs:
        try:
            initialize_log_file()
            blob = _get_blob()
            if blob:
                raw = blob.download_as_text()
                logs = json.loads(raw) if raw.strip() else []
                logs.append(new_entry)
                blob.upload_from_string(
                    json.dumps(logs, indent=2),
                    content_type="application/json"
                )
                return
        except Exception as e:
            print(f"[Yojana Setu] GCS write error. Appending locally: {e}")
            
    _local_fallback_logs.append(new_entry)

def fetch_all_logs():
    global _local_fallback_logs
    logs = []

    if _use_gcs:
        try:
            initialize_log_file()
            blob = _get_blob()
            if blob:
                raw = blob.download_as_text()
                logs = json.loads(raw) if raw.strip() else []
        except Exception as e:
            print(f"[Yojana Setu] GCS read error. Reading from local memory fallback: {e}")
            logs = _local_fallback_logs
    else:
        logs = _local_fallback_logs

    # Merge seed data to ensure the admin dashboard is populated from the start
    if len(logs) < 50:
        seed_count = 100 - len(logs)
        seeded = generate_seed_data(seed_count)
        return seeded + logs
        
    return logs