from sqlalchemy.exc import (
    IntegrityError,
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session

from app.config import access_token
from app.database import UserDatabase
from app.exceptions import PasswordDidNotMatchException, InvalidPasswordException
from app.models import UserConfigModel
from app.schemas import (
    AuthResponseSchema,
    LoginRequestSchema,
    UserDataSchema,
    UserRequestSchema,
    UserStatusRequestSchema,
)
from app.schemas import CommonResponseSchema
from app.utils import logger, verify_password_hash, validate_email, validate_password

EXPIRY_TIME: int = 1440


class UserService:
    @staticmethod
    def user_signup(
        user_data: UserRequestSchema, session: Session
    ) -> AuthResponseSchema:
        function_name: str = "Create User Service"
        logger.info(f"Enter - {function_name}")
        try:
            if not validate_email(user_data.email):
                raise ValueError("Provided email is not valid")
            if not validate_password(user_data.password):
                raise InvalidPasswordException()
            user_object: UserConfigModel = UserDatabase.user_signup(user_data, session)
            logger.info(f"Exit - {function_name}")
            user_data: UserDataSchema = UserDataSchema(
                email=user_object.user_email,
                username=user_object.username,
            )
            return AuthResponseSchema(
                message="User login created successfully",
                data=user_data,
                access_token=access_token.create_access_token(
                    {
                        "email": user_object.user_email,
                        "username": user_object.username,
                    },
                ),
            )
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
    def login_user(
        request_body: LoginRequestSchema, session: Session
    ) -> AuthResponseSchema:
        function_name: str = "Login User Service"
        logger.info(f"Enter - {function_name}")
        try:
            user_object: UserConfigModel = UserDatabase.login_user(request_body, session)
            is_password_match: bool = verify_password_hash(
                request_body.password, user_object.password
            )
            if is_password_match:
                user_data: UserDataSchema = UserDataSchema(
                    email=user_object.user_email,
                    username=user_object.username,
                )
                return AuthResponseSchema(
                    data=user_data,
                    access_token=access_token.create_access_token(
                        {
                            "email": user_object.user_email,
                            "username": user_object.username,
                        },
                    ),
                )
            else:
                logger.info(f"Exit - {function_name} Unauthorized")
                raise PasswordDidNotMatchException
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
        except (ValueError,) as user_not_found:
            logger.error(
                f"Exit {function_name} Exception occurred: {str(user_not_found)}",
                )
            raise user_not_found

    @staticmethod
    def validate_token(token: str) -> bool:
        function_name: str = "Validate Token Service"
        logger.info(f"Enter - {function_name}")
        try:
            logger.info(f"Exit - {function_name}")
            return access_token.validate_access_token(token)
        except (
            ValueError,
        ) as value_error:
            logger.error(f"Exit {function_name} Exception occurred: {str(value_error)}")
            raise value_error
