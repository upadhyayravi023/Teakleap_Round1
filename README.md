# Candidate Management API

A robust, enterprise-grade generic Candidate Management API built to industry standards using Python and FastAPI, designed with Clean / Domain-Driven Architecture layout and Dependency Injection.

## Features completed
- Layers separated into Routers, Services, Schemas, and Repositories.
- Dependency Injection through FastAPI's `Depends` for decoupled logical boundaries.
- Uses `Pydantic` including `EmailStr` and standard Python `Enum` for stringent validation.
- Mock asynchronous in-memory data store using abstracted repository pattern.
- Robust global exception handling integrated with FastAPI context.

## Requirements
To run this application verify you have Python 3.10+ installed.

### Setup

1. Install dependencies from ``requirements.txt``:
```sh
pip install -r requirements.txt
```

2. Run the application:
```sh
uvicorn app.main:app --reload
```

3. Open Swagger Documentation:
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the API directly using the automatically generated Swagger UI.
