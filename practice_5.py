from fastapi import FastAPI, model_validate, status, Depends, Query, HTTPException
from sqlmodel import SQLModel,  create_engine, Session, Relationship
from pydantic import Field, relationship

app = FastAPI()

sqllite = "hdhdhddh"
engine = create_engine(sqllite = sqllite, echo= True)

def get_session():
    with Session(engine ) as session: 
        yield session

@app.on_event("startup")
def create():
    SQLModel.metadata.create_all(engine )

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    user_id: int | None = Field(default=None, foreign_key="user.id")

    user: User | None = Relationship(back_populates="tasks")