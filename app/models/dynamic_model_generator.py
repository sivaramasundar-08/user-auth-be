from sqlalchemy.orm import declarative_base
from app.models.user_model import UserConfigModel


class DynamicModelGenerator:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def generate_user_config_model():
        base = declarative_base()

        class DynamicUserConfigModel(base, UserConfigModel):
            __tablename__ = "user_config"
            __table_args__ = {"extend_existing": True}

        return DynamicUserConfigModel

