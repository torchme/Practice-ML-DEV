import uvicorn
from fastapi import FastAPI
from src.backend.routers.ml_model import ml_router
from src.backend.routers.user import user_router
from src.backend.routers.token import token_router
from src.db import core
from src.db.database import engine

core.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ml_router, prefix="/predict")
app.include_router(user_router, prefix="/user")
app.include_router(token_router, prefix="/token")


@app.get("/health")
def read_root():
    return {"Status": "Healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
