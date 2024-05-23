from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models import User
from database import get_database

router = APIRouter()

@router.get("/get-users", response_model=List[User])
async def get_users(db = Depends(get_database)):
    users = []
    async for user in db["users"].find({}):
        users.append(User(**user))
    return users

@router.post("/create-user")
async def create_user(user: User, db = Depends(get_database)):
    result = await db["users"].insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@router.put("/update-user/{user_id}")
async def update_user(user_id: int, users: list[User], db = Depends(get_database)):
    result = await db["users"].update_one({"id": user_id}, {"$set": users[0].dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: int, db = Depends(get_database)):
    result = await db["users"].delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.put("/update-partial-user/{user_id}")
async def update_user(user_id: int, user_update: User, db = Depends(get_database)):
    # Obtener el usuario existente
    existing_user = await db["users"].find_one({"id": user_id})
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Crear un diccionario con solo los campos que se enviaron en la solicitud
    update_data = {}
    if user_update.name is not None:
        update_data["name"] = user_update.name
    if user_update.path is not None:
        update_data["path"] = user_update.path
    
    # Actualizar solo los campos que se enviaron
    result = await db["users"].update_one({"id": user_id}, {"$set": update_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User updated successfully"}