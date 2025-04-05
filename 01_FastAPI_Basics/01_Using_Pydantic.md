# FastAPI: Data Validation and Exception Handling

## Overview

The `01_data_validation_and_exceptions.py` file builds upon the basic FastAPI setup by introducing request body validation, use of Pydantic models, and exception handling with HTTP status codes. It demonstrates how FastAPI ensures data integrity and provides informative responses in both successful and erroneous scenarios.

## Running the Application

Unlike the previous [[00_Writing_Your_First_Fast_API_APP.md|example]] where we used `uvicorn` from the command line, this version runs the server by executing the Python script directly. This demonstrates another valid approach to starting a FastAPI application.

```bash
python 01_data_validation_and_exceptions.py
```

The file includes a `__main__` block that calls `uvicorn.run` internally:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01_data_validation_and_exceptions:app", reload=True)
```

This starts the development server with automatic reloading enabled, just like using the `--reload` flag in the CLI.

> [!NOTE]
> This is a different method than the one shown in `00_basic_crud.py`, and it illustrates the flexibility of running FastAPI apps—either via CLI or by embedding `uvicorn.run()` in code.

The server will be available at:

```plaintext
http://localhost:8000
```

## Employee Endpoints and Data Validation

In this section, we will explore how FastAPI leverages Pydantic for validating and parsing request bodies, path parameters, and query parameters. Pydantic models are essential for ensuring that incoming data adheres to predefined structures and constraints. We will also demonstrate how to implement validation logic, such as age validation, directly within Pydantic models.

The application uses an in-memory dictionary `employee_db` to store employee records for the purpose of this demonstration. In a production environment, you would typically replace this with a persistent database, such as SQLite, PostgreSQL, or another database system, to store employee data more reliably.

### Create a New Employee

```http
POST /v0/employees
```

This endpoint utilizes **Pydantic** to validate the request body and enforces business logic through custom validation on fields like `birthday` and `email`. The request body is validated against the `Employee` model, which ensures that all required fields are present and conform to the expected formats.

#### Employee Model Definition

```python
class Employee(BaseModel):
    first_name: str
    last_name: str
    birthday: date = Field(description="Birthday in YYYY-MM-DD format")
    email: Optional[EmailStr] = None
