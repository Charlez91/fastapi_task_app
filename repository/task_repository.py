from sqlalchemy.orm import Session

class TaskRepository:

    def __init__(self, session:Session) -> None:
        self.session = session