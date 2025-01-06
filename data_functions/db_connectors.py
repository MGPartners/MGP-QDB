from google.cloud import firestore

def store_to_firestore(project_name: str, collection_name: str, document_id: str, data: dict):
    db = firestore.Client(project=project_name)
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
