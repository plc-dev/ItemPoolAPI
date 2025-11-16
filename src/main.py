from fastapi import FastAPI
from .routers import TaskRegistration, TaskRetrieval, TaskCollection

app = FastAPI()

app.include_router(TaskRegistration.router)
app.include_router(TaskRetrieval.router)
app.include_router(TaskCollection.router)
