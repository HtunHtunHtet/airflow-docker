# Apache Airflow Docker Setup with MySQL

This project provides a complete Apache Airflow environment using Docker Compose, configured with CeleryExecutor, Redis, and MySQL for local development and testing.

## Architecture

The setup includes the following services:
- **Airflow Webserver**: Web UI for managing workflows
- **Airflow Scheduler**: Schedules and monitors DAG execution
- **Airflow Worker**: Executes tasks using Celery
- **Airflow Triggerer**: Handles deferred tasks and sensors
- **MySQL**: Metadata database (8.0)
- **Redis**: Message broker for Celery

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of RAM available for Docker (6GB recommended)
- Docker Compose v2.0+

## Quick Start

### 1. Clone and Navigate
```bash
cd /your/work/directory
```

### 2. Build Custom Airflow Image (First Time Only)
```bash
docker-compose build
```

### 3. Initialize Airflow Database (First Time Only)
```bash
docker-compose up airflow-init
```

### 4. Start All Services
```bash
# Start database services first
docker-compose up -d --no-deps mysql redis

# Wait for databases to be ready, then start Airflow services
sleep 10 && docker-compose up -d --no-deps airflow-webserver airflow-scheduler
```

### 5. Access Airflow Web UI
Open your browser and navigate to: http://localhost:8080

**Default Credentials:**
- Username: `airflow`
- Password: `airflow`

## Project Structure

```
airflow-docker/
├── docker-compose.yaml    # Docker Compose configuration
├── Dockerfile            # Custom Airflow image with MySQL support
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── dags/                  # Airflow DAG files
├── plugins/               # Custom Airflow plugins
├── config/                # Airflow configuration files
├── logs/                  # Airflow logs (auto-generated, not in Git)
└── README.md             # This file
```

## Configuration

### Environment Variables
The project uses a `.env` file for configuration:
- `AIRFLOW_UID=501` - User ID for Airflow containers
- `_PIP_ADDITIONAL_REQUIREMENTS=pymysql` - MySQL Python driver

### Key Configuration Details
- **Airflow Version**: 2.10.2
- **Executor**: CeleryExecutor
- **Database**: MySQL 8.0 (with pymysql driver)
- **Message Broker**: Redis 7.2
- **Web UI Port**: 8080
- **Custom Image**: Extended with pymysql for MySQL connectivity

### Database Connection
- **Connection String**: `mysql+pymysql://airflow:airflow@mysql/airflow`
- **Host**: mysql (Docker service name)
- **Database**: airflow
- **User**: airflow
- **Password**: airflow


## Common Commands

### Service Management
```bash
# Build custom image (after Dockerfile changes)
docker-compose build

# Start database services first, then Airflow services (recommended method)
docker-compose up -d --no-deps mysql redis && sleep 10 && docker-compose up -d --no-deps airflow-webserver airflow-scheduler

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart airflow-webserver

# View service status
docker-compose ps

# View logs
docker-compose logs -f airflow-webserver
docker-compose logs -f airflow-scheduler
```

### Database Management
```bash
# Initialize database (first time only)
docker-compose up airflow-init

# Reset database (clean slate)
docker-compose down -v
docker-compose build
docker-compose up airflow-init
```

### Maintenance
```bash
# Remove all containers and volumes (clean slate)
docker-compose down -v

# Access Airflow CLI
docker-compose exec airflow-webserver airflow --help

# Access MySQL database
docker-compose exec mysql mysql -u airflow -p airflow
```
