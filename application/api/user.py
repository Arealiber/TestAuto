from application import session_scope
from application.model.user import User


def add_user(**kwargs):
    with session_scope() as session:
        user = User(**kwargs)
        session.add(user)


def get_user(**kwargs):
    with session_scope() as session:
        user_list = session.query(User).filter_by(**kwargs)
        session.expunge_all()
    return user_list


def modify_user(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(User).filter_by(id=id).update(kwargs)


def del_user(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(User).filter_by(id=id).update({'status': 0})
