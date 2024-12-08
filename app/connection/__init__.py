import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy import MetaData, create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import app_config
from app.models.dynamic_model_generator import DynamicModelGenerator
from app.utils import logger


class Database:
    def __init__(self):
        self.db_url = (
            f"mysql+pymysql://{app_config.db_username}:{app_config.db_password}@{app_config.database_url}/"
            f"{app_config.db_name}?charset=utf8"
        )
        self.engine: Engine = create_engine(self.db_url, echo=True, poolclass=NullPool)
        self.session_local = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )


def get_session() -> Session:
    function_name = "Get DB"
    database = Database()
    session: Session | None = None
    try:
        session = database.session_local()
        yield session
    except (DatabaseError, TimeoutError) as exception:
        logger.error(f"Exit - {function_name} Exception occurred {exception}")
    finally:
        session.close()


def get_engine() -> Engine:
    function_name = "Get Engine"
    database: Database = Database()
    try:
        logger.info(message="Creating engine", function_name=function_name)
        return database.engine
    except (DatabaseError, TimeoutError) as exception:
        logger.error(
            message=f"Exit - {function_name} Exception occurred {exception}",
            function_name=function_name,
        )
        raise exception


def create_table_user_config():
    database = Database()
    engine = database.engine
    user_config_model = DynamicModelGenerator.generate_user_config_model()
    insp = sa.inspect(engine)
    if not insp.dialect.has_table(engine.connect(), user_config_model.__table__):  # If table don't exist, Create.
        metadata = MetaData(engine)
        metadata.create_all(
            bind=engine,
            tables=[
                user_config_model.__table__,
            ],
        )
