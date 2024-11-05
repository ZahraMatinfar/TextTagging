# Text Tagging and Dataset Management

A Django REST API system for managing text datasets, tagging, and generating daily operator performance reports. The application is dockerized with PostgreSQL as the database, Celery for background tasks, and Redis as the message broker.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Environment Setup](#environment-setup)
- [Running the Project with Docker](#running-the-project-with-docker)
- [Testing](#testing)
- [API Documentation](#api-documentation)

## Features
- **Text Dataset Management**: Create and manage text datasets.
- **Tagging System**: Tag texts within datasets by categories.
- **Daily Reports**: Automated daily reporting of operator tagging activities, saved to the `DatasetReport` model.
- **API Documentation**: OpenAPI documentation available via `drf_spectacular`.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery with Redis as the broker
- **Database**: PostgreSQL
- **Docker**: For containerization
- **Pandas**: For report generation

## Environment Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ZahraMatinfar/TextTagging.git
 

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**:

    ``` bash
    pip install -r requirements.txt

4. **Configure environment variables**:

    Create a .env file in the project root directory based on the .env.example file.

## Running the Project with Docker
1. **Ensure Docker and Docker Compose are installed.**

2. **Build and run the containers**:

    ```bash 
    docker-compose up --build

3. **Create a superuser**:

    ```bash
    docker-compose exec web python manage.py createsuperuser

## Testing:
Run the tests with:

    docker-compose exec web python manage.py test

## API Documentation:
The API documentation is available at /api/schema/docs/ once the server is running, generated with drf-spectacular.