# Writing Your First FastAPI

## Overview

The `00_basic_crud.py` file contains a simple FastAPI application designed to demonstrate key FastAPI features. These include handling GET, POST, and DELETE requests, parsing path and query parameters, and performing health checks.

## Running the Application

To start the FastAPI server using Uvicorn, follow these steps:

1. Open your terminal or command prompt.
    
2. Navigate to the directory containing your FastAPI application.
    
3. Execute the following command:
    

```powershell
python -m uvicorn 00_basic_crud:app --reload
```

The `--reload` flag enables automatic reloading of the server whenever code changes are detected.

**Note:** Uvicorn defaults to port 8000 unless specified otherwise.

## API Endpoints

### Health Check Endpoint

```http
GET /v0/healthcheck
```

A `healthcheck` or `heartbeat` endpoint is crucial for verifying the server's operational status. It is commonly used when debugging API errors to confirm that the server is reachable and functioning correctly.

**Example Response:**

```json
{
    "status": "ok",
    "service": "tutorial 1",
    "timestamp": "2025-03-24T13:06:23Z"
}
```

The timestamp follows the ISO 8601 format for consistency.

### Employee Endpoint

The employee endpoint supports multiple HTTP methods to manage employee-related operations. It also demonstrates FastAPI's path parameter parsing capabilities.

**Examples:**

**GET Request:**

```http
GET /v0/employee/{employee_id}
```

```python
@app.get("/v0/employee/{employee_id}")
def get_employee(employee_id: str):
    return {"status": f"{employee_id} requested"}
```

**POST Request:**

```http
POST /v0/employee/{employee_id}
```

```python
@app.post("/v0/employee/{employee_id}")
async def create_employee(employee_id: str):
    return {"status": f"employee {employee_id=} created"}
```

**DELETE Request:**

```http
DELETE /v0/employee/{employee_id}
```

```python
@app.delete("/v0/employee/{employee_id}")
async def delete_employee(employee_id: str):
    return {"status": f"employee {employee_id} deleted"}
```

### Employee Information and Item Availability Endpoints

**GET Employee Info with Optional Query Parameters:**

```http
GET /v0/employee/{employee_id}/info/{info_str}?q=min%3D1%26max%3D5
```

**Example Response:**

```json
{
    "status": "salary of employee with employee_id=1 queried with parameters min=1&max=5"
}
```

**GET Item Availability with Required Query Parameter:**

```http
GET /v0/items/{items_id}?available=true
```

**Example Response:**

```json
{
    "status": "items_id=1 is available=True"
}
```

### Advanced Employee Search Endpoint

For advanced queries using `Query` parameters:

```http
GET /v0/employees?age=30&in_office=true
```

**Example Response:**

```json
{
    "status": "get for employees with age=30 and in office"
}
```

## FastAPI's Parsing and Exception Handling

FastAPI includes powerful parsing and validation capabilities that automatically handle invalid data. For instance, the following request will return a **422 Unprocessable Entity** error:

```http
GET /v0/items/t?available=true HTTP/1.1
```

**Example Error Response:**

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": ["path", "items_id"],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "t"
        }
    ]
}
```

This occurs because the `items_id` parameter expects an integer, but the path provided (`t`) is a string. FastAPI automatically detects such issues and returns informative error messages, simplifying debugging and improving API reliability.

## Synchronous vs Asynchronous Code in FastAPI

FastAPI is optimized to handle asynchronous code efficiently, but it also fully supports synchronous code. In the provided examples, both `async def` and regular `def` functions are used.

- Asynchronous functions (`async def`) are ideal for I/O-bound tasks like database interactions or HTTP requests.
    
- Synchronous functions (`def`) are still acceptable and work seamlessly in FastAPI.
    

In this example, the two styles are used randomly to demonstrate compatibility. Choosing the most efficient method depends on the nature of the task and will be discussed in detail in future documentation.

While mixing these styles does **not** result in runtime errors, it may introduce latency issues if not managed carefully. This topic is beyond the scope of this basic demonstration but will be covered thoroughly in later documentation.

## Testing the API

Testing is an essential step to ensure your endpoints behave as expected. Below are two effective ways to test your API: using Swagger UI and cURL.

### 1. Swagger UI (Recommended for Visual Testing)

FastAPI automatically generates interactive API documentation, accessible at:

```plaintext
http://localhost:8000/docs
```

The Swagger UI provides a user-friendly interface where you can test your endpoints directly from the browser.

### 2. cURL (Recommended for Command-Line Testing)

cURL is useful for automated testing or when you prefer command-line tools.

**Basic Request:**

```bash
curl -X 'GET' \
  'http://localhost:8000/v0/employee/1/info/salary' \
  -H 'accept: application/json'
```

**Response:**

```json
{
    "status": "salary of employee with employee_id=1 queried without parameters"
}
```

**Request with Parameters:**

```bash
curl -X 'GET' \
  'http://localhost:8000/v0/employee/1/info/salary?q=min%3D1%26max%3D5' \
  -H 'accept: application/json'
```

**Response:**

```json
{
    "status": "salary of employee with employee_id=1 queried with parameters min=1&max=5"
}
```

By combining these methods, you can efficiently test your API during development and deployment.
