# Real Estate Estimator



---

## Getting Started

Follow the steps below to set up and run the application.

---

### Prerequisites

1. **Install Docker**  
   Ensure Docker is installed and running on your machine.  
   You can download it from [Docker's official site](https://www.docker.com/).

2. **Download Required Files**  
   Download or place the following files in the specified locations within the project directory:

   - **GeoJSON file for property information**  
     - **File Name:** `Formated_final.json`  
     - **Download Link:** [Formated_final.json](https://drive.google.com/file/d/...)  
     - **Path:** `src/flask_website/static/geojson/Formated_final.json`

   - **City district and mukatat data with area**  
     - **File Name:** `city_district_mukatats_with_area.json`
     - **Download Link:** [city_district_mukatats_with_area.json](https://drive.google.com/file/d/...)  
     - **Path:** `src/flask_website/static/geojson/city_district_mukatats_with_area.json`

   - **Machine learning model for predicting prices**  
     - **File Name:** `final_catboost_property_model_tunedNov5_925.cbm`
     - **Download Link:** [final_catboost_property_model_tunedNov5_925.cbm](https://drive.google.com/file/d/...)  
     - **Path:** `src/flask_website/final_catboost_property_model_tunedNov5_925.cbm`

   - **Environment file**  
     - **File Name:** `.env`  
     - **Instructions to create the file:** See the [Environment Configuration](#environment-configuration) section below.

---

### Environment Configuration

Create a `.env` file in the root project directory with the following structure:

```ini
# Configurations used by the docker-compose file

WEB_PORT=5000
DB_PORT=3306
INIT_FILE=./resources
HOSTNAME=test1
MYSQL_DATABASE=ree
MYSQL_ROOT_PASSWORD=changeme
MYSQL_USER=dbuser1
MYSQL_PASSWORD=changeme
SCHEMA=ree
SECRET_KEY=my_secret_key_here
```
---

### Directory Structure
```
├── src/
│   ├── flask_website/
│   │   ├── static/
│   │   │   ├── geojson/
│   │   │   │   ├── Formated_final.json
│   │   │   │   ├── city_district_mukatats_with_area.json
│   │   ├── final_catboost_property_model_tunedNov5_925.cbm
│   ├── docker-compose.yml
│   ├── .env
```

---

### Setup Instructions

#### Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd <repository_folder>
```


#### Build and Run the Application
Run the following commands to build and start the application:

```bash
Copy codedocker-compose down
docker-compose up --build
```
Or Run start.sh file in bash
```
./start.sh
```
#### Access the Application

Once the application is running, open your web browser and navigate to:
```
http://localhost:5000
```
