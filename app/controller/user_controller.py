from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import (
    IntegrityError,
    NoSuchColumnError,
    NoSuchTableError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from app.connection import get_session
from app.exceptions import PasswordDidNotMatchException, InvalidPasswordException
from app.schemas import (
    AuthResponseSchema,
    CommonResponseSchema,
    LoginRequestSchema,
    UserRequestSchema,
    ErrorResponseSchema,
)
from app.service import UserService
from app.utils import logger

user_router = APIRouter(tags=["User"])


@user_router.post("/signup")
async def user_signup(body: UserRequestSchema, session: Session = Depends(get_session)):
    function_name: str = "Create User Controller"
    logger.info(f"Enter - {function_name}")
    try:
        response: AuthResponseSchema = UserService.user_signup(body, session)
        logger.info(f"Exit - {function_name}")
        return JSONResponse(content=response.dict(), status_code=HTTP_200_OK)
    except ValueError as value_error:
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Provide a valid values",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except (
        NoSuchTableError,
        ProgrammingError,
        NoSuchColumnError,
        OperationalError,
    ) as programming_error:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(programming_error)}",
        )
        return JSONResponse(
            content=CommonResponseSchema(
                message="Unknown error occurred",
                status="Not Ok",
            ).dict(),
            status_code=HTTP_409_CONFLICT,
        )
    except IntegrityError as not_unique_error:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(not_unique_error)}",
        )
        return JSONResponse(
            content=CommonResponseSchema(
                message="User already exists",
                status="Not Ok",
            ).dict(),
            status_code=HTTP_409_CONFLICT,
        )
    except InvalidPasswordException as untidy_password_error:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(untidy_password_error)}",
        )
        return JSONResponse(
            content=CommonResponseSchema(
                message="Please enter a valid password",
                status="Not Ok",
            ).dict(),
            status_code=HTTP_409_CONFLICT,
        )


@user_router.post("/login")
async def login_user(body: LoginRequestSchema, session: Session = Depends(get_session)):
    function_name: str = "Login User Controller"
    logger.info(f"Enter - {function_name}")
    try:
        response: AuthResponseSchema = UserService.login_user(
            request_body=body, session=session
        )
        logger.info(f"Exit - {function_name}")
        return JSONResponse(content=response.dict(), status_code=HTTP_200_OK)
    except (
        NoSuchTableError,
        ProgrammingError,
        NoSuchColumnError,
        OperationalError,
    ) as does_not_exist:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(does_not_exist)}",
        )
        return JSONResponse(
            content=CommonResponseSchema(
                message="Server Error Occurred",
                status="Not Ok",
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except ValueError as value_error:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(value_error)}",
        )
        return JSONResponse(
            content=ErrorResponseSchema(
                message="User not found",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=HTTP_404_NOT_FOUND,
        )
    except PasswordDidNotMatchException as password_did_not_match_exception:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(password_did_not_match_exception)}",
        )
        return JSONResponse(
            content=CommonResponseSchema(
                message="Email or Password did not match",
                status="Not Ok",
            ).dict(),
            status_code=HTTP_401_UNAUTHORIZED,
        )


@user_router.get("/validate")
async def validate_token(request: Request):
    function_name: str = "Validate Token Controller"
    logger.info(f"Enter - {function_name}")
    try:
        token = request.headers.get("access-token")
        response: bool = UserService.validate_token(token)
        logger.info(f"Exit - {function_name}")
        if response:
            return JSONResponse(
                content=CommonResponseSchema(
                    message="Token Valid",
                    status="Ok",
                ).dict(),
                status_code=HTTP_200_OK,
            )
        return JSONResponse(
            content=CommonResponseSchema(
                message="Token Invalid",
                status="Not Ok",
            ).dict(),
            status_code=HTTP_401_UNAUTHORIZED,
        )
    except ValueError as value_error:
        logger.error(
            f"Exit {function_name} Exception occurred: {str(value_error)}",
        )
        return JSONResponse(
            content=ErrorResponseSchema(
                message="Invalid token",
                status="Not Ok",
                error_detail=str(value_error),
            ).dict(),
            status_code=HTTP_401_UNAUTHORIZED,
        )

