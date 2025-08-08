# Apache Airflow Docker Setup with MySQL

This project provides a complete Apache Airflow environment using Docker Compose, configured with CeleryExecutor, Redis, and MySQL for local development and testing.

## 🏗️ Architecture

The setup includes the following services:
- **Airflow Webserver**: Web UI for managing workflows
- **Airflow Scheduler**: Schedules and monitors DAG execution
- **Airflow Worker**: Executes tasks using Celery
- **Airflow Triggerer**: Handles deferred tasks and sensors
- **MySQL**: Metadata database (8.0)
- **Redis**: Message broker for Celery

## 📋 Prerequisites

- Docker Desktop installed and running
- At least 4GB of RAM available for Docker (6GB recommended)
- Docker Compose v2.0+

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd /Users/htunhtunhtet/Work/playground/airflow-docker
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
docker-compose up -d --no-deps airflow-webserver airflow-scheduler airflow-worker airflow-triggerer
```

### 5. Access Airflow Web UI
Open your browser and navigate to: http://localhost:8080

**Default Credentials:**
- Username: `airflow`
- Password: `airflow`

## 📁 Project Structure

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

## 🔧 Configuration

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

## 📝 Managing DAGs

1. Place your DAG files in the `dags/` directory
2. DAGs will automatically appear in the Airflow web interface
3. The `dags/` folder is mounted as a volume, so changes are reflected immediately

### Example DAG Structure
```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

start >> end
```

## 🛠️ Common Commands

### Service Management
```bash
# Build custom image (after Dockerfile changes)
docker-compose build

# Start all services (recommended method)
docker-compose up -d --no-deps airflow-webserver airflow-scheduler airflow-worker airflow-triggerer

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

## 🔍 Monitoring and Troubleshooting

### Health Checks
All services include health checks. Check service status:
```bash
docker-compose ps
```

### Common Issues

1. **Memory Warning**: If you see memory warnings:
   - Increase Docker Desktop memory allocation to 6GB+
   - Close other applications to free up RAM

2. **Port Conflicts**: If port 8080 is in use:
   - Stop other services using port 8080
   - Or modify the port mapping in `docker-compose.yaml`

3. **Permission Issues**: Ensure the `AIRFLOW_UID` in `.env` matches your system user ID:
   ```bash
   echo "AIRFLOW_UID=$(id -u)" > .env
   ```

4. **MySQL Connection Issues**: 
   - Ensure MySQL service is healthy: `docker-compose ps`
   - Check MySQL logs: `docker-compose logs mysql`
   - Verify pymysql is installed in custom image

### Viewing Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs airflow-scheduler

# Follow logs in real-time
docker-compose logs -f airflow-webserver
```

## 🔐 Security Notes

⚠️ **Important**: This configuration is for local development only. Do not use in production without proper security hardening:

- Change default passwords
- Configure proper authentication
- Set up SSL/TLS
- Review and harden security settings
- Use secrets management for sensitive data
- Secure MySQL with proper credentials

## 🗄️ Database Information

This setup uses **MySQL 8.0** instead of the default PostgreSQL:

### Why MySQL?
- Familiar database for many developers
- Good performance for Airflow workloads
- Easy to manage and backup

### Connection Details
- **Service**: mysql
- **Port**: 3306 (internal)
- **Database**: airflow
- **Username**: airflow
- **Password**: airflow
- **Driver**: pymysql

### Switching Back to PostgreSQL
If you want to switch back to PostgreSQL:
1. Update `docker-compose.yaml` database service
2. Change connection strings to use `postgresql+psycopg2`
3. Update Dockerfile to install `psycopg2` instead of `pymysql`

## 📚 Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose for Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## 🤝 Contributing

1. Add your DAGs to the `dags/` directory
2. Place custom plugins in the `plugins/` directory
3. Update configuration files in the `config/` directory as needed
4. Test your changes locally before deployment
5. Do not commit `logs/` directory (excluded by .gitignore)

## 📄 License

This project uses the Apache Airflow Docker Compose configuration, which is licensed under the Apache License 2.0.
