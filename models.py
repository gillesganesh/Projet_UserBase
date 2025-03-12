from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion PostgreSQL (à modifier si nécessaire)
DATABASE_URL = "postgresql://admin:admin@postgres:5432/users_db"

# Créer l'engine PostgreSQL
engine = create_engine(DATABASE_URL)

# Définir la base
Base = declarative_base()

# Modèle de table Utilisateur
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Gérer les sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour créer la base (à exécuter séparément)
def init_db():
    Base.metadata.create_all(bind=engine)
