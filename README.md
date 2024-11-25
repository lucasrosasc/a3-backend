# a3-backend

This project is a Python-based API built with FastAPI for performing betting data analysis. It provides a scalable and efficient framework for collecting, processing, and analyzing betting information from various sources, enabling insights into betting patterns, trends, and statistics.

## Setting up environment


### Copy development environment variables

```bash
$ cp .env.example .env
```

### Dependencies

- python = v3.11.0

### Install Project Dependencies

```bash
$ pip install -r requirements.txt
```

# Run project

```bash
$ uvicorn main:app --reload
```

### Documentation is only available when the project is running 

```bash
$ http://localhost:8000/docs
```

## Database Setup

### Prerequisites
- Docker and Docker Compose installed on your machine
- PostgreSQL client (optional, for direct database access)

### Running the Database

1. Start the PostgreSQL container:
```bash
$ docker-compose up -d
```

2. Verify the container is running:
```bash
$ docker-compose ps
```

3. Stop the database:
```bash
$ docker-compose down
```

4. To completely reset the database (removes all data):
```bash
$ docker-compose down -v
```

### Database Connection Details
- Host: localhost
- Port: 5432
- Database: betting_predictions
- Username: postgres
- Password: postgres

### Troubleshooting
If you encounter database connection issues:
1. Ensure the database container is running
2. Check if port 5432 is available on your machine
3. Verify your .env file matches the database credentials
4. Try resetting the database with `docker-compose down -v` followed by `docker-compose up -d`
