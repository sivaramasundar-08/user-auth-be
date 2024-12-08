from typing import Any, Optional

import pydantic


class CommonResponseSchema(pydantic.BaseModel):
    message: str
    status: str


class DataResponseSchema(CommonResponseSchema):
    data: Optional[Any]


class ErrorResponseSchema(CommonResponseSchema):
    error_detail: str
