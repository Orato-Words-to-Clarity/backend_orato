from app.core.database import Base, engine
from app.db.models.user import User

# Create all tables in the database

Base.metadata.create_all(bind=engine)

