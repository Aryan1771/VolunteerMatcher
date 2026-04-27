import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


_client = None
_db = None


def get_db():
    """Create one shared MongoDB connection and reuse it for every request."""
    global _client, _db

    if _db is not None:
        return _db

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "volunteer_matcher")

    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not configured. Add it to .env or Render environment variables.")

    try:
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        _db = _client[db_name]
        return _db
    except PyMongoError as exc:
        raise RuntimeError(f"Could not connect to MongoDB: {exc}") from exc


def get_collection(name):
    return get_db()[name]
