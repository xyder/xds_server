from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from core.lib import import_models

from server.settings import ACTIVE_CONFIG

# the database engine
engine = create_engine(ACTIVE_CONFIG.SQLALCHEMY_DATABASE_URI)

# the database session
db_session = scoped_session(sessionmaker(bind=engine))

# Base model for all models
Base = declarative_base()
Base.query = db_session.query_property()
Base.recountable_models = []


def _register_recountable_model(model):
    if model not in Base.recountable_models:
        Base.recountable_models.append(model)

Base.register_recountable_model = _register_recountable_model


def recount_positions(obj, is_deleted):
    """
    Function that recounts the relative positions of the children of the parent of the given object.
    :param obj: the object for which the processing will be done
    :param is_deleted: if the bookmark is marked for deletion.
    """

    children = obj.__class__.query.filter(
        obj.__class__.parent == obj.parent
    ).order_by(obj.__class__.position.asc()).all()

    if obj in children:
        children.remove(obj)

    k = 0
    n = len(children)

    if not is_deleted:
        if obj.position is None or obj.position > n:
            obj.position = n

        if obj.position < 0:
            obj.position = 0

    for child in children:
        # skip object if not deleted
        if k == obj.position and not is_deleted:
            k += 1

        child.position = k
        k += 1


def recount_session_set(session, objects, parents, is_deleted):
    """
    Function that recounts positions for all the objects of registered classes.
    :param objects: the objects set
    :param parents: a dictionary containing the list of parents which were already processed.
    :param is_deleted: flag used if the objects are in a 'deleted' set
    :return: the updated parents dictionary
    """

    for obj in objects:
        for model in Base.recountable_models:
            if isinstance(obj, model) and obj.parent not in parents[model.__name__]:
                if session.is_modified(obj) or is_deleted:
                    recount_positions(obj, is_deleted)
                    parents[model.__name__].append(obj.parent)
    return parents


# noinspection PyUnusedLocal
def recounting_event_handler(session, flush_context, instances):
    """
    Function that runs the session objects recounter over all sets
    """

    parents = {}
    for model in Base.recountable_models:
        parents[model.__name__] = []

    parents.update(recount_session_set(session, session.new, parents, False))
    parents.update(recount_session_set(session, session.dirty, parents, False))
    recount_session_set(session, session.deleted, parents, True)


def init_db() -> None:
    """
    Initializes the database and builds tables for models if needed.
    """

    import_models()
    Base.metadata.create_all(bind=engine)
    listen(db_session, 'before_flush', recounting_event_handler)
