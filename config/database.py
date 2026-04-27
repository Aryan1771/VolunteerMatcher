from google.cloud import firestore


_db = None


def get_db():
    """Create one shared Firestore client and reuse it for every request."""
    global _db

    if _db is None:
        _db = firestore.Client()

    return _db


def get_collection(name):
    return get_db().collection(name)


def snapshot_to_dict(snapshot):
    data = snapshot.to_dict()
    if data is None:
        return None

    data["_id"] = snapshot.id
    return data


def create_document(collection_name, data):
    _, document_ref = get_collection(collection_name).add(data)
    data["_id"] = document_ref.id
    return data


def get_document(collection_name, document_id):
    snapshot = get_collection(collection_name).document(document_id).get()
    if not snapshot.exists:
        return None

    return snapshot_to_dict(snapshot)


def list_documents(collection_name, order_by=None, descending=False):
    query = get_collection(collection_name)

    if order_by:
        direction = firestore.Query.DESCENDING if descending else firestore.Query.ASCENDING
        query = query.order_by(order_by, direction=direction)

    return [snapshot_to_dict(snapshot) for snapshot in query.stream()]


def update_document(collection_name, document_id, data):
    document_ref = get_collection(collection_name).document(document_id)
    if not document_ref.get().exists:
        return None

    document_ref.update(data)
    return get_document(collection_name, document_id)


def delete_document(collection_name, document_id):
    document_ref = get_collection(collection_name).document(document_id)
    if not document_ref.get().exists:
        return False

    document_ref.delete()
    return True
