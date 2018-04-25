from application import session_scope
from application.model.encryption import Encryption


def get_encryption_list():
    with session_scope() as session:
        query = session.query(Encryption).all()
        encryption_list = [encryption.to_dict() for encryption in query]
    return encryption_list