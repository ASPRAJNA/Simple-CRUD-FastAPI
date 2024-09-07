import datetime 
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

router=APIRouter(prefix='/tasks',tags = ['CRUD Operation'])

class Tasks(BaseModel):
    title: str
    description:str | None
    date:datetime.datetime =datetime.datetime.now()

class Update_Tasks(BaseModel):
    title: Optional[str] | None
    description: Optional[str] |None 
    date:datetime.datetime =datetime.datetime.now()


tasks=[
    {"id":1,
    "title":"task 1",
    "description":"hi there you have to learn fastapi",
    "date":datetime.datetime(2020, 5, 17)
    },
     {"id":2,
    "title":"task 2",
    "description":"make a project using fastapi",
    "date":datetime.datetime(2020, 8, 17)
    },
      {"id":3,
    "title":"task 3",
    "description":"make crud operation using fastapi",
    "date":datetime.datetime(2020, 8, 17)
    },
]

@router.get("/alltasks")
def get_task(limit:int |None=10) ->list :
    return tasks[:limit]

  
@router.get("/getbyid/{id}")
def get_task_by_id(id:int)->dict:
    for x in tasks:
        if x['id']==id:
            return x
    return {"Message":f"No task with the id :{id} found"}


@router.post("/create")
def create_task(task:Tasks) -> list:
    task_new = jsonable_encoder(task)
    l=[]
    for i in range(len(tasks)):
        l.append(tasks[i]["id"])
    newid={}
    newid["id"]=max(l)+1
    res_task= {**newid, **task_new}
    tasks.append(res_task)
    return tasks

@router.put("/update/{id}")
def update_task(id:int,task:Update_Tasks)-> dict:
    for x in tasks:
        if x['id']==id:
            if isinstance(task.title,str):
                x['title']=task.title
            if isinstance(task.description,str):
                x['description']=task.description
            x['date']=task.date
            return x
    return {"Message":f"Task with id : {id} not found"}

@router.delete("/delete/{id}")
def delete_task(id:int):
    for x in tasks:
        if x["id"]==id:
            tasks.pop(tasks.index(x))
            return {"Message":f"Task of id {id} deleted successfully"}
    return {"Message":f"Task of id :{id} not found"}