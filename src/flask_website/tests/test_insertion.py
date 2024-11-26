import unittest
import json
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import requests

# Configuration for the database (can be imported from a config file)
HOSTNAME = os.environ.get('HOSTNAME', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 3306)
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ree')
MYSQL_USER = os.environ.get('MYSQL_USER', 'dbuser')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'changeme')

class TestInsertion(unittest.TestCase):
    def setUp(self):
        """Set up the Flask app for testing"""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOSTNAME}:{DB_PORT}/{MYSQL_DATABASE}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.db = SQLAlchemy(self.app)

        # Automap base preparation
        self.base = automap_base()

        with self.app.app_context():
            self.base.prepare(autoload_with=self.db.engine)

    def test_insert_properties_from_geojson(self):
        """Test inserting data from a GeoJSON file into the properties table"""
        geojson_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../static/geojson/property_info.json')
        )

        # Load the GeoJSON data
        with open(geojson_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # Get the Property class dynamically from the database mapping
        Property = self.base.classes.properties

        with self.app.app_context():
            success_count = 0
            failure_count = 0
            batch_size = 1000  # Adjust as needed for performance

            # Extract features
            features = geojson_data['features']
            total_features = len(features)
            logging.info(f"Total features to process: {total_features}")

            # Process records in batches
            for i in range(0, total_features, batch_size):
                batch = features[i:i + batch_size]
                insert_data = []

                for feature in batch:
                    try:
                        # Extract and clean data from GeoJSON properties
                        properties = feature['properties']

                        price_per_sqm_raw = properties.get('price_per_square_meter')
                        price_per_sqm = float(price_per_sqm_raw) if price_per_sqm_raw else None

                        shape_area_raw = properties.get('shape_area')
                        shape_area = float(shape_area_raw.replace(',', '')) if shape_area_raw else None

                        muncp_id = int(properties.get('muncp_id')) if properties.get('muncp_id') else None

                        # Prepare data for bulk insertion
                        insert_data.append({
                            'shape_area': shape_area,
                            'owner_name': properties.get('owner_name'),
                            'parcel_land_use': properties.get('parcel_land_use'),
                            'district_name': properties.get('district_name'),
                            'subdiv_name': properties.get('subdiv_name'),
                            'city_name': properties.get('city_name'),
                            'muncp_name': properties.get('muncp_name'),
                            'parcel_status': properties.get('parcel_status'),
                            'muncp_id': muncp_id,
                            'block_no': properties.get('block_no'),
                            'subdiv_no': properties.get('subdiv_no'),
                            'parcel_no': properties.get('parcel_no'),
                            'subdiv_type': properties.get('subdiv_type') or None,
                            'muncp_desc': properties.get('muncp_desc'),
                            'id_object': properties.get('id_object'),
                            'property_type': properties.get('property_type'),
                            'price_per_square_meter': price_per_sqm,
                            'area': properties.get('area')
                        })
                        success_count += 1

                    except Exception as e:
                        logging.error(f"Error processing feature ID {feature.get('id')}: {e}")
                        failure_count += 1

                # Commit the batch
                try:
                    self.db.session.bulk_insert_mappings(Property, insert_data)
                    self.db.session.commit()
                    logging.info(f"Batch {i // batch_size + 1} committed successfully.")
                except SQLAlchemyError as e:
                    logging.error(f"Failed to insert batch {i // batch_size + 1}: {e}")
                    self.db.session.rollback()
                    # Reduce success count for failed batch
                    success_count -= len(insert_data)

            logging.info(f"Successfully inserted {success_count} properties.")
            logging.info(f"Failed to insert {failure_count} properties.")
            logging.info(f"Total properties processed: {success_count + failure_count}")

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            self.db.session.remove()

if __name__ == '__main__':
    unittest.main()
