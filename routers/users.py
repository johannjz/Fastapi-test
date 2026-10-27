from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter()

# Inicia el servidor con uvicorn users:app --reload

# Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
        User(id=1, name="oko", surname="pazon", url="https://eloko.com", age="47"),
        User(id=2, name="pinuino", surname="chitito", url="https://elchitito.com", age="24"),
        User(id=3, name="puhupaszo", surname="pahupon", url="https://elpuhupo.com", age="22")]

@router.get("/user")
async def usersjson():
    return [{
        "name":"oko",
        "surname":"pazon",
        "url":"https://eloko.com",
        "age":"47"
        },
            {
        "name":"pinuino",
        "surname":"chitito",
        "url":"https://elchitito.com",
        "age":"24"
        },
            {
        "name":"puhupazo",
        "surname":"puhupon",
        "url":"https://elpuhupo.com",
        "age":"22"
        }]

@router.get("/user")
async def users():
    return users_list

# Path

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query 

@router.get("/user/")
async def user(id: int):
    return search_user(id)

@router.post("/user/", response_model=User ,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")

    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error":"No se actualizó el usuario"}

    return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error":"No se ha eliminado el usuario"}   
    
def search_user(id: int):
    usersl = filter(lambda user: user.id == id, users_list)
    try:
        return list(usersl)[0]
    except:
        return {"error":" no hay usuario con ese id"}