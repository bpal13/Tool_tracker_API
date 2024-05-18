from fastapi import FastAPI
from . import models
from .database import engine
from .routers import admin, auth, tools

# create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(tools.router)


@app.get('/')
def root():
    return {'message': 'tool tracker homepage'}