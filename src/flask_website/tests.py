import unittest
import json
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import requests

# Configuration for the database
HOSTNAME = os.environ.get('HOSTNAME', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 3306)
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ree')
MYSQL_USER = os.environ.get('MYSQL_USER', 'dbuser')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'changeme')
BASE_URL = 'http://127.0.0.1:5000/api'  # Adjust if running on a different server

logging.basicConfig(level=logging.INFO)

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
            os.path.join(os.path.dirname(__file__), 'static/geojson/property_info.json')
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

class BackendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Shared setup for all tests"""
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOSTNAME}:{DB_PORT}/{MYSQL_DATABASE}'

        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.db = SQLAlchemy(cls.app)

        # Automap base preparation
        cls.base = automap_base()

        with cls.app.app_context():
            cls.base.prepare(autoload_with=cls.db.engine)

            # Define the example property as a class attribute
            cls.example_property = {
                'id_object': 1,
                'shape_area': 868.977,
                'owner_name': None,
                'parcel_land_use': 'سكني تجاري',
                'district_name': 'السلام الغربي',
                'subdiv_name': 'تخطيط لأرض المواطن عبد الله العيدان',
                'city_name': 'بريده',
                'muncp_name': 'بلدية الديرة',
                'parcel_status': 'فضاء',
                'muncp_id': 1,
                'block_no': '',
                'subdiv_no': 'ق/904',
                'parcel_no': '86',
                'subdiv_type': 'خاص',
                'muncp_desc': 'بلدية الديرة',
                'property_type': 'أرض',
                'price_per_square_meter': 150.0,
                'area': 'منطقة القصيم'
            }

            # Insert the example property if it doesn't exist
            Property = cls.base.classes.properties
            existing_property = cls.db.session.query(Property).filter_by(id_object=cls.example_property['id_object']).first()
            if not existing_property:
                cls.db.session.execute(Property.__table__.insert(), [cls.example_property])
                cls.db.session.commit()

            # Save the ID for use in tests
            cls.test_property_id = cls.example_property['id_object']

    def test_1_database_connection(self):
        """Test database connection and query"""
        try:
            with self.app.app_context():
                Property = self.base.classes.properties
                logging.info(f"Mapped columns: {[col.key for col in Property.__table__.columns]}")
                result = self.db.session.query(Property).limit(1).all()
                self.assertIsNotNone(result, "Database query returned no results")
                logging.info("Database connection and query successful.")
        except SQLAlchemyError as e:
            self.fail(f"Database connection or query failed: {e}")

    def test_2_add_property(self):
        """Test adding the example property"""
        with self.app.app_context():
            Property = self.base.classes.properties

            try:
                # Clean up any existing test property
                existing_property = self.db.session.query(Property).filter_by(id_object=self.example_property['id_object']).first()
                if existing_property:
                    self.db.session.delete(existing_property)
                    self.db.session.commit()

                # Insert the example property
                self.db.session.execute(Property.__table__.insert(), [self.example_property])
                self.db.session.commit()

                # Verify the record was added
                added_property = self.db.session.query(Property).filter_by(id_object=self.example_property['id_object']).first()
                self.assertIsNotNone(added_property, "Failed to add property to the database")
                logging.info(f"Property added successfully with ID: {self.example_property['id_object']}")
            except SQLAlchemyError as e:
                self.db.session.rollback()
                self.fail(f"Add property test failed: {e}")

    def test_3_property_details(self):
        """Test property details route using the added property"""
        with self.app.app_context():
            Property = self.base.classes.properties

            # Fetch the property from the database
            property_in_db = self.db.session.query(Property).filter_by(id_object=self.example_property['id_object']).first()
            if not property_in_db:
                self.fail("No property available for details test")

            self.test_property_id = property_in_db.id_object
            logging.info(f"test_3_property_details: test_property_id = {self.test_property_id}")

            # Call the property details route
            try:
                response = requests.get(f"http://127.0.0.1:5000/property/{self.test_property_id}")
                self.assertEqual(response.status_code, 200, f"Property details route did not return status 200. Got: {response.status_code}")
                self.assertIn("Property Details", response.text, "Property details page missing expected title")
                self.assertIn("Parcel No", response.text, "Property details page missing 'Parcel No'")
                self.assertIn("Estimated Price", response.text, "Property details page missing 'Estimated Price'")
                logging.info("Property details route test successful.")
            except Exception as e:
                self.fail(f"Property details route test failed: {e}")

    def test_4_api_endpoint_prediction(self):
        """Test the API prediction endpoint using the added property"""
        if not self.example_property:
            self.skipTest("No property available for prediction test")

        payload = {
            "area": self.example_property['area'],
            "city": self.example_property['city_name'],
            "district": self.example_property['district_name'],
            "Mukatat": self.example_property['subdiv_no'],
            "property_classification": self.example_property['parcel_land_use'],
            "property_type": self.example_property['property_type'],
            "space": self.example_property['shape_area']
        }

        try:
            response = requests.post(f"{BASE_URL}/estimate_price", json=payload)
            self.assertEqual(response.status_code, 200, "API response status code is not 200")
            data = response.json()
            self.assertIn("predicted_price", data, "Predicted price not found in API response")
            logging.info(f"API prediction test successful. Predicted price: {data['predicted_price']}")
        except Exception as e:
            self.fail(f"API prediction test failed: {e}")

    def test_5_delete_property(self):
        """Test deleting the added property"""
        if not self.example_property:
            self.skipTest("No property available for deletion test")

        with self.app.app_context():
            Property = self.base.classes.properties

            try:
                # Find the property
                property_to_delete = self.db.session.query(Property).filter_by(id_object=self.example_property['id_object']).first()
                self.assertIsNotNone(property_to_delete, "Property not found for deletion")

                # Delete the property
                self.db.session.delete(property_to_delete)
                self.db.session.commit()

                # Verify the record was deleted
                deleted_property = self.db.session.query(Property).filter_by(id_object=self.example_property['id_object']).first()
                self.assertIsNone(deleted_property, "Failed to delete property from the database")
                logging.info("Property deleted successfully.")
            except SQLAlchemyError as e:
                self.db.session.rollback()
                self.fail(f"Delete property test failed: {e}")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        with cls.app.app_context():
            cls.db.session.remove()

if __name__ == '__main__':
    unittest.main()