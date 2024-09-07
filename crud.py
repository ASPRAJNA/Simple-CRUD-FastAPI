import csv
import datetime 
import pandas as pd 
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

router=APIRouter(prefix='/tasks',tags = ['CRUD Operation'])

class Tasks(BaseModel):
    title: str
    description:str | None

class Update_Tasks(BaseModel):
    title: Optional[str] | None
    description: Optional[str] |None 


def list_task():
    myList=[]
    myFile = open('list_task.csv', 'r')
    reader = csv.DictReader(myFile)
    for dictionary in reader:
        myList.append(dictionary)
    myFile.close()
    return myList


@router.get("/alltasks")
def get_task(limit:int |None=10) ->list :
    return list_task()[:limit]


@router.get("/getbyid/{id}")
def get_task_by_id(id:int)->dict:
    myList=list_task()
    for x in myList:
        if x['id']==str(id):
            return x
    return {"Message":f"No task with the id :{id} found"}


@router.post("/create")
def create_task(task:Tasks):
    task_new = jsonable_encoder(task)
    l=[]
    tasks=list_task()
    for i in range(len(tasks)):
        l.append(int(tasks[i]['id']))
    newid={}
    if len(l)==0:
        newid["id"]=1
    else:
        newid["id"]=max(l)+1
    res_task= {**newid, **task_new}
    res_task['date']=datetime.datetime.now()
    tasks.append(res_task)
    df = pd.DataFrame.from_records(tasks) 
    df.to_csv('list_task.csv', index=False)
    return res_task



@router.put("/update/{id}")
def update_task(id:int,task:Update_Tasks)-> dict | list:
    tasks=list_task()
    for x in tasks:
        if x['id']==str(id):
            if isinstance(task.title,str):
                x['title']=task.title
            if isinstance(task.description,str):
                x['description']=task.description
            x['date']=datetime.datetime.now()
            df = pd.DataFrame.from_records(tasks) 
            df.to_csv('list_task.csv', index=False)
            return x
    return {"Message":f"Task with id : {id} not found"}



@router.delete("/delete/{id}")
def delete_task(id:int):
    tasks=list_task()
    for x in tasks:
        if x["id"]==str(id):
            tasks.pop(tasks.index(x))
            df = pd.DataFrame.from_records(tasks) 
            df.to_csv('list_task.csv', index=False)
            return {"Message":f"Task of id {id} deleted successfully"}
    return {"Message":f"Task of id :{id} not found"}

