# OK, let's go a bit more advanced now.
# In this example, we will:
# 1. Carefully handle the http status_code.
# 2. Carefully handle exceptions.
# 3. Query Parameters & Data Validation with a Pydantic Model

# In the following, we will mimic a employee database API
from collections import namedtuple
from datetime import date, datetime, timezone
from typing import Annotated, NamedTuple, Optional, cast
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

# Initiate an random db
# Of course, a real db should not be store in an in-memory dictionary.
# This serves only as a simple example of a db
employee_db = {
    "ccbd5cb5-1850-4a48-97c2-dccc11b4b935": {
        "first_name": "John",
        "last_name": "Doe",
        "birthday": "1981-01-01",
        "email": "jdoe@example.com",
    },
    "5b1b2bd6-dffa-491d-aaa8-570d707f77ef": {
        "first_name": "Jane",
        "last_name": "Smith",
        "birthday": "1990-05-14",
        "email": "jsmith@example.com",
    },
    "b51b1ec4-c5f8-4e38-8ba2-b47d10709d80": {
        "first_name": "Alice",
        "last_name": "Brown",
        "birthday": "1985-07-23",
        "email": "abrown@example.com",
    },
    "4f221ea2-7f36-4d73-aeaa-24092ea3ceec": {
        "first_name": "Bob",
        "last_name": "Johnson",
        "birthday": "1992-02-10",
        "email": "bjohnson@example.com",
    },
    "21544171-dd54-48c9-92ee-c1ab6e8e33cf": {
        "first_name": "Emily",
        "last_name": "Davis",
        "birthday": "1995-09-30",
        "email": "edavis@example.com",
    },
}


# The Employee Model will do data validation and check that all is ok
class Employee(BaseModel):
    first_name: str
    last_name: str
    birthday: date = Field(description="Birthday in YYYY-MM-DD format")
    email: Optional[EmailStr] = None

    @field_validator("first_name", "last_name")
    @classmethod  # Not always necessary but preferred for clean code
    def validate_and_format_name(cls, v):
        v = v.strip()
        if not v.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return v.capitalize()

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v):
        # Ensure the person is between 18 and 64 years old
        today = datetime.today().date()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

        if age < 18 or age > 64:
            raise ValueError("Age must be between 18 and 64 years old.")
        return v

    @model_validator(mode="after")
    @classmethod
    def validate_email(cls, values):
        if email := values.email:
            email = email.lower()
            expected_email = (
                f"{values.first_name[0].lower()}{values.last_name.lower()}@example.com"
            )
            if email != expected_email:
                raise ValueError(f"Email must be null or equal to '{expected_email}'.")
        return values


class NameParams(BaseModel):
    first_name: str
    last_name: str

    # Validates and transforms the first and last name
    # Requires Pydantic v2.x
    @field_validator("first_name", "last_name")
    @classmethod
    def validate_and_format_name(cls, v):
        v = v.strip()
        if not v.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return v.capitalize()


class AgeParams(BaseModel):
    min_age: int = Field(ge=18)
    max_age: int = Field(le=64)

    # validates that the min and max are in order
    # requires Pydantic v2.x
    @model_validator(mode="before")
    @classmethod
    def check_max_age_greater_than_min_age(cls, values):
        min_age = values.get("min_age")
        max_age = values.get("max_age")

        if min_age is not None and max_age is not None and max_age <= min_age:
            raise ValueError("max_age must be greater than min_age")

        return values


class SearchParams(BaseModel):
    first_name: Optional[str] = Field(default=None, description="Employee First Name")
    last_name: Optional[str] = Field(default=None, description="Employee Last Name")
    min_age: Optional[int] = Field(default=None, ge=18)
    max_age: Optional[int] = Field(default=None, le=64)

    @model_validator(mode="before")
    @classmethod
    def do_basic_checks(cls, values):
        min_age = values.get("min_age")
        max_age = values.get("max_age")

        if (min_age is None) != (max_age is None):
            raise ValueError(
                "Both min_age and max_age must be provided together or omitted."
            )
        # No need to check min_age...
        if max_age is not None and max_age <= min_age:
            raise ValueError("max_age must be greater than min_age.")

        first_name = values.get("first_name")
        last_name = values.get("last_name")

        if (first_name is None) != (last_name is None):
            raise ValueError(
                "Both first_name and last_name must be provided together or omitted."
            )

        return values

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_and_format_name(cls, v):
        if v:
            v = v.strip()
            if not v.isalpha():
                raise ValueError("Name must contain only alphabetic characters.")
            return v.capitalize()
        return v


# ------------------------------------------------------------------------------------ #
#                                   Start of the API                                   #
# -------------------------------------------------------------------------------------#

