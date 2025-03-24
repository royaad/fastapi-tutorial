from datetime import datetime, timezone

from fastapi import FastAPI, Query


# create a FastAPI app
app = FastAPI()

# A basic get request to do a health-check
# time is not iso 8601
@app.get("/v0/healthcheck")
async def healthcheck():
    return {
        "status": "ok",
        "service": "tutorial 1",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

# Notice that this function is not asynchronous
# FastAPI can handle both... The choice between them will be explained later.
# FastAPI can parse path parameters.
@app.get("/v0/employee/{employee_id}")
def get_employee(employee_id: str):
    return {"status": f"{employee_id} requested"}


# Below is a dummy post request
@app.post("/v0/employee/{employee_id}")
async def create_employee(employee_id: str):
    return {"status": f"employee {employee_id=} created"}

# And a dummy delete request
@app.delete("/v0/employee/{employee_id}")
async def delete_employee(employee_id: str):
    return {"status": f"employee {employee_id} deleted"}

# FastAPI parses multiple path and query parameters.
# The queries below are optional
@app.get("/v0/employee/{employee_id}/info/{info_str}")
def get_employee_info(
    employee_id: int,
    info_str: str,
    q: str | None = None,
    ):
    if q:
        return {"status": f"{info_str} of employee with {employee_id=} queried with parameters {q}"}
    return {"status": f"{info_str} of employee with {employee_id=} queried without parameters"}

# The query below is required
@app.get("/v0/items/{items_id}")
def get_item_availability(items_id: int, available: bool):
    return {"status": f"{items_id=} is {available=}"}

# another way to treat query parameters
@app.get("/v0/employees")
def get_employee_info_adv(
    age: int = Query(None, title="Age", description="Age to filter for"),
    in_office: bool = Query(False, description="If person is in office or on vacation.")
    ):
    if age:
        if in_office:
            return {"status": f"get for employees with {age=} and in office"}
        return {"status": f"get for employees with {age=}"}
    
    if in_office:
        return {"status": f"get any employees in office"}
    return {"status": f"get any employees"}
