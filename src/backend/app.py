import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.backend.routers.ml_model import ml_router
from src.backend.routers.token import token_router
from src.backend.routers.user import user_router
from src.db import core
from src.db.database import engine
from starlette.responses import FileResponse

core.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ml_router, prefix="/predict")
app.include_router(user_router, prefix="/user")
app.include_router(token_router, prefix="/token")
app.mount("/", StaticFiles(directory="src/frontend/", html=True), name="static")


@app.get("/health")
def health_status():
    return {"Status": "Healthy"}


@app.get("/", response_class=HTMLResponse)
def read_root():
    path = os.path.join(sys.path[0], "src/frontend/index.html")
    return FileResponse(path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
