from airflow import dag, task, PythonOperator
from pendulum import datetime, duration
from datetime import timedelta
import logging
import googleapiclient.discovery

api_service_name = "Youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAru82hLkwVztVx2xCJIdIzy-rKDMhUeyg"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

log = logging.getLogger("airflow.task")

default_args = {
    'owner':  'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': 'vuaustin1017@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    schedule="@daily",
    catchup=False,
    dagrun_timeout=duration(hours=1),
    default_args=default_args,
    description='First ETL code'
)

def extract_dag():
    @task
    def get_youtube_data():
        # retrieve top 50 searched cat videos' ID
        request = youtube.search().list(
            part="id",
            type='video',
            regionCode="US",
            order="relevance",
            q="kitties",
            maxResults=50,
            fields="items(id(videoId))"
        )
        
        # run the query
        response = request.execute()
        return response.json()

    @task
    def write_data_to_file(response):
        f = open("cats.csv", "a")
        f.write(response)
        f.close()

    @task
    def read_data_from_file():
        f = open("cats.csv", "r")
        log.info(f.read(5))
        f.close()

    write_data_to_file(get_youtube_data()) >> read_data_from_file()


extract_dag()