app = FastAPI()


# Basic API health check
@app.get("/v0/healthcheck", status_code=200)
def healthcheck():
    return {
        "status": "ok",
        "service": "tutorial 1",
        "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
    }


# Update employee by uuid
@app.put("/v0/employees/{uuid}")
def update_employee(uuid: UUID, employee_update: Employee):
    if (str_uuid := str(uuid)) not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_db[str_uuid].update(employee_update.model_dump(exclude_unset=False))
    return {"status": "Employee updated", "employee": employee_db[str_uuid]}


# To partially update an employee we need to create model that allows for partial info
# EmployeePatch model inherits from Employee and does the necessary modifications to allow for partial updates
class EmployeePatch(Employee):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    email: Optional[EmailStr] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_and_format_name(cls, v):
        if v is None:
            return v
        return Employee.validate_and_format_name(v)

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v):
        if v is None:
            return v
        return Employee.validate_birthday(v)

    @model_validator(mode="after")
    @classmethod
    def validate_email(cls, values):
        if values.email and values.first_name and values.last_name:
            return Employee.validate_email(values)  # type: ignore
        elif (values.email is None) != (
            values.first_name is None and values.last_name is None
        ) or (
            len(values.model_fields_set) == 1 and "birthday" in values.model_fields_set
        ):
            return values
        else:
            raise ValueError("Invalid patch due to missing values.")


@app.patch("/v0/employees/{uuid}")
def partially_update_employee(uuid: UUID, employee_patch: EmployeePatch):
    if (str_uuid := str(uuid)) not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")

    # validate the email in the data
    if employee_db[str_uuid].get("email") is None:
        employee_db[str_uuid].update(employee_patch.model_dump(exclude_unset=True))
    if (
        "email" in employee_patch.model_fields_set
        and "first_name" not in employee_patch.model_fields_set
        and "last_name" not in employee_patch.model_fields_set
        and employee_patch.email
        != (
            expected_email := f"{employee_db[str_uuid]["first_name"][0].lower()+employee_db[str_uuid]["last_name"].lower()}@example.com"
        )
    ):
        raise HTTPException(
            status_code=404, detail=f"Email should be '{expected_email}'"
        )
    else:
        employee_db[str_uuid].update(employee_patch.model_dump(exclude_unset=True))

    # There are more cases to be consider... However this is not the purpose of this tutorial

    return {"status": "Employee updated", "employee": employee_db[str_uuid]}


# Creates a new employee
@app.post("/v0/employees", status_code=201)
def create_employee(employee: Employee):
    # Check if the employee already exists by using a set of unique identifiers
    for employee_id, existing_employee in employee_db.items():
        if (
            existing_employee["first_name"].lower()
            == employee.first_name.strip().lower()
            and existing_employee["last_name"].lower()
            == employee.last_name.strip().lower()
            and existing_employee["birthday"] == employee.birthday
        ):
            raise HTTPException(
                status_code=409, detail=f"Employee already exists at id {employee_id}"
            )

    # Create new employee with a unique ID
    employee_id = str(uuid4())
    employee_db[employee_id] = employee.model_dump()

    return {
        "status": "Employee added successfully",
        "employee_id": employee_id,
        "employee_data": employee_db[employee_id],
    }


# Deletes an employee
# 204 doesn't return a message
@app.delete("/v0/employees/{uuid}", status_code=204)
def delete_employee(uuid: UUID):
    if employee_db.pop(str(uuid), None) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return


# Searches for an employee by age range
@app.get("/v0/employees/search-by-age")
def get_employee_by_age(age_query: Annotated[AgeParams, Query()]):
    today = date.today()

    # Filter employees by age
    matching_employees = [
        {
            "id": emp_id,
            **employee,
            "age": today.year
            - datetime.strptime(employee["birthday"], "%Y-%m-%d").year,
        }
        for emp_id, employee in employee_db.items()
        if age_query.min_age
        <= today.year - datetime.strptime(employee["birthday"], "%Y-%m-%d").year
        <= age_query.max_age
    ]

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found in the specified age range"
        )

    return {"status": "success", "employees": matching_employees}


# Searches for an employee by age range
@app.get("/v0/employees/search-by-name")
def get_employee_by_name(name_query: Annotated[NameParams, Query()]):

    # Filter employees by name
    matching_employees = [
        {
            "id": emp_id,
            **employee,
        }
        for emp_id, employee in employee_db.items()
        if name_query.first_name == employee["first_name"]
        and name_query.last_name == employee["last_name"]
    ]

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found in the specified age range"
        )

    return {"status": "success", "employees": matching_employees}


