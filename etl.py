from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
import pandas as pd
import mysql.connector

start_date = datetime(2025, 7, 14)

dag = DAG(
    'etl_stock_to_mysql',
    schedule=None,
    start_date=start_date,
    catchup=False
)

# Task 1: Buat tabel di MySQL
create_table = MySqlOperator(
    task_id='create_table_mysql',
    mysql_conn_id='mysql-local',
    sql="""
    CREATE TABLE IF NOT EXISTS stock_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATETIME,
        open_price DECIMAL(10,2),
        high_price DECIMAL(10,2),
        low_price DECIMAL(10,2),
        close_price DECIMAL(10,2),
        volume BIGINT
    );
    """,
    dag=dag,
)

# Task 2: Extract & Transform
def extract_transform():
    file_path = "dags/data/BTC-USD.csv"  # File input tetap di lokasi semula
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    df.to_csv("/tmp/BTC-USD-transformed.csv", index=False)  # Simpan ke /tmp

df_task = PythonOperator(
    task_id='extract_transform',
    python_callable=extract_transform,
    dag=dag,
)

# Task 3: Load ke MySQL
def load_to_mysql():
    connection = BaseHook.get_connection("mysql-local")
    db_conn = mysql.connector.connect(
        host=connection.host,
        user=connection.login,
        password=connection.password,
        database=connection.schema,
        port=connection.port
    )

    df = pd.read_csv("/tmp/BTC-USD-transformed.csv")  # Baca dari /tmp
    cursor = db_conn.cursor()
    insert_query = """
    INSERT INTO stock_data (date, open_price, high_price, low_price, close_price, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']
        ))
    db_conn.commit()
    cursor.close()
    db_conn.close()

load_task = PythonOperator(
    task_id="load_to_mysql",
    python_callable=load_to_mysql,
    dag=dag,
)

create_table >> df_task >> load_task
