from config.database import  engine

from models.task_model import Task
from models.user_model import User

def create_tables():
    """Create All database tables defined in application"""
    Task.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)