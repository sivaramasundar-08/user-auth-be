import time
from sqlalchemy import and_
from sqlalchemy.exc import (
    IntegrityError,
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session

from app.models import UserConfigModel, DynamicModelGenerator
from app.schemas import LoginRequestSchema, UserRequestSchema, UserStatusRequestSchema
from app.utils import logger, generate_password_hash


class UserDatabase:
    @staticmethod
    def user_signup(user_data: UserRequestSchema, session: Session) -> UserConfigModel:
        function_name: str = "Create User Database"
        logger.info(f"Enter - {function_name}")
        try:
            user_config_model = DynamicModelGenerator.generate_user_config_model()
            filter_value = [
                user_config_model.user_email == user_data.email,
                user_config_model.is_active == 1,
            ]
            user_detail = session.query(user_config_model).filter(*filter_value).first()
            if user_detail:
                raise ValueError("User details already exist")

            user_object = user_config_model()
            user_object.is_active = 1
            user_object.created_at = int(time.time())
            user_object.updated_at = int(time.time())
            user_object.user_email = user_data.email
            user_object.username = user_data.username
            user_object.phone_number = user_data.phone_number
            user_object.password = generate_password_hash(user_data.password)
            session.add(user_object)
            session.commit()
            logger.info(f"Exit - {function_name}")
            return user_object
        except (
            NoSuchTableError,
            ProgrammingError,
            NoSuchColumnError,
            OperationalError,
            IntegrityError,
        ) as not_unique_error:
            logger.error(
                f"Exit {function_name} Exception occurred: {str(not_unique_error)}",
                )
            raise not_unique_error

    @staticmethod
    def login_user(user_data: LoginRequestSchema, session: Session) -> UserConfigModel:
        function_name: str = "Login User Database"
        logger.info(f"Enter - {function_name}")
        try:
            user_config_model = DynamicModelGenerator.generate_user_config_model()
            user_object = session.query(user_config_model).filter(
                    and_(
                        user_config_model.user_email == user_data.email,
                        user_config_model.is_active == 1,
                    ),
                ).first()
            if not user_object:
                raise ValueError("User not found")
            return user_object
        except (
            NoSuchTableError,
            ProgrammingError,
            NoSuchColumnError,
            OperationalError,
        ) as does_not_exist_error:
            logger.error(
                f"Exit {function_name} Exception occurred: {str(does_not_exist_error)}",
                )
            raise does_not_exist_error

