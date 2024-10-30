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
        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
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
        geojson_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'static/geojson/TestPrint1.json')
        )

        # Load the GeoJSON data
        with open(geojson_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # Get the Property class dynamically from the database mapping
        Property = self.base.classes.properties

        with self.app.app_context():
            success_count = 0
            failure_count = 0
            batch_size = 100

            for idx, feature in enumerate(geojson_data['features']):
                try:
                    geometry = feature['geometry']
                    properties = feature['properties']

                    # Data Cleaning: Handle potential issues with missing or malformed fields
                    shape_area = properties.get('SHAPE.AREA')
                    shape_area = float(shape_area.replace(',', '')) if shape_area else None
                    
                    coordinates = json.dumps(geometry.get('coordinates')) if geometry else None
                    muncp_id = properties.get('MUNCP_ID')
                    muncp_id = int(muncp_id) if muncp_id else None

                    # Create a new `Property` instance with the cleaned fields
                    new_property = Property(
                        coordinates=coordinates,
                        shape_area=shape_area,
                        owner_name=properties.get('OWNERNAME'),
                        parcel_land_use=properties.get('PARCEL_LANDUSE'),
                        district_name=properties.get('DISTRICT_NAME_D'),
                        subdiv_name=properties.get('SUBDIV_NAME'),
                        city_name=properties.get('CITY_NAME'),
                        muncp_name=properties.get('MUNCP_NAME'),
                        parcel_status=properties.get('PARCEL_STATUS'),
                        muncp_id=muncp_id,
                        block_no=properties.get('BLOCK_NO'),
                        subdiv_no=properties.get('SUBDIV_NO'),
                        parcel_no=properties.get('PARCEL_NO'),
                        notes=properties.get('NOTES') or None,
                        construction_type=properties.get('CONSTRUCTION_TYPE') or None,
                        split_type=properties.get('SPLIT_TYPE') or None,
                        subdiv_type=properties.get('SUBDIV_TYPE') or None,
                        muncp_desc=properties.get('MUNCP_DESC'),
                        id_object=properties['OBJECTID']  # OBJECTID is assumed mandatory
                    )

                    # Add the property to the session
                    self.db.session.add(new_property)
                    success_count += 1

                    # Commit in batches
                    if (idx + 1) % batch_size == 0:
                        self.db.session.commit()

                except Exception as e:
                    print(f"Error processing feature ID {feature['id']}: {e}")
                    failure_count += 1

            # Final commit for any remaining features
            self.db.session.commit()

            # Print results for verification
            print(f"Successfully inserted {success_count} properties.")
            print(f"Failed to insert {failure_count} properties.")

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

if __name__ == '__main__':
    unittest.main()
