import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi_sqlalchemy import DBSessionMiddleware, db

from .schema import Bug as SchemaBug
from .schema import User as SchemaUser
from . import schema
from .schema import Bug, BugUpdate, BugCreate
from .schema import User, UserUpdate, UserCreate
from app.db import models
from app.db.models import Bug as ModelBug
from app.db.models import User as ModelUser
from app.db.session import SessionLocal, engine
import os
from dotenv import load_dotenv


models.Base.metadata.create_all(bind=engine)

load_dotenv('.env')
Session = SessionLocal()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/bug/', response_model=SchemaBug)
async def create_bug(bug: BugCreate, db: Session = Depends(get_db)):
    new_bug = ModelBug(title=bug.title, description=bug.description)
    db.add(new_bug)
    db.commit()
    return new_bug

@app.get('/bug')
async def get_all_bug(db: Session = Depends(get_db)):
    bug = db.query(ModelBug).all() 
    return bug


@app.post('/user/', response_model=SchemaUser)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = ModelUser(name=user.name)
    db.add(db_user)
    db.commit()
    print(db_user.id)
    return db_user

@app.get('/user')
async def get_all_user(db: Session = Depends(get_db)):
    user = db.query(ModelUser).all() 
    return user

@app.get('/user/{id}', response_model= SchemaUser)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    new_user = db.query(ModelUser).filter(ModelUser.id == id).first()
    if not new_user:
        raise HTTPException(Status_code=status.HTTP_404_NOT_FOUND,
        detail="user with id: {id} does not exists")
    db.add(new_user)
    db.commit()
    return new_user

@app.get('/bug/{id}', response_model= SchemaBug)
async def get_bug_by_id(id: int, db: Session = Depends(get_db)):
    new_bug = db.query(ModelBug).filter(ModelBug.id == id).first()
    if not new_bug:
        raise HTTPException(Status_code=status.HTTP_404_NOT_FOUND,
        detail="bug with id: {id} does not exists")
    db.add(new_bug)
    db.commit()
    return new_bug


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(ModelUser).filter(ModelUser.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id: {id} does not exists")
    user.delete(synchronize_session=False)
    db.commit()
    return 
@app.delete('/bug/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_bug_buy_id(id: int, db: Session = Depends(get_db)):
    bug = db.query(ModelBug).filter(ModelBug.id == id)

    if not bug.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"bug with id: {id} does not exists")
    bug.delete(synchronize_session=False)
    db.commit()
    return 


@app.put('/user/{id}', response_model= SchemaUser)
async def update_user(id: int,updated_user: UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(ModelUser).filter(ModelUser.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(Status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id: {id} does not exists")
    # user_query.update(updated_user.dict(), synchronize_session=False)
    user.name = updated_user.name
    db.commit()
    db.refresh(user)
    return user

@app.put('/bug/{id}', response_model= SchemaBug)
async def update_bug(id: int,updated_bug: BugUpdate, db: Session = Depends(get_db)):
    bug_query = db.query(ModelBug).filter(ModelBug.id == id)
    bug = bug_query.first()
    if bug == None:
        raise HTTPException(Status_code=status.HTTP_404_NOT_FOUND,
        detail=f"bug with id: {id} does not exists")
    bug.title = updated_bug.title
    bug.description = updated_bug.description
    # bug_query.update(updated_bug.dict(), synchronize_session=False)
    db.commit()
    db.refresh(bug)
    return bug




if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)