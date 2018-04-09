from application import session_scope
from application.model.user import User


def add_user(**kwargs):
    with session_scope() as session:
        user = User(**kwargs)
        session.add(user)
    return user.username


def get_user(**kwargs):
    with session_scope() as session:
        user_list = session.query(User).filter_by(**kwargs).filter_by(status=1)
        session.expunge_all()
    return user_list


def modify_user(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(User).filter_by(id=id).update(kwargs)
    return session.query(User).filter_by(id=id).first().username


def del_user(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(User).filter_by(id=id).update({'status': 0})
    return session.query(User).filter_by(id=id).first().username
