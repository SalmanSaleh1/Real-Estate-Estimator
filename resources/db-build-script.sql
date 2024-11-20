CREATE DATABASE IF NOT EXISTS ree;
USE ree;

CREATE TABLE IF NOT EXISTS properties (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,  -- Primary key with auto-increment
    id_object INT UNIQUE NOT NULL,  -- id_object must be unique and not null
    shape_area DOUBLE NULL,  -- Shape area (nullable)
    owner_name VARCHAR(255) NULL,  -- Owner's name (nullable)
    parcel_land_use VARCHAR(50) NULL,  -- Land use type (nullable)
    district_name VARCHAR(100) NULL,  -- District name (nullable)
    subdiv_name VARCHAR(255) NULL,  -- Subdivision name (nullable)
    city_name VARCHAR(100) NULL,  -- City name (nullable)
    muncp_name VARCHAR(100) NULL,  -- Municipality name (nullable)
    parcel_status VARCHAR(50) NULL,  -- Parcel status (nullable)
    muncp_id INT NULL,  -- Municipality ID (nullable)
    block_no VARCHAR(50) NULL,  -- Block number (nullable)
    subdiv_no VARCHAR(50) NULL,  -- Subdivision number (nullable)
    parcel_no VARCHAR(50) NULL,  -- Parcel number (nullable)
    subdiv_type VARCHAR(50) NULL,  -- Subdivision type (nullable)
    muncp_desc VARCHAR(255) NULL,  -- Municipality description (nullable)
    property_type VARCHAR(50) NULL,  -- Property type (nullable)
    price_per_square_meter DOUBLE NULL,  -- Price per square meter (nullable)
    area VARCHAR(255) NULL  -- Area (nullable)
);
