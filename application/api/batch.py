from application import session_scope
from application.model.batch import Batch, BatchUseCaseRelation


def add_batch(**kwargs):
    with session_scope() as session:
        batch = Batch(**kwargs)
        session.add(batch)


def get_batch(**kwargs):
    with session_scope() as session:
        query = session.query(Batch).filter_by(**kwargs).filter_by(status=1)
    batch_list = [s_batch for s_batch in query]
    return batch_list


def modify_batch(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Batch).filter_by(id=id).update(kwargs)


def del_batch(**kwargs):
    with session_scope() as session:
        id = kwargs.pop('id')
        session.query(Batch).filter_by(id=id).update({'status': 0})
        session.query(BatchUseCaseRelation).filter_by(batch_id=id).update({'status': 0})


def add_batch_use_case_relation(batch_id, use_case_id):
    with session_scope() as session:
        batchUseCaseRelation = BatchUseCaseRelation(batch_id, use_case_id)
        session.add(batchUseCaseRelation)


def get_batch_use_case_relation(**kwargs):
    with session_scope() as session:
        query = session.query(BatchUseCaseRelation).filter_by(**kwargs).filter_by(status=1)
    batch_use_case_relation_list = [b_use_case.to_dict() for b_use_case in query]
    return batch_use_case_relation_list


def del_batch_use_case_relation(batch_id, use_case_id):
    with session_scope() as session:
        session.query(BatchUseCaseRelation).\
            filter_by(batch_id=batch_id).filter_by(use_case_id=use_case_id).update({'status': 0})