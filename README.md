# ETL-Airflow-MySQL

## Introduction
This project demonstrates a simple ETL pipeline that extracts historical stock (BTC-USD) data from a CSV file, performs a minimal transformation, and loads the processed rows into a MySQL table using an Apache Airflow DAG. It's built to run with the Astro (Astronomer) CLI and Docker for local development and testing.

## What this does
- Creates a MySQL table (if it doesn't exist).
- Extracts and transforms a CSV file located at `dags/data/BTC-USD.csv` (removes timezone information from the Date column and writes a transformed CSV to `/tmp`).
- Loads the transformed CSV rows into the `stock_data` table in MySQL.

## Stack
- Language(s): Python (Airflow DAGs) and Shell (helper script)
- Framework / runtime: Apache Airflow (recommended: Astro runtime via Astro CLI)
- Notable libraries: pandas, mysql-connector-python, apache-airflow-providers-mysql

## Requirements
- Astro CLI (for running the Astro/Airflow runtime locally)
- Docker Desktop
- A running MySQL server (MySQL Workbench or a MySQL Docker container)

The repository already includes a `requirements.txt` listing the minimal Python packages used by the DAG.

## Files of interest
```
README.md                      Project introduction and instructions
etl.py                         Airflow DAG: extract -> transform -> load
requirements.txt               Python dependencies (providers, mysql connector)
airflow_project_setup.sh       Helper script for starting Astro and checking MySQL/docker
```

## How it's organized
```
.
├─ dags/                        (add your DAGs or place data under dags/data/)
├─ etl.py                       Airflow DAG that runs the ETL pipeline
├─ requirements.txt             Python package requirements
├─ airflow_project_setup.sh     Example helper script for local dev with Astro/Docker/MySQL
└─ README.md                    This file
```

How it fits together: The Airflow DAG defined in `etl.py` contains three tasks: a MySqlOperator that ensures the `stock_data` table exists, a PythonOperator that reads and transforms `dags/data/BTC-USD.csv` and writes a temp file, and a PythonOperator that reads the transformed CSV from `/tmp` and inserts rows into MySQL using the Airflow connection `mysql-local`.

## Quick start (local development)
1. Clone the repository:
```
git clone https://github.com/anandawln/ETL-Airflow-MySQL.git
cd ETL-Airflow-MySQL
```
2. Start the Astro/Airflow environment (requires Astro CLI & Docker):
```
astro dev start
```
3. Ensure MySQL is available and reachable. Options:
   - Start a local MySQL server (system service) and ensure port 3306 is accessible.
   - Or run a MySQL Docker container and expose port 3306 to the host.

4. Configure the Airflow connection used by the DAG:
   - Open the Airflow UI (usually at http://localhost:8080 when using Astro).
   - Go to Admin → Connections and create a connection with Conn Id `mysql-local`:
     - Conn Type: MySQL
     - Host: (e.g. host.docker.internal or your MySQL host)
     - Schema: the database name (e.g. `etl_db`)
     - Login: user (e.g. `root`)
     - Password: your DB password
     - Port: 3306

5. Place your CSV data at `dags/data/BTC-USD.csv` (the DAG expects this path).
6. Trigger the DAG named `etl_stock_to_mysql` from the Airflow UI or using the CLI:
```
# to trigger via CLI inside the Astro/Airflow container
airflow dags trigger etl_stock_to_mysql
```

## Notes & tips
- The ETL DAG writes a transformed CSV to `/tmp/BTC-USD-transformed.csv`. Ensure the Airflow worker/container has permissions to read/write `/tmp`.
- The DAG uses an Airflow connection named `mysql-local`. If you change the connection id, update `etl.py` accordingly.
- The project is intentionally minimal to illustrate the pattern; for production use you should add batching, upserts, schema validation, error handling, and idempotency.

## Example commands from the helper script
The `airflow_project_setup.sh` contains examples for starting Astro, checking Docker containers, and attempting to run MySQL client commands inside the Airflow container. It is provided for convenience and may require sudo or container names that match your environment.

---

If you want, I can also:
- Add a usage example showing the required SQL to create the database used by MySQL.
- Add a Docker Compose file to launch a MySQL container for local testing.

