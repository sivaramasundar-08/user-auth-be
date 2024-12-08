import pydantic


class UserStatusRequestSchema(pydantic.BaseModel):
    status: int
    email: str
