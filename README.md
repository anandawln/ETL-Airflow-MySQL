
## Prerequisites
- Docker installed ([Get Docker](https://www.docker.com/))
- Docker Compose installed
- Astronomer CLI ([Install Astro CLI](https://www.astronomer.io/docs))

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/anandawln/ETL-pipeline
    cd repository
    ```

2. Start Docker services using Docker Compose:
    ```bash
    docker-compose up
    ```

3. Open Astro CLI to initialize and manage your Airflow setup:
    ```bash
    astro dev start
    ```

4. Access the Airflow web interface:
    - URL: `http://localhost:8080`
    - Default username/password: `admin/admin`

## How It Works
1. **Extraction**: Pulls data from a source system (e.g., API, database).
2. **Transformation**: Processes and cleans the data using custom Python scripts in DAGs.
3. **Loading**: Saves the data to a target storage system (e.g., database, data lake).

## Usage
- Modify the DAGs in the `dags/` directory to fit your specific ETL logic.
- Customize Dockerfile and `docker-compose.yml` to add dependencies or services.
- Monitor and debug tasks via the Airflow web interface.

## License
This project is licensed under the [MIT License](LICENSE).

---
