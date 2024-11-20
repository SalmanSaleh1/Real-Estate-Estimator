# Real Estate Estimator

## Overview
This project provides a **machine learning-driven solution** for estimating real estate prices tailored to the Saudi Arabian market. It incorporates **Geographic Information System (GIS)** integration and advanced algorithms to enhance the accuracy and transparency of property valuations.

### Key Features
- **Accurate Price Estimation:** Uses historical transaction data and real-time economic indicators.
- **GIS Integration:** Visualizes property data spatially for better context and decision-making.
- **Interactive Web Application:** Built using Flask with a user-friendly interface.
- **Scalable Design:** Enables future feature expansion and extensibility.


---

## Getting Started

Follow the steps below to set up and run the application.

---

# Project Setup Instructions

## 1. Install Docker
Ensure Docker is installed and running on your machine.  
You can download it from [Docker's official site](https://www.docker.com/).

## 2. Download Required Files
Download or place the following files in the specified locations within the project directory:

- **GeoJSON file for property information**  
  - **File Name:** `property_info.json`  
  - **Download Link:** [property_info.json](https://drive.google.com/file/d/1P8Jz38rqcvRTIWVhsulRwEYPMhmLBLLW/view?usp=sharing)  
  - **Path:** `src/flask_website/static/geojson/property_info.json`

- **Machine learning model for predicting prices**  
  - **File Name:** `catboost_model.cbm`  
  - **Download Link:** [catboost_model.cbm](https://drive.google.com/file/d/1myz3mPqhwMA8huZfYJAZlnzpqlqgxp9p/view?usp=sharing)  
  - **Path:** `src/flask_website/catboost_model.cbm`

- **Environment file**  
  - **File Name:** `.env`  
  - **Instructions to create the file:** See the [Environment Configuration](#environment-configuration) section below.

## 3. Add Google Maps API Key
You need to configure the Google Maps API key for the project by updating the following files:

- **File 1:** `\flask_website\templates\home.html`  
  - **Line Number:** 141  
  - **Instruction:** Replace the placeholder key with your Google Maps API key in the `<gmpx-api-loader>` tag.  
  - Example:  
    ```html
    <!-- Google Maps API Loader -->
    <gmpx-api-loader key="YOUR_GOOGLE_MAPS_API_KEY" solution-channel="GMP_GE_mapsandplacesautocomplete_v1"></gmpx-api-loader>
    ```

- **File 2:** `\flask_website\static\js\map.js`  
  - **Line Number:** 19  
  - **Instruction:** Update the map ID key and configure map options.  
  - Example:  
    ```javascript
    // Set map options (e.g., disable map type control, set Map ID)
    map.innerMap.setOptions({
        mapTypeControl: false,
        mapId: 'YOUR_MAP_ID' // Add your Map ID here
    });
    ```

- **Documentation for Google Maps API:**  
  - Visit the [Google Maps API Documentation](https://developers.google.com/maps/documentation/javascript/get-api-key) for detailed instructions on obtaining and managing your API key.

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

## Objectives

- Enhance transparency in property transactions.
- Enable efficient and informed decision-making for buyers and sellers.
- Provide a scalable and intuitive tool for real estate price estimation.

## Team Members

- **Yazeed Asim Alramadi**
- **Salman Saleh Alkhalifah**
- **Mohammed Ali Aldubayyan**
- **Abdulrrahman Alowaymir**

### Supervisor

- **Dr. Ziyad Alsaeed**

## Acknowledgments

This project was developed as part of the **Information Technology** curriculum at **Qassim University**.