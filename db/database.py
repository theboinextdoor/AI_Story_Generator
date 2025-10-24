from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings

#! engine is your main link to the database
engine = create_engine(settings.DATABASE_URL)

#! It helps create “sessions” — temporary workspaces to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#! This is the starting point for your table definitions.
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#! This looks at all the classes that inherit from Base and creates their tables in the database
def create_table():
    Base.metadata.create_all(bind=engine)
