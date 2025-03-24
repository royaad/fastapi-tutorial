# Writing Your First API App

The [[01_basic_crud.py]] file contains a basic FastAPI application to demonstrate the core features of FastAPI, including handling GET, POST, and DELETE requests, parsing path and query parameters, and performing health checks.
### Running the Application

To run the FastAPI server using Uvicorn, follow these steps:

1. Open your terminal or command prompt.

2. Navigate to the directory where your FastAPI application (Python file) is located.

3. Execute the following command:

   ```powershell
   python -m uvicorn <py_file>:<fastapi_instance> --reload
   ```

Replace `<py_file>` with the name of your Python file (without the `.py` extension) and `<fastapi_instance>` with the name of your FastAPI instance or app.

The `--reload` flag enables automatic reloading of the server whenever code changes are detected.

To run the FastAPI application, use the following command:

Note: uvicorn works on port 8000 by defalt
## API Endpoints

The created app has a few endpoints

### Health Check

```http
GET /v0/healthcheck
```

it is always a good idea to have a `healthcheck` or a `heartbeat` endpoint that uses the get method. this endpoint is usually used to check if the server is ok so that when we are debugging an API request error we are sure at first that we can reach it and it is operational
this endpoint usually should return basic like below with a timestamp preferrably to make sure that the return response is a recent one.

```json
{
    "status": "ok",
    "service": "tutorial 1",
    "timestamp": "2025-03-24T13:06:23Z"
}
```

### Employee Endpoint

This endpoint supports various methods to handle employee-related operations. and serves as an example on how to use the various http methods. the endpoint serves also to show the parsing capabilities of fdastapi.

for example the endpoiunt

```http
GET /v0/employee/{employee_id}
```

fast api parses the `employee_id` to the correct type as indicated in the type hinting

```python
@app.get("/v0/employee/{employee_id}")
def get_employee(employee_id: str):
    return {"status": f"{employee_id} requested"}
```

### Get Employee Info and get Item Availabiltiy


those endpoint serve to show how query parsing works in fastapi.,

## Swagger UI

to check the docuymentation you can go to 

```plaintext
http://localhost:8000/docs
```

## cURL


curl -X 'GET' \

  'http://localhost:8000/v0/employee/1/info/salary' \

  -H 'accept: application/json'

  

  {

  "status": "salary of employee with employee_id=1 queried without parameters"

}

  

curl -X 'GET' \

  'http://localhost:8000/v0/employee/1/info/salary?q=min%3D1%26max%3D5' \

  -H 'accept: application/json'

  

  {

  "status": "salary of employee with employee_id=1 queried with parameters min=1&max=5"

}