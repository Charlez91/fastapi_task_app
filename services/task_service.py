from sqlalchemy.orm import Session

class TaskService:

    def __init__(self, session:Session) -> None:
        self.session = session