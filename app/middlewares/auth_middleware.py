from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.config import access_token
from app.schemas import CommonResponseSchema
from app.utils import logger


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
            ) -> Response:
        function_name = "Auth Middleware"
        xss_protection = request.headers.get("X-XSS-protection")
        content_security_policy = request.headers.get("Content-Security-Policy")
        frame_options = request.headers.get("X-Frame-Options")
        content_options = request.headers.get("X-Content-Type-Options")
        sts_policy = request.headers.get("Strict-Transport-Security")

        if (
                xss_protection is None
                or xss_protection == ""
                or content_security_policy is None
                or content_security_policy == ""
                or frame_options is None
                or frame_options == ""
                or content_options is None
                or content_options == ""
                or sts_policy is None
                or sts_policy == ""
        ):
            logger.error(
                    message=f"Exit {function_name} X-XSS-protection header not found",
                    function_name=function_name,
                    )
            return JSONResponse(
                    content=CommonResponseSchema(
                            message="X-XSS-protection header not found",
                            status="Not Ok",
                            ).dict(),
                    status_code=status.HTTP_400_BAD_REQUEST,
                    )
        try:
            access_token.decode_access_token(request.headers.get("access-token"))
            response = await call_next(request)
            logger.info(f"Exit - {function_name}", function_name=function_name)
        except (
                PyJWTError,
                InvalidTokenError,
                ExpiredSignatureError,
                ValueError,
                ) as jwt_validation_exception:
            response = JSONResponse(
                    content=CommonResponseSchema(
                            message="Token ID is not valid or Expired token",
                            status="Not Ok",
                            ).dict(),
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    )
            logger.error(
                    f"Exit - {function_name} Exception Occurred {jwt_validation_exception}",
                    function_name=function_name,
                    )
        return response
