from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import time

# Funciones de tareas
def inicio():
    print("¡El DAG ha comenzado!")

def esperar():
    time.sleep(5)
    print("Esperando 5 segundos...")

def fin():
    print("¡El DAG ha finalizado!")

# Definir el DAG
with DAG(
    dag_id="simple_dag",
    description="Un DAG simple con tres tareas en Docker",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False
) as dag:

    tarea_inicio = PythonOperator(
        task_id="inicio",
        python_callable=inicio
    )

    tarea_esperar = PythonOperator(
        task_id="esperar",
        python_callable=esperar
    )

    tarea_fin = PythonOperator(
        task_id="fin",
        python_callable=fin
    )

    # Definir flujo de tareas
    tarea_inicio >> tarea_esperar >> tarea_fin
