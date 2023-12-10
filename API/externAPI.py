from fastapi import APIRouter

external_router = APIRouter()

@external_router.get('/')
def index():
    return {'message': 'Hello external world'}

@external_router.post('/{username}/new_receipt')
def new_receipt(username: str, ):
    pass