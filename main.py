from typing import List
from fastapi import FastAPI,HTTPException
from uuid import UUID, uuid4
from models import Gender, Role, User, UserUpdateRequest


app = FastAPI()

db: List[User] = [
    User(
        id = UUID("5b74c13f-1916-4e7f-a83c-4cbb6c03be41"),
        first_name="Nunya",
        last_name="Klah",
        gender=Gender.male,
        roles=[Role.student]
    ),
    User(
        id = UUID("f500db72-d6d4-41c7-b619-709c2dbdc57c"),
        first_name="Kukua",
        last_name="Ansah",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    )
]
@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;    

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}    


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID): 
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code = 404,
        detail= f"User with id: {user_id} does not exist"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )                    