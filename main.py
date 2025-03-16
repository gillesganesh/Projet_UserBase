from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import User, SessionLocal

app = FastAPI()

# Dépendance pour la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèle Pydantic pour la requête
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Utilisateurs"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
	return users 
    except Exception as e:
        # Retourner une erreur HTTP 500 avec un message personnalisé
        raise HTTPException(status_code=500, detail=f""La base de données est vide. Veuillez ajouter des utilisateurs. documentation_url : /docs: {str(e)}")
      

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
