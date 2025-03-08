# FastAPI Tutorial

## Prerequisites

### What is a REST API

A REST (Representational State Transfer) API is an architectural style that defines a set of constraints to be used for creating web services. REST APIs allow different software applications to communicate over the web using HTTP requests. These APIs are stateless, meaning each request from a client contains all the information needed for the server to fulfill that request.

#### Benefits of REST APIs

- **Scalability**: REST APIs separate client and server concerns, making it easier to scale applications.
- **Statelessness**: Each request is independent, which simplifies the server-side logic and reduces server load.
- **Cacheability**: Responses can be cached, improving performance by reducing server load.
- **Flexibility and Portability**: REST APIs can be consumed by any client that understands HTTP, making them highly versatile.
- **Easy to Use and Learn**: REST APIs follow standard HTTP methods, making them intuitive for developers familiar with web development.

## Basics

### Installation

To get started with FastAPI, you'll first need to install FastAPI and an ASGI server, such as Uvicorn. Use the following command:

```powershell
pip install fastapi uvicorn
```

This tutorial uses FastAPI version `0.114.0` and Uvicorn version `0.30.6`.

FastAPI relies on Pydantic for data validation and settings management. To ensure compatibility, upgrade Pydantic to version `2.9.0`:

```powershell
pip install --upgrade pydantic
```

### Running the Server and Accessing Documentation

To run the FastAPI server using Uvicorn, follow these steps:

1. Open your terminal or command prompt.

2. Navigate to the directory where your FastAPI application (Python file) is located.

3. Execute the following command:

   ```powershell
   python -m uvicorn <py_file>:<fastapi_instance> --reload
   ```

   Replace `<py_file>` with the name of your Python file (without the `.py` extension) and `<fastapi_instance>` with the name of your FastAPI instance or app.

   The `--reload` flag enables automatic reloading of the server whenever code changes are detected.

4. Once the server is running, you can access the FastAPI documentation. Open any web browser and visit:

   ```http
   http://localhost:8000/docs
   ```

   This URL will take you to the interactive API documentation provided by FastAPI. You'll find detailed information about your API endpoints, request parameters, and response formats.

### Basic CRUD Operations

The `1_basic_crud.py` example demonstrates fundamental CRUD (Create, Read, Update, Delete) operations using an in-memory employee database. Here's what each endpoint does:

1. **Heartbeat Endpoint (`/heartbeat`):**

   - Provides a simple status response to indicate that the service is operational.
   - Includes the current timestamp.
   - Decorated with `@app.get("/heartbeat")`.

2. **Square Endpoint (`/square`):**

   - Accepts an integer input (`number`).
   - Computes the square of the input number.
   - Returns the result as a JSON response.
   - Decorated with `@app.post("/square")`.

3. **Get Employee Database Endpoint (`/get_employee_db`):**

   - Retrieves the in-memory employee database (loaded from a JSON file).
   - Returns the entire employee database as a JSON response.
   - Decorated with `@app.get("/get_employee_db")`.

4. **Add Employee Endpoint (`/add_employee`):**

   - Accepts an employee object (validation is simplified here; consider using a `BaseModel` in production).
   - Generates a new employee ID based on existing keys.
   - Adds the employee to the in-memory database.
   - Returns a status message indicating successful addition.
   - Decorated with `@app.put("/add_employee")`.

5. **Delete Employee Endpoint (`/delete_employee`):**
   - Accepts an employee ID.
   - Checks if the employee exists in the database.
   - Removes the employee if found.
   - Returns a status message indicating successful deletion or if the employee was not found.
   - Decorated with `@app.delete("/delete_employee")`.

> [!NOTE]
>
> - This example intentionally keeps things basic and lacks robust validation and error handling.
> - In a production environment, use a proper database (e.g., PostgreSQL, MongoDB) and implement thorough API validation and error responses.

Remember to decorate each function with the appropriate FastAPI method (`@app.get`, `@app.post`, `@app.put`, or `@app.delete`) to map it to the corresponding endpoint.

## Advanced

_Discuss advanced topics like middleware, dependency injection, background tasks, WebSocket, and OAuth2._

## References

- [Markdown Admonition](https://stackoverflow.com/questions/50544499/github-flavored-markdown-how-to-make-a-styled-admonition-box-in-a-gist)
