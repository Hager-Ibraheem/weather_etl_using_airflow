import requests
import pandas as pd
from tempfile import NamedTemporaryFile
from datetime import datetime , timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args={
    'owner':'hager',
    'start_date': datetime(2024, 9, 3),
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def extract():

    API_key = 'f7e1d21eba18e9326d59148f77bafe65'
    city_name = 'Alexandria'
    request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"

    response = requests.get(request_url)

    if response.status_code == 200:

        weather_data = response.json()

    return weather_data   


def transform_load(ti):

    def kelvin_to_celsius(temp_kelvin):
        temp_celsius=temp_kelvin-273.15
        return temp_celsius

    weather_data=ti.xcom_pull(task_ids='weather_data_extract')
    
    transformed_weather_data={

        'city': weather_data['name'],
        'country_code': weather_data['sys']['country'],
        'temperature (C)': kelvin_to_celsius(weather_data['main']['temp']),
        'feels_like (C)': kelvin_to_celsius(weather_data['main']['feels_like']),
        'weather_description': weather_data['weather'][0]['description'],
        'pressure': weather_data['main']['pressure'],
        'humidity': weather_data['main']['humidity'],
        'wind_speed': weather_data['wind']['speed'],
        'cloudiness': weather_data['clouds']['all'],
        'time_of_calculation': datetime.utcfromtimestamp(weather_data['dt']+ weather_data['timezone']),
        'sunrise_time': datetime.utcfromtimestamp(weather_data['sys']['sunrise']+ weather_data['timezone']),
        'sunset_time': datetime.utcfromtimestamp(weather_data['sys']['sunset']+ weather_data['timezone'])

    }
    dt= transformed_weather_data['time_of_calculation']

    weather_df=pd.DataFrame([transformed_weather_data])

    with NamedTemporaryFile(mode='w', suffix='.csv') as f:
        weather_df.to_csv(f.name, index=False)

        S3_hook=S3Hook(aws_conn_id="S3_conn")
        S3_hook.load_file(
            filename=f.name,
            key=f"weather_alexandria/{dt}.csv",
            bucket_name="hi-weather",
            replace=True
        )

with DAG(
    dag_id='weather_airflow_dag',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:
    
    is_api_ready= HttpSensor(
        task_id='is_api_ready',
        http_conn_id='openweather_conn',
        endpoint='/data/2.5/weather?q=Alexandria&appid=f7e1d21eba18e9326d59148f77bafe65'
    )

    weather_data_extract= PythonOperator(
        task_id='weather_data_extract',
        python_callable= extract
    )

    weather_data_transform_load= PythonOperator(
        task_id='weather_data_transform_load',
        python_callable= transform_load
    )

is_api_ready >> weather_data_extract >> weather_data_transform_load