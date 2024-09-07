from fastapi import APIRouter


home_router=APIRouter(prefix='/home',tags = ['Home Page'])

#home page
@home_router.get('/')
def home()->dict:
    return {"Message":"Welcome to FastAPI demo!!"}