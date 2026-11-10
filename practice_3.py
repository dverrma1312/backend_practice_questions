from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, model_validate, status, Depends, Query, HTTPException
from sqlmodel import SQLModel,  create_engine, Session

sqllite_url = "something"
engine = create_engine(sqllite_url, echo= True)

def get_session(): 
    with Session(engine) as session:
        yield session


class Task(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=3)
    description : Optional[str] = None
    priority : int = Field(le=1 , ge= 5)
    completed : bool
    

class Response(SQLModel):
    title: str = Field(min_length=3)
    description : Optional[str] = None
    priority : int = Field(le=1 , ge= 5)
    completed : bool

app = FastAPI(title = "practice3")

@app.delete("/delete/{task_id}", status_code= status.HTTP_204_NO_CONTENT)
def deletethepoint(task_id : str = Query(default= None), session: Session = Depends(get_session)):
    data = session.get(Task ,task_id)
    if not data:
        return HTTPException(
            status_code= status.HTTP_100_CONTINUE,
            detail= " not dound"
        )
    session.delete(data)
    session.commit()
    
    return None


@app.put("/put/{task_id}", status_code= status.HTTP_100_CONTINUE)
def updatethepoint(request : Response, task_id : str = Query(default= None), session: Session = Depends(get_session)):
    data = session.get(Task , task_id)
    if not data:
        return HTTPException(
            status_code= status.HTTP_100_CONTINUE,
            detail= " not dound"
        )
    data.sqlmodel_update(request.model_dump())
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return request



    
    