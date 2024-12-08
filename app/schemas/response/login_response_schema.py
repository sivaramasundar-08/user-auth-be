from typing import Optional

import pydantic

from app.schemas.response.user_data_schema import UserDataSchema


class AuthResponseSchema(pydantic.BaseModel):
    status: str = "Ok"
    message: str = "User Logged in Successfully"
    access_token: Optional[str]
    data: UserDataSchema
