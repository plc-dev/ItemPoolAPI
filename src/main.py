from fastapi import FastAPI
from .routers import TaskRegistration, TaskRetrieval

app = FastAPI()

app.include_router(TaskRegistration.router)
app.include_router(TaskRetrieval.router)