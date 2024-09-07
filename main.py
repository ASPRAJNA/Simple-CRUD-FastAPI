import crud
import home
from fastapi import FastAPI

app=FastAPI()

app.include_router(home.home_router)
app.include_router(crud.router)

@app.get("/",tags=["FastAPI"])
def index():
    return{"Message":"FASTAPI"}