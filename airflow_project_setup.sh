#!/bin/bash

echo "🔄 Starting Astro project..."
astro dev start

echo "🐳 Checking active Docker containers..."
docker ps

echo "🔎 Checking if port 3306 is in use..."
sudo lsof -i :3306

echo "🧩 Checking MySQL service status..."
sudo systemctl status mysql

echo "🚀 Starting MySQL service..."
sudo systemctl start mysql

echo "🔐 Connecting to MySQL as root..."
mysql -u root -p

echo "📦 Listing all Docker containers (including stopped)..."
docker ps -a

echo "🗂️ Running SHOW DATABASES inside the Airflow API container..."
docker exec -it my-airflow-project_98cd6a-api-server-1 mysql -h host.docker.internal -u root -p -e "SHOW DATABASES;"

echo "🔧 Updating container and installing mysql-client..."
docker exec -it my-airflow-project_98cd6a-api-server-1 bash -c \
  "apt-get update && apt-get install -y mysql-client && \
  mysql -h host.docker.internal -u root -p -e 'SHOW DATABASES;'"

echo "🔧 (With sudo) Updating container and installing mysql-client..."
docker exec -it my-airflow-project_98cd6a-api-server-1 bash -c \
  "sudo apt-get update && sudo apt-get install -y mysql-client && \
  mysql -h host.docker.internal -u root -p -e 'SHOW DATABASES;'"

echo "🛠️ Opening bash shell inside container as root..."
docker exec -u root -it my-airflow-project_98cd6a-api-server-1 bash