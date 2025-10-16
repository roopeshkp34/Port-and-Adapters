from uuid import uuid4

import sqlalchemy as sa

from ..base_class import Base


class Book(Base):
    id = sa.Column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    title = sa.Column(sa.String, nullable=False, index=True)
    author = sa.Column(sa.String, nullable=False, index=True)
    year = sa.Column(sa.Integer, nullable=False, index=True)
    created_on = sa.Column(sa.DateTime, default=sa.func.now(), nullable=False)
