# Simple Blog

This is a simple blog application with three roles: ADMIN, AUTHOR, and READER.

- ADMIN can create users and change their roles from AUTHOR to READER and vice versa.
- ADMIN and AUTHOR can create, update, and delete posts.
- READERS can read posts and write comments on them.

Authentication is done using JWT tokens.

## Frameworks and Libraries
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- SQLModel: A library for interacting with SQL databases using Python type hints.


## Getting Started

To run the project, follow these steps:

1. Copy the `.env.example` file to `.env` and complete the fields.
2. Migrate the database by installing Alembic, making migrations, and upgrading. Copy the `alembic.ini.example` file to `alembic.ini` and Set the database URL in `alembic.ini`.
3. Install the project requirements.
4. Run `main.py` using FastAPI.

or run with docker compose:
1. Run `docker-compose up` to start the project.

## Architecture

The project architecture 

1. **models**: Contains the business logic of the project.
2. **db context**: Handles the database operations.
3. **repositories**: Performs the database operations.
4. **services**: Implements the business logic of the project.
5. **controllers**: Defines the endpoints of the project.
6. **core**: Handles JWT token generation and verification, as well as password hashing.
7. **viewmodels**: Contains the Pydantic models for the request and response of the endpoints.

## Features

The blog application includes the following features:

1. Create user.
2. Change user role.
3. Create post.
4. Update post.
5. Delete post.
6. Get all posts with filters.
7. Write comment on post.
8. Get all comments on post.
9. Create admin.

