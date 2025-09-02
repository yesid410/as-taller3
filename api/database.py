from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Configurar la URL de la base de datos desde variables de entorno
DATABASE_URL = "postgresql://postgres:postgres@db:5432/tienda_db"

# TODO: Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# TODO: Crear SessionLocal para las sesiones de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: Crear Base para los modelos
Base = declarative_base()

# TODO: Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
