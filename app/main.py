from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.db.database import Base, engine 

#uvicorn app.main:app --reload

app = FastAPI(
    title="API de portes de arma em FastAPI",
    description="Autenticação JWT/Bcrypt."
)

# Inclui as rotas
app.include_router(auth.auth_router, prefix="/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}