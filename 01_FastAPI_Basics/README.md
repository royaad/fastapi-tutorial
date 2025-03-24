# FastAPI Basics

After introducing some HTTP and API design basics, let's dive into building a very basic FastAPI app. This app won't be highly efficient or professional yet, but it will serve to demonstrate how FastAPI works and what it offers. You might encounter a few unexplained terms in this README file, such as ASGI or OpenAPI. Don't worry about them for now; we'll explain them later. For now, let's focus on installing and building a basic app.

## What is FastAPI?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use and to help developers build applications quickly and efficiently.

### Key Features of FastAPI

1. **ASGI Compatibility**: FastAPI is built on the Asynchronous Server Gateway Interface (ASGI), which is a standard for asynchronous web servers and applications in Python. This allows FastAPI to handle many concurrent connections efficiently.

2. **Uvicorn**: FastAPI applications are typically run using Uvicorn, a lightning-fast ASGI server implementation. Uvicorn is designed to offer high performance and is often the preferred choice for running FastAPI applications.

3. **OpenAPI Documentation**: FastAPI automatically generates OpenAPI documentation for your API. OpenAPI is a standard for defining APIs, and FastAPI uses it to create interactive API documentation with tools like Swagger UI. This makes it easy to explore and test your API endpoints.

4. **Automatic JSON Conversion**: FastAPI automatically converts request and response bodies to and from JSON, making it easy to work with JSON data.

5. **Request Validation**: FastAPI uses Pydantic models to validate request data. Pydantic allows you to define data models with type annotations, and FastAPI ensures that incoming requests conform to these models.

## Installation

To get started with FastAPI, you'll first need to install FastAPI and an ASGI server, such as Uvicorn. Use the following command:

```powershell
pip install fastapi uvicorn
```

FastAPI relies on Pydantic for data validation and settings management. To ensure compatibility, upgrade Pydantic:

```powershell
pip install --upgrade pydantic
```

## Writing and Running Your First FastAPI App

For this section check [[00_Writing_Your_First_Fast_API_APP.md]]
