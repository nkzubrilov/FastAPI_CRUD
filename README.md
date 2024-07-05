# FastAPI CRUD Application

## Overview

This project is a CRUD (Create, Read, Update, Delete) application built with FastAPI. It includes:
- A RESTful API for managing CRUD operations.
- Integration with a PostgreSQL database.
- Dockerized setup for easy deployment.
- CI/CD pipeline for automated testing, building, and deployment using GitHub Actions.

The application is deployed on an AWS EC2 instance and can be accessed at [fastapi-crud.xyz](http://fastapi-crud.xyz).

## Technologies Used

### Backend
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [JWT](https://jwt.io/)

### Database
- [PostgreSQL](https://www.postgresql.org/)

### ORM and Migrations
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)

### Containerization
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### CI/CD
- [GitHub Actions](https://github.com/features/actions)

### Cloud
- [AWS EC2](https://aws.amazon.com/ec2/)

### Web Server
- [Nginx](https://www.nginx.com/)

### SSL/TLS
- [Certbot](https://certbot.eff.org/)

### Operating System
- [Ubuntu](https://ubuntu.com/)

## Getting Started

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- PostgreSQL

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
2. **Set up environment variables:** \
Create a env.env file in the root directory with the following content:
   ```env
   DB_HOSTNAME=your_db_hostname
   DB_PORT=your_db_port
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   SECRET_KEY=your_secret_key
   ALGORITHM=your_algorithm
   TOKEN_EXPIRE_MINUTES=your_token_expire_minutes
   ```
3. Install dependencies:
   ```commandline
   pip install -r requirements.txt
   ```
4. Run the application:
   ```commandline
   uvicorn main:app --reload
   ```
   
### Docker
To run the application using Docker:

1. **Build and start containers:**
   ```commandline
   docker-compose up --build
   ```
2. **Stop containers:**
   ```commandline
   docker-compose down
   ```