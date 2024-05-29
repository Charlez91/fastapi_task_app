from typing import List, Optional
from pydantic import Field, UUID4, BaseModel

class CreateTaskDTO(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    #completed : bool

class UpdateTaskDTO(BaseModel):
    title : Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    completed : Optional[bool] = None

class ITaskData(BaseModel):
    id : UUID4
    title : str
    description : str
    completed : bool

class ITaskRO(BaseModel):
    task : ITaskData

class ITasksRO(BaseModel):
    tasks : List[ITaskData]