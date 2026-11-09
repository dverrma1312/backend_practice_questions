from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, model_validate, status, Depends, Query
from sqlmodel import SQLModel,  create_engine, Session

sqllite_url = "somehting"
engine = create_engine(sqllite_url, echo= True)


class Task(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=3)
    description : Optional[str] = None
    priority : int = Field(le=1 , ge= 5)
    completed : bool
    

def get_session():
    with Session(engine) as session:
        yield session
        
app = FastAPI(title = "practice2")
        
@app.patch("/udpate/tasks/{task_id}", status_code= status.HTTP_401_UNAUTHORIZED)
def updatethetask(request: Task, task_id : int = Query(le = 3), session: Session = Depends(get_session)):
    data1 = session.get(Task, task_id)
    if not data1:
        return status.HTTP_204_NO_CONTENT
    data1.sqlmodel_update(request.model_dump(exclude_unset=True))
    session.add(data1)
    session.commit()
    session.refresh(data1)
    return data1
    