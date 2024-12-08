import pydantic


class UserRequestSchema(pydantic.BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
