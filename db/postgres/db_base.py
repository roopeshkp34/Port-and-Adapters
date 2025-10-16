# Import all the models.
# So that Base has them before being imported by Alembic.
from .base_class import Base # noqa: F401
import models  # noqa: F401
