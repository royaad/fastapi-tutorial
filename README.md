# FastAPI Tutorial

## Prerequisites

### What is a REST API

A REST (Representational State Transfer) API is an architectural style that defines a set of constraints to be used for creating web services. REST APIs allow different software applications to communicate over the web using HTTP requests. These APIs are stateless, meaning each request from a client contains all the information needed for the server to fulfill that request.

#### Benefits of REST APIs:

- **Scalability**: REST APIs separate client and server concerns, making it easier to scale applications.
- **Statelessness**: Each request is independent, which simplifies the server-side logic and reduces server load.
- **Cacheability**: Responses can be cached, improving performance by reducing server load.
- **Flexibility and Portability**: REST APIs can be consumed by any client that understands HTTP, making them highly versatile.
- **Easy to Use and Learn**: REST APIs follow standard HTTP methods, making them intuitive for developers familiar with web development.

### REST API Requests

REST API requests utilize standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on resources. The mapping between CRUD operations and HTTP methods is as follows:

| Operation | HTTP Method |
| --------- | ----------- |
| Create    | POST        |
| Read      | GET         |
| Update    | PUT         |
| Delete    | DELETE      |

### HTTP Status Codes

When a request is made to a REST API, it returns an HTTP status code in the response. These status codes provide information about the result of the request and can be grouped into five categories: 100s, 200s, 300s, 400s, and 500s.

<div style="background: #d9edf7; padding: 10px; border: 2px solid #bcdff1; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #31708f;">🛈 Informational Responses (1XX)</p>
</div>

The `1XX` status codes indicate informational responses.

- **100**: Continue - The initial part of a request has been received, and the client should continue with the request.
- **101**: Switching Protocols - The server is switching protocols as requested by the client, such as from HTTP to WebSocket.

<div style="background: #d4edda; padding: 10px; border: 2px solid #c3e6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #155724;">✅ Successful Responses (2XX)</p>
</div>

The `2XX` status codes indicate that the request was successfully processed by the server.

- **200**: OK - The request was successful.
- **201**: Created - The request was successful, and a new resource was created.
- **204**: No Content - The request was successful, but there is no content to send back (commonly used for DELETE operations).

<div style="background: #fff3cd; padding: 10px; border: 2px solid #ffeeba; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #856404;">🔀 Redirection Messages (3XX)</p>
</div>

The `3XX` status codes indicate that further action needs to be taken by the client to complete the request, usually involving redirection.

- **301**: Moved Permanently - The resource has been permanently moved to a new URL.
- **302**: Found - The resource is temporarily located at a different URL.
- **304**: Not Modified - The resource has not been modified since the last request (used for caching).
- **307**: Temporary Redirect - The request should be repeated with another URL, but the method and the body of the original request must be used. Unlike `302`, `307` guarantees that the method used in the original request (e.g., POST) will not be changed to GET.

<div style="background: #f8d7da; padding: 10px; border: 2px solid #f5c6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #d6336c;">⛔ Client Error Responses (4XX)</p>
</div>

The `4XX` status codes indicate client-side errors.

- **401**: Unauthorized - The client must authenticate itself to get the requested response.
- **403**: Forbidden - The client does not have access rights to the content.
- **404**: Not Found - The server could not find the requested resource.
- **429**: Too Many Requests - The user has sent too many requests in a given amount of time (rate limiting).

<div style="background: #f8d7da; padding: 10px; border: 2px solid #f5c6cb; display: flex; align-items: center; height: 50px; border-radius: 5px;">
  <p style="margin: 0; font-size: 18px; font-weight: bold; color: #721c24;">⚠ Server Error Responses (5XX)</p>
</div>

The `5XX` status codes indicate server-side errors.

- **500**: Internal Server Error - The server has encountered a situation it doesn't know how to handle.
- **502**: Bad Gateway - The server received an invalid response from the upstream server.
- **503**: Service Unavailable - The server is not ready to handle the request, often due to maintenance or overload.

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