# Mixed search with new query model SearchParams
@app.get("/v0/employees/search")
def get_employee_v0(search_query: SearchParams = Depends()):
    # search_query: Annotated[SearchParams, Query()] works the same
    today = date.today()

    # Filter employees by conditions
    matching_employees = []
    for emp_id, employee in employee_db.items():
        employee_age = (
            today.year - datetime.strptime(employee["birthday"], "%Y-%m-%d").year
        )
        age_match = search_query.min_age is None or (
            search_query.min_age <= employee_age <= cast("int", search_query.max_age)
        )
        name_match = search_query.first_name is None or (
            employee["first_name"] == search_query.first_name
            and employee["last_name"] == search_query.last_name
        )
        if age_match and name_match:
            matching_employees.append({"id": emp_id, **employee, "age": employee_age})

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found matching the criteria"
        )

    return {"status": "success", "employees": matching_employees}


# Another way to create queries from old queries
# However, here all parameters are required
@app.get("/v1/employees/search")
def get_employee_v1(
    age_query: AgeParams = Depends(),  # or Annotated[AgeParams, Depends()]
    name_query: NameParams = Depends(),  # also works the same as above
):
    today = date.today()

    # Filter employees by conditions
    matching_employees = []
    for emp_id, employee in employee_db.items():
        employee_age = (
            today.year - datetime.strptime(employee["birthday"], "%Y-%m-%d").year
        )
        age_match = age_query.min_age is None or (
            age_query.min_age <= employee_age <= age_query.max_age
        )  # type: ignore
        name_match = name_query.first_name is None or (
            employee["first_name"] == name_query.first_name
            and employee["last_name"] == name_query.last_name
        )
        if age_match and name_match:
            matching_employees.append({"id": emp_id, **employee, "age": employee_age})

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found matching the criteria"
        )

    return {"status": "success", "employees": matching_employees}


def bundle_name_and_age(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> Optional[NamedTuple]:
    data = {}
    # not gonna complicate it just to make a proof
    if first_name is None and last_name is None and min_age is None and max_age is None:
        return None
    if first_name is None or last_name is None:
        data["first_name"] = None
        data["last_name"] = None
    else:
        data.update(NameParams(first_name=first_name, last_name=last_name).model_dump())

    if min_age is None or max_age is None:
        data["min_age"] = None
        data["max_age"] = None
    else:
        data.update(AgeParams(min_age=min_age, max_age=max_age).model_dump())

    tmp = namedtuple("tmp", data)

    return tmp(**data)


# I am just using this class for linting
class MixedSearchParams(NamedTuple):
    first_name: str
    last_name: str
    min_age: int
    max_age: int


# A second way to create query params from old Params
# The Depends function can be used as a wrapper
@app.get("/v2/employees/search")
def get_employee_v2(
    search_query: Annotated[MixedSearchParams, Depends(bundle_name_and_age)],
):
    today = date.today()

    # Filter employees by conditions
    matching_employees = []
    for emp_id, employee in employee_db.items():
        employee_age = (
            today.year - datetime.strptime(employee["birthday"], "%Y-%m-%d").year
        )
        age_match = (
            search_query is None
            or search_query.min_age is None
            or (search_query.min_age <= employee_age <= search_query.max_age)
        )
        name_match = (
            search_query is None
            or search_query.first_name is None
            or (
                employee["first_name"] == search_query.first_name
                and employee["last_name"] == search_query.last_name
            )
        )
        if age_match and name_match:
            matching_employees.append({"id": emp_id, **employee, "age": employee_age})

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found matching the criteria"
        )

    return {"status": "success", "employees": matching_employees}


# A second way to create query params from old Params
# The Depends function can be used as a wrapper
@app.get("/v3/employees/search")
def get_employee_v3(
    age_query: Annotated[Optional[AgeParams], Depends()] = None,
    name_query: Annotated[Optional[NameParams], Depends()] = None,
):
    today = date.today()

    # Filter employees by conditions
    matching_employees = []
    for emp_id, employee in employee_db.items():
        employee_age = (
            today.year - datetime.strptime(employee["birthday"], "%Y-%m-%d").year
        )
        age_match = age_query.min_age is None or (
            age_query.min_age <= employee_age <= age_query.max_age
        )  # type: ignore
        name_match = name_query.first_name is None or (
            employee["first_name"] == name_query.first_name
            and employee["last_name"] == name_query.last_name
        )
        if age_match and name_match:
            matching_employees.append({"id": emp_id, **employee, "age": employee_age})

    if not matching_employees:
        raise HTTPException(
            status_code=404, detail="No employees found matching the criteria"
        )

    return {"status": "success", "employees": matching_employees}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("01_data_validation_and_exceptions:app", reload=True)
