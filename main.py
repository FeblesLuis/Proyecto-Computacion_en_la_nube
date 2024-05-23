from fastapi import FastAPI
from controller import router as user_router

app = FastAPI()

app.include_router(user_router)
