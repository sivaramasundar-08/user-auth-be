import pydantic


class UserDataSchema(pydantic.BaseModel):
    email: str
    username: str
