import json
from datetime import datetime

from fastapi import FastAPI

with open("./db.json", "r") as f:
    employee_db: dict = json.load(f)

app = FastAPI()


@app.get("/heartbeat")
async def heartbeat():
    return {
        "status": "ok",
        "service": "tutorial 1",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


@app.post("/square")
async def square(number: int):
    return {"square": number**2}


@app.get("/get_employee_db")
async def get_employee_db():
    return employee_db


# the following code is not optimized
# it should have a BaseModel for validation
# and should return specific status codes
# however, this is just a basic demo of the put and delete methods.
@app.put("/add_employee")
async def add_employee(employee):
    id_num = list(employee_db.keys())[-1].split("_")[-1]
    id_num = int(id_num) + 1
    employee_db.update({f"id_{id_num}": employee})
    # json should be saved for persistency
    return {"status": f"employee {id_num=} added"}


@app.delete("/delete_employee")
async def delete_employee(id):
    if employee_db.get(id) is None:
        return {"status": "employee not found"}
    employee_db.pop(id)
    return {"status": "employee deleted"}
