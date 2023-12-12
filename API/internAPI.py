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
        "userID": result[0][0] if success else "",
        "error": error
    }
    return formattedResult

@internal_router.get('/{userid}/receipts')
def get_receipts(userid: int):
    db = DBConnector()
    query = 'SELECT * FROM public.receipt_with_total WHERE "userwhomadeitid" = %s'
    params = (userid,)
    result = db.fetch(query, params)
    db.disconnect()
    receipts = []
    for row in result:
        receipts.append(schema.ReceiptTable.model_validate({
            "id": row[0],
            "userid": row[1],
            "groupid": row[2],
            "date": row[3],
            "currency": row[4],
            "total": row[5]
        })
        )
    return receipts

@internal_router.get('/{userid}/receipts/{receipt_id}')
def get_receipt(userid: int, receipt_id: int):
    # ensure receipt belongs to user
    db = DBConnector()
    query = 'SELECT * FROM public.receipttable WHERE "id" = %s'
    params = (receipt_id,)
    result = db.fetch(query, params)
    if result == []:
        return {"success": False, "error": "Receipt not found"}
    if result[0][1] != userid:
        return {"success": False, "error": "Receipt does not belong to user"}
    
    # get receipt items
    query = 'SELECT * FROM public.itemtable WHERE "scanningid" = %s'
    params = (receipt_id,)
    result = db.fetch(query, params)
    db.disconnect()
    items = []
    for row in result:
        items.append(schema.ItemTable.model_validate({
            "id": row[0],
            "scanningId": row[1],
            "itemName": row[2],
            "price": row[3],
            "userId": row[4]
        })
        )
    return items

@internal_router.get('/{userid}/groupMembers')
def get_group_members(userid: int):
    db = DBConnector()
    query = 'SELECT * from usertable WHERE "id" IN (SELECT "userid" FROM useringrouptable WHERE "groupid" IN (SELECT "id" FROM public.grouptable WHERE "owneruserid" = %s))'
    params = (userid,)
    result = db.fetch(query, params)
    db.disconnect()
    members = []
    for row in result:
        members.append(schema.UserTable.model_validate({
            "id": row[0],
            "userEmail": row[1],
            "userName": row[2]
        })
        )
    return members

@internal_router.get('/{userid}/groupMembers/{groupid}')
def get_group_members(userid: int, groupid: int):
    db = DBConnector()
    query = 'SELECT * from usertable WHERE "id" IN (SELECT "userid" FROM useringrouptable WHERE "groupid" = %s)'
    params = (groupid,)
    result = db.fetch(query, params)
    db.disconnect()
    members = []
    for row in result:
        members.append(schema.UserTable.model_validate({
            "id": row[0],
            "userEmail": row[1],
            "userName": row[2]
        })
        )
    return members



@internal_router.get('/{userid}/groups')
def get_groups(userid: int):
    db = DBConnector()
    query = 'SELECT * FROM public.grouptable WHERE "owneruserid" = %s'
    params = (userid,)
    result = db.fetch(query, params)
    db.disconnect()
    groups = []
    for row in result:
        groups.append(schema.GroupTable.model_validate({
            "id": row[0],
            "groupName": row[1],
            "ownerUserId": row[2]
        })
        )
    return groups

@internal_router.post('/{userid}/receipts/{receipt_id}/user/{user_id}')
def add_user_to_receipt(userid: int, receipt_id: int, user_id: int):
    pass

@internal_router.post('/{userid}/receipts/{receipt_id}/group/{group_id}')
def add_group_to_receipt(userid: int, receipt_id: int, group_id: int):
    pass

@internal_router.post("/internal/{userid}/groups/{groupName}")
async def create_group(userid: str, groupName: str):
    pass

@internal_router.delete("/internal/{userid}/groups/{group_id}")
async def delete_group(userid: str, group_id: str):
    pass

@internal_router.post("/internal/{userid}/groups/{group_id}/user/{user}")
async def add_user_to_group(userid: str, group_id: str, user: str):
    pass

@internal_router.delete("/internal/{userid}/groups/{group_id}/user/{user}")
async def remove_user_from_group(userid: str, group_id: str, user: str):
    pass