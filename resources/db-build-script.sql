CREATE DATABASE IF NOT EXISTS ree;
USE ree;

CREATE TABLE IF NOT EXISTS properties (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,  -- Primary key with auto-increment
    id_object INT UNIQUE,  -- New column: id_object (unique and nullable)
    coordinates JSON,  -- Coordinates field (nullable)
    shape_area DOUBLE,  -- Shape area (nullable)
    owner_name VARCHAR(255),  -- Owner's name (nullable)
    parcel_land_use VARCHAR(50),  -- Land use type (nullable)
    district_name VARCHAR(100),  -- District name (nullable)
    subdiv_name VARCHAR(255),  -- Subdivision name (nullable)
    city_name VARCHAR(100),  -- City name (nullable)
    muncp_name VARCHAR(100),  -- Municipality name (nullable)
    parcel_status VARCHAR(50),  -- Parcel status (nullable)
    muncp_id INT,  -- Municipality ID (nullable)
    block_no VARCHAR(50),  -- Block number (nullable)
    subdiv_no VARCHAR(50),  -- Subdivision number (nullable)
    parcel_no VARCHAR(50),  -- Parcel number (nullable)
    notes TEXT,  -- Notes (nullable)
    construction_type VARCHAR(50),  -- Construction type (nullable)
    split_type VARCHAR(10),  -- Split type (nullable)
    subdiv_type VARCHAR(50),  -- Subdivision type (nullable)
    muncp_desc VARCHAR(255)  -- Municipality description (nullable)
);
