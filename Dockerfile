FROM apache/airflow:2.10.2

# Install pymysql for MySQL connectivity
USER airflow
RUN pip install --no-cache-dir pymysql
