from sqlmodel import create_engine, SQLModel

from db.models import Message, Conversation


def new_engine(uri: str = "sqlite:///htmxgpt.db"):
    engine = create_engine(uri)
    SQLModel.metadata.create_all(engine)
    return engine
