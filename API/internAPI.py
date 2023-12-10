from fastapi import APIRouter
from API.DBConnector import DBConnector
import API.schema as schema

internal_router = APIRouter()

@internal_router.get('/')
def index():
    return {'message': 'Hello internal world'}


@internal_router.get('/login')
def login(username: str):
    db = DBConnector()
    query = "SELECT * FROM usertable WHERE username = %s"
    params = (username,)
    result = db.fetch(query, params)
    db.disconnect()
    success = result != []
    error = "User not found" if not success else ""
    formattedResult = {
        "success": success,
        "error": error
    }
    return formattedResult

@internal_router.get('/{username}/receipts')
def get_receipts(username: str):
    db = DBConnector()
    query = "SELECT * FROM receipttable WHERE username = %s"
    params = (username,)
    result = db.fetch(query, params)
    db.disconnect()
    receipts = []
    for row in result:
        receipts.append(schema.ReceiptTable(
            id=row[0],
            username=row[1],
            date=row[2],
            currency=row[3],
            total=row[4]
        ))
    return receipts

@internal_router.get('/{username}/receipts/{receipt_id}')
def get_receipt(username: str, receipt_id: int):
    pass

