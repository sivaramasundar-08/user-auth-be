import pydantic


class LoginRequestSchema(pydantic.BaseModel):
    email: str
    password: str
