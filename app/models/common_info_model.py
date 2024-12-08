from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, VARCHAR


class CommonInfoModel:
    __abstract__ = True

    is_active = Column(TINYINT(1), nullable=True)
    created_at = Column(BIGINT(20), nullable=True)
    updated_at = Column(BIGINT(20), nullable=True)
    user_email = Column(VARCHAR(255), nullable=True)
