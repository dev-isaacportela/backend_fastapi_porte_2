from fastapi import FastAPI
from app.api.v1.endpoints import auth, users
from app.db.database import Base, engine 


app = FastAPI(
    title="API de portes de arma em FastAPI",
    description="Autenticação JWT/Bcrypt."
)

# Inclui as rotas
app.include_router(auth.router, prefix="/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])

@app.get("/health")
def health_check():
    return {"status": "ok"}