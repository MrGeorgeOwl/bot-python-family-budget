from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init_db(engine):
    Base.metadata.create_all(engine)

def config_session(engine):
    session = sessionmaker()
    session.configure(bind=engine)
    return session

def config_engine(base_dir: str):
    engine = create_engine(f'sqlite:////{base_dir}')
    return engine