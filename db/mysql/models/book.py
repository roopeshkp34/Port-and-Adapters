from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import CHAR

from ..base_class import Base


class Book(Base):
    # MySQL doesn't have native UUID type, use CHAR(36)
    id = sa.Column(
        CHAR(36), primary_key=True, default=lambda: str(uuid4()), nullable=False
    )
    title = sa.Column(sa.String(255), nullable=False, index=True)
    author = sa.Column(sa.String(255), nullable=False, index=True)
    year = sa.Column(sa.Integer, nullable=False, index=True)
    created_on = sa.Column(sa.DateTime, default=sa.func.now(), nullable=False)

