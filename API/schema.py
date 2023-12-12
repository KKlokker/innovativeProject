from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserTable(BaseModel):
    id: Optional[int] = None
    userEmail: str
    userName: str

class GroupTable(BaseModel):
    id: Optional[int] = None
    groupName: str
    ownerUserId: int

class UserInGroupTable(BaseModel):
    userId: int
    groupId: int

class ScanningTable(BaseModel):
    id: Optional[int] = None
    userWhoMadeItId: int
    attachedGroupId: int
    dateOfCreation: str
    currencyType: str

class ItemTable(BaseModel):
    id: Optional[int] = None
    scanningId: int
    itemName: str
    price: float
    userId: int

class ReceiptTable(BaseModel):
    id: int
    userid: int
    groupid: int
    date: datetime
    currency: str
    total: float