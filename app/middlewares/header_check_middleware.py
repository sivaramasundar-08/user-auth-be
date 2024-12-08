from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.schemas import CommonResponseSchema
from app.utils import logger


class HeaderMiddleware(BaseHTTPMiddleware):
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
                    message=f"Exit {function_name} Security headers missing not found",
                    function_name=function_name,
                    )
            return JSONResponse(
                    content=CommonResponseSchema(
                            message="X-XSS-protection header not found",
                            status="Not Ok",
                            ).dict(),
                    status_code=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            response = await call_next(request)
            logger.info(f"Exit - {function_name}", function_name=function_name)
            return response
