from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importar routers
from routes.users import router as users_router
from routes.products import router as products_router
from routes.carts import router as carts_router

from database import get_db

# Crear la aplicación FastAPI
app = FastAPI(
    title="Tienda Virtual API",
    version="1.0.0",
    description="API para gestionar usuarios, productos y carritos de la Tienda Virtual."
)

# Middleware CORS (para permitir frontend externo)
origins = ["*", "http://localhost", "http://webapp", "http://proxy"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En producción es mejor poner ["http://localhost:3000", "https://tudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

# Registrar routers
app.include_router(users.router, prefix=f"{API_PREFIX}/users", tags=["users"])
app.include_router(products.router, prefix=f"{API_PREFIX}/products", tags=["products"])
app.include_router(carts.router, prefix=f"{API_PREFIX}/carts", tags=["carts"])

# Endpoint raíz
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a la Tienda Virtual API 🚀"}


# Health check (para verificar la BD)
@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "database": "disconnected",
                "error": str(e)
            }
        )