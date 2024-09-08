from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

# initiate an empty_db
employee_db = {}


class Employee(BaseModel):
    first_name: str
    last_name: str
    birthday: date
    email: Optional[EmailStr] = None


app = FastAPI()


@app.get("/heartbeat")
async def heartbeat():
    return {
        "status": "ok",
        "service": "tutorial 1",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


@app.get("/get_employee_db")
async def get_employee_db():
    return employee_db


@app.put("/add_employee", status_code=201)
async def add_employee(employee: Employee):
    # check if the employee already exists
    for k, v in employee_db.items():
        print(k, v)
        if (
            v["first_name"] == employee.first_name
            and v["last_name"] == employee.last_name
            and v["birthday"] == employee.birthday
        ):
            raise HTTPException(
                status_code=403, detail=f"employee already exists at id {k}"
            )
    str(uuid4())
    employee_db.update({str(uuid4()): employee.model_dump()})
    return {"status": "employee added"}


# 204 doesn't return a message
@app.delete("/delete_employee", status_code=204)
async def delete_employee(id: UUID):
    str_id = str(id)
    if employee_db.get(str_id) is None:
        raise HTTPException(status_code=404, detail="employee not found")
    tmp = employee_db.pop(str_id)
    return {f"status: employee {tmp} deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("2_data_validation_and_exceptions:app", reload=True)
