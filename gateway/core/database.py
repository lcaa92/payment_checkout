import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

engine = create_engine(os.getenv("DATABASE_URL", "postgresql://"))


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
