from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.db.database import Base, engine 


app = FastAPI(
    title="API de portes de arma em FastAPI",
    description="Autenticação JWT/Bcrypt."
)

# Inclui as rotas
app.include_router(auth.router, prefix="/v1", tags=["Authentication"])

@app.get("/health")
def health_check():
    return {"status": "ok"}