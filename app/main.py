from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.db.database import Base, engine 

<<<<<<< HEAD
#uvicorn app.main:app --reload

=======
>>>>>>> 76d042f830440c089a3dcf227d1245534ad2ff22
app = FastAPI(
    title="API de portes de arma em FastAPI",
    description="Autenticação JWT/Bcrypt."
)

# Inclui as rotas
app.include_router(auth.auth_router, prefix="/v1")
<<<<<<< HEAD
=======

@app.get("/health")
def health_check():
    return {"status": "ok"}
>>>>>>> 76d042f830440c089a3dcf227d1245534ad2ff22
