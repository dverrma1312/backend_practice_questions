from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, model_validate, status, Depends
from sqlmodel import SQLModel,  create_engine, Session

sqllite_url = "sqlite:///tasks.db"
engine = create_engine(sqllite_url, echo= True)

def get_session():
    with Session(engine) as session:
        yield session
    

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=3)
    description : Optional[str] = None
    priority : int = Field(le=1 , ge= 5)
    completed : bool
    
class Usercheck(BaseModel):
    title: str = Field(min_length=3)
    description : Optional[str] = None
    priority : int = Field(le=1 , ge= 5)
    completed : bool
    
app = FastAPI(title = "practice")

@app.on_event("startup")
def create_tables():
    SQLModel.metadata.create_all(engine)


@app.post("/createtask", response_model= User, status_code= status.HTTP_200_OK)
def create(request: Usercheck, session: Session = Depends(get_session)):
    data = User(**request.model_dump())
    session.add(data)
    session.commit()
    session.refreh(data)
    
    return data

