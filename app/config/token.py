from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.config import app_config
from app.utils import logger


class AccessToken:
    @staticmethod
    def create_access_token(
        data: dict, expires_delta: timedelta = timedelta(hours=8)
    ) -> str:
        function_name = "Create Access Token"
        logger.info(f"Enter - {function_name}", function_name=function_name)
        to_encode = data.copy()
        print(datetime.utcnow())
        print(datetime.utcnow() + expires_delta)
        print(expires_delta)
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=720)
        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(
            to_encode, app_config.secret_key, algorithm=app_config.algorithm
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        function_name = "Decode Access Token"
        logger.info(f"Enter - {function_name}", function_name=function_name)
        try:
            if token:
                decoded_token: dict = jwt.decode(
                    token, app_config.secret_key, algorithms=[app_config.algorithm]
                )
                return decoded_token
            else:
                raise ValueError("Please provide a valid access token")
        except (
            ValueError,
        ) as jwt_error:
            logger.error(
                f"Exit - {function_name} Exception Occurred {jwt_error}",
                )
            raise jwt_error

    def validate_access_token(self, token: str) -> bool:
        function_name = "Validate Access Token"
        logger.info(f"Enter - {function_name}")
        try:
            data: dict = self.decode_access_token(token)
            logger.info(f"Exit - {function_name}")
            return bool(data.get("email", ""))
        except (
            ValueError,
        ) as jwt_error:
            logger.error(
                f"Exit - {function_name} Exception Occurred {jwt_error}",
                )
            raise jwt_error
        except (
            ExpiredSignatureError,
            InvalidTokenError,
        ) as jwt_error:
            logger.error(f"Exit {function_name} Exception occurred: {str(jwt_error)}")
            raise jwt_error


access_token = AccessToken()