```

The `Employee` model contains four fields:

-   **First Name** (`first_name`): A required string field representing the employee's first name.
-   **Last Name** (`last_name`): A required string field representing the employee's last name.
-   **Birthday** (`birthday`): A required `date` field, which is validated to ensure the employee is between 18 and 64 years old.
-   **Email** (`email`): An optional email address field, validated to ensure it either remains `null` or matches a specific value, `"jtall@example.com"`, for demonstration purposes.

The model also includes custom validation logic:

-   **Age Validation**: Ensures the employee’s age, derived from their `birthday`, is within a valid range (18–64 years).
-   **Email Validation**: Restricts the `email` field to either `null` or the value `"jtall@example.com"`.

#### Example Request (Valid)

```bash
curl -X 'POST' \
  'http://localhost:8000/v0/employees' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "jane",
  "last_name": "tall",
  "birthday": "2005-04-05",
  "email": "jtall@example.com"
}'
```

In this request, the `email` value `"jtall@example.com"` meets the validation criteria, and the `birthday` value results in a valid age (within the 18–64 range). Therefore, the employee will be successfully created.

#### Example Response (201 Created)

```json
{
    "status": "Employee added successfully",
    "employee_id": "34b90155-b16f-49a2-bc2b-821c4f36d7b1",
    "employee_data": {
        "first_name": "Jane",
        "last_name": "Tall",
        "birthday": "2005-04-05",
        "email": "jtall@example.com"
    }
}
```

This response confirms that the employee was successfully created with a `201 Created` status code. The response includes a newly generated `employee_id` and returns the stored employee data, demonstrating the successful processing of the request.

#### Example Request (Invalid: Age Validation)

```bash
curl -X 'POST' \
  'http://localhost:8000/v0/employees' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "jane",
  "last_name": "tall",
  "birthday": "2025-04-05",
  "email": "user@example.com"
}'
```

In this case, the `birthday` value of `"2025-04-05"` results in an age calculation that falls outside the valid range (18–64 years), which triggers an error.

#### Example Response (422 Unprocessable Entity)

```json
{
    "detail": [
        {
            "type": "value_error",
            "loc": ["body", "birthday"],
            "msg": "Value error, Age must be between 18 and 64 years old.",
            "input": "2025-04-05",
            "ctx": {
                "error": {}
            }
        }
    ]
}
```

The response clearly indicates the error type (`value_error`) and points to the location in the request body where the validation failed (`birthday`). The error message specifies that the provided `birthday` results in an invalid age, and it is rejected as a result.

#### Example Request (Invalid: Email Validation)

```bash
curl -X 'POST' \
  'http://localhost:8000/v0/employees' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "jane",
  "last_name": "tall",
  "birthday": "2005-04-05",
  "email": "user@example.com"
}'
```

In this case, the `email` value does not match the expected value `"jtall@example.com"`, and validation fails.

#### Example Response (422 Unprocessable Entity)

```json
{
    "detail": [
        {
            "type": "value_error",
            "loc": ["body"],
            "msg": "Value error, Email must be null or equal to 'jtall@example.com'.",
            "input": {
                "first_name": "jane",
                "last_name": "tall",
                "birthday": "2005-04-05",
                "email": "user@example.com"
            },
            "ctx": {
                "error": {}
            }
        }
    ]
}
```

This response indicates that the `email` field does not meet the validation rules. Specifically, the email provided does not match the expected value `"jtall@example.com"`, and thus the request is rejected with a `422 Unprocessable Entity` error.

Thank you for pointing that out! Here's an updated explanation that includes the missing query parameter error:

### Search Employees by Name

```http
GET /v0/employees/search-by-name
```

This endpoint allows users to search for employees by their first and last names. Both `first_name` and `last_name` are required query parameters, and FastAPI will automatically handle the validation and parsing of these values using the `NameParams` model. The model checks that the `first_name` and `last_name` fields contain only alphabetic characters and applies capitalization formatting to ensure consistency.

#### Pydantic Model for Name Validation

```python
class NameParams(BaseModel):
    first_name: str
    last_name: str
```

### Example Request (200 Success)

```bash
curl -X 'GET' \
  'http://localhost:8000/v0/employees/search-by-name?first_name=john&last_name=doe' \
  -H 'accept: application/json'
```

In this case, the request includes both the `first_name` and `last_name` query parameters. The names are validated and properly formatted by the `NameParams` model. If the employee `"John Doe"` exists in the database, the response will include their details.

```json
{
    "status": "success",
    "employees": [
        {
            "id": "ccbd5cb5-1850-4a48-97c2-dccc11b4b935",
            "first_name": "John",
            "last_name": "Doe",
            "birthday": "1981-01-01",
            "email": "jdoe@example.com"
        }
    ]
}
```

### Example Request (404 Not Found)

```bash
curl -X 'GET' \
  'http://localhost:8000/v0/employees/search-by-name?first_name=justice&last_name=doe' \
  -H 'accept: application/json'
```

This request searches for an employee named `"Justice Doe"`. Since no such employee exists in the database, the response will return a `404 Not Found` error.

```json
{
    "detail": "No employees found in the specified age range"
}
```

### Example Request (422 Missing Query Parameter)

```bash
curl -X 'GET' \
  'http://localhost:8000/v0/employees/search-by-name?first_name=john' \
  -H 'accept: application/json'
```

If the `last_name` query parameter is missing, FastAPI will automatically return a `422 Unprocessable Entity` error, since the `last_name` is required. The response will indicate that the `last_name` field is missing:

```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["query", "last_name"],
            "msg": "Field required",
            "input": { "first_name": "john" }
        }
    ]
}
```

This behavior ensures that both `first_name` and `last_name` are always provided, helping maintain data consistency and integrity.

### Key Takeaways

-   **Required Query Parameters**: Both `first_name` and `last_name` are required for this endpoint. If either is missing, FastAPI automatically raises a validation error.
-   **Name Validation**: The `NameParams` model ensures that the names contain only alphabetic characters and applies consistent formatting.
-   **Flexible Error Handling**: When missing or invalid parameters are provided, FastAPI returns clear and descriptive error messages, allowing for easy debugging.
