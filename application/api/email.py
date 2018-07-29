from application import session_scope
from application.model.email import Email


def add_email_account(**kwargs):
    with session_scope() as session:
        email = Email(**kwargs)
        session.add(email)
        session.flush()
        return email.id


def query_email_account():
    with session_scope() as session:
        query = session.query(Email)
        email_list = [email.to_dict() for email in query]
        return email_list


def del_email_account(**kwargs):
    email_id = kwargs.pop('id')
    with session_scope() as session:
        session.query(Email).filter_by(id=email_id).delete(synchronize_session=False)
