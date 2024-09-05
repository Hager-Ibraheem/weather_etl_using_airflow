# Weather Data ETL Pipeline using Apache Airflow on Docker.

## Description
This project runs Apache Airflow on Docker to automate the ETL processes of extracting current weather data for Alexandria from the OpenWeather API, transforming the data, and loading it into an S3 bucket in CSV format. The pipeline runs daily.

### Features
- **Data Extraction**: extracts current weather data by sending a GET request to the OpenWeather API using the API key and city name.
- **Data Transformation**: transforms the weather data by converting temperature units, formatting timestamps, and extracting relevant fields. Saves the transformed data to a temporary CSV file.
- **Data Loading**: loads the CSV file to an S3 bucket using an S3Hook. The file is named using the date and time of data calculation.
- **Automation**: uses Apache Airflow on Docker to automate the ETL processes.
  
### Prerequisites
To run this project, ensure you have the following:
- Docker and Docker Compose.
- AWS Account.

### Setup
To deploy Airflow on Docker:
1. Clone This Repo
   ```bash
   git clone https://github.com/Hager-Ibraheem/weather_etl_project.git
   cd weather_etl_project
   ```
2. Create folders for logs, plugins and config
   ```bash
   mkdir -p ./logs ./plugins ./config
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```
3. Build the Docker image
   ```bash
   docker-compose build
   ```
4. Running Airflow
   ```bash
   docker compose up -d
   ```
5. Accessing the web interface
   The webserver is available at: http://localhost:8080. The default account has the login airflow and the password airflow.

### Configuration
1. **Connections**
   - OpenWeather API Connection: An HTTP connection with the ID openweather_conn must be configured in Airflow UI to check the availability of the OpenWeather API.
     
     ![image](https://github.com/user-attachments/assets/d2f9f15e-9bcf-4c55-adc6-027d57ddebf1)
   - S3 Connection: An AWS S3 connection with the ID S3_conn must be set up in Airflow UI to allow uploading files to the S3 bucket.
     
     ![image](https://github.com/user-attachments/assets/78aa2c32-d9a9-4f70-b5ac-30f26763bac0)
2. **Variables**
   - API Key: Replace the placeholder f7e1d21eba18e9326d59148f77bafe65 with your actual OpenWeather API key.
   - S3 Bucket: Replace hi-weather with your S3 bucket.
