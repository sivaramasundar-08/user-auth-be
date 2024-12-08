from app.models.common_info_model import CommonInfoModel
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy import Column


class UserConfigModel(CommonInfoModel):
    id = Column(BIGINT(20), primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255), nullable=True)
    password = Column(VARCHAR(255), nullable=True)
    phone_number = Column(VARCHAR(255), nullable=True)

    class Config:
        orm_mode = True

