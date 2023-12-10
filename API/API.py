import fastapi
import uvicorn
from fastapi import FastAPI, Form, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from API.externAPI import external_router
from API.internAPI import internal_router

app = FastAPI()
app.include_router(external_router, prefix='/external')
app.include_router(internal_router, prefix='/internal')

origins = [
    "http://localhost",
    "localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return {'message': 'Hello world'}
