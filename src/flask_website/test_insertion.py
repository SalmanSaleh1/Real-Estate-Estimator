import unittest
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

# Import db_connection directly since the script is now in the same module
from db_connection import db  # Correct import after moving the test script

# Configuration for the database
HOSTNAME = os.environ.get('HOSTNAME', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 3306)
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ree')
MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD', 'changeme')
MYSQL_USER = os.environ.get('MYSQL_USER', 'dbuser')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'changeme')
SCHEMA = os.environ.get('SCHEMA', 'ree')

class TestInsertion(unittest.TestCase):
    def setUp(self):
        """Set up the Flask app for testing"""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] =\
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOSTNAME}:{DB_PORT}/{SCHEMA}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.db = SQLAlchemy(self.app)

        # Automap base preparation
        self.base = automap_base()

        with self.app.app_context():
            self.base.prepare(autoload_with=self.db.engine)
            self.db.create_all()

    def test_insert_properties_from_geojson(self):
        """Test inserting data from a GeoJSON file into the properties table"""
        geojson_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static/geojson/TestPrint1.json'))

        with open(geojson_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # Assuming you have a mapped class for 'properties'
        Property = self.base.classes.properties

        # Ensure the test runs within the application context
        with self.app.app_context():
            batch_size = 100  # Set batch size for commits
            success_count = 0  # Counter for successful rows
            failure_count = 0  # Counter for failed rows

            for idx, feature in enumerate(geojson_data['features']):
                try:
                    geometry = feature['geometry']
                    properties = feature['properties']

                    # Replace missing values with None (for null-like values in JSON)
                    shape_area = properties.get('SHAPE.AREA', None)
                    if isinstance(shape_area, str):
                        shape_area = shape_area.replace(',', '')  # Clean up commas if it's a string

                    coordinates = geometry.get('coordinates') if geometry else None  # Ensure coordinates are not missing
                    if coordinates and isinstance(coordinates[0], list):
                        coordinates = json.dumps(coordinates)  # Convert coordinates to JSON string for storage

                    # Handle 'muncp_id' as an integer or None if empty
                    muncp_id = properties.get('MUNCP_ID', None)
                    if muncp_id == '':
                        muncp_id = None  # If muncp_id is empty string, set it to None

                    # Extract other fields
                    owner_name = properties.get('OWNERNAME', None)
                    parcel_land_use = properties.get('PARCEL_LANDUSE', None)
                    district_name = properties.get('DISTRICT_NAME_D', None)
                    subdiv_name = properties.get('SUBDIV_NAME', None)
                    city_name = properties.get('CITY_NAME', None)
                    muncp_name = properties.get('MUNCP_NAME', None)
                    parcel_status = properties.get('PARCEL_STATUS', None)
                    block_no = properties.get('BLOCK_NO', None)
                    subdiv_no = properties.get('SUBDIV_NO', None)
                    parcel_no = properties.get('PARCEL_NO', None)
                    notes = properties.get('NOTES', None)
                    construction_type = properties.get('CONSTRUCTION_TYPE', None)
                    split_type = properties.get('SPLIT_TYPE', None)
                    subdiv_type = properties.get('SUBDIV_TYPE', None)
                    muncp_desc = properties.get('MUNCP_DESC', None)
                    id_object = properties.get('OBJECTID', None)

                    # Ensure id_object is present, since it's the only non-nullable field
                    if id_object is None:
                        print(f"Skipping row {idx + 1}: Missing OBJECTID")
                        failure_count += 1
                        continue

                    # Create a new property entry from GeoJSON data
                    new_property = Property(
                        coordinates=coordinates,  # Store as a proper JSON object or None
                        shape_area=shape_area,  # Updated shape_area
                        owner_name=owner_name,
                        parcel_land_use=parcel_land_use,
                        district_name=district_name,
                        subdiv_name=subdiv_name,
                        city_name=city_name,
                        muncp_name=muncp_name,
                        parcel_status=parcel_status,
                        muncp_id=muncp_id,  # Ensure this is either a valid integer or None
                        block_no=block_no,
                        subdiv_no=subdiv_no,
                        parcel_no=parcel_no,
                        notes=notes,
                        construction_type=construction_type,
                        split_type=split_type,
                        subdiv_type=subdiv_type,
                        muncp_desc=muncp_desc,
                        id_object=id_object
                    )

                    # Add the property to the session
                    self.db.session.add(new_property)
                    success_count += 1

                    # Commit in batches
                    if (idx + 1) % batch_size == 0:
                        self.db.session.flush()  # Flush before committing to avoid memory overload
                        self.db.session.commit()

                except Exception as e:
                    # Log and skip any row that causes an error
                    print(f"Error processing row {idx + 1}: {e}")
                    failure_count += 1
                    continue

            # Final commit for remaining rows after the loop
            self.db.session.commit()

            # Output success and failure counts for verification
            print(f"Successfully inserted {success_count} rows.")
            print(f"Failed to insert {failure_count} rows.")

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

if __name__ == '__main__':
    unittest.main()
