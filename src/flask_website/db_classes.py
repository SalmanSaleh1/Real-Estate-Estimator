from db_connection import db

# Create the database table schema for the ree database
class Property(db.Model):
    __tablename__ = 'properties'

    # Fields matching the GeoJSON data structure
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_object = db.Column(db.Integer, unique=True, nullable=False)  # id_object must be unique and not null
    shape_area = db.Column(db.Float, nullable=True)  # Use Float for compatibility with DOUBLE
    owner_name = db.Column(db.String(255), nullable=True)  # Owner's name (nullable)
    parcel_land_use = db.Column(db.String(50), nullable=True)  # Land use type (nullable)
    district_name = db.Column(db.String(100), nullable=True)  # District name (nullable)
    subdiv_name = db.Column(db.String(255), nullable=True)  # Subdivision name (nullable)
    city_name = db.Column(db.String(100), nullable=True)  # City name (nullable)
    muncp_name = db.Column(db.String(100), nullable=True)  # Municipality name (nullable)
    parcel_status = db.Column(db.String(50), nullable=True)  # Parcel status (nullable)
    muncp_id = db.Column(db.Integer, nullable=True)  # Municipality ID (nullable)
    block_no = db.Column(db.String(50), nullable=True)  # Block number (nullable)
    subdiv_no = db.Column(db.String(50), nullable=True)  # Subdivision number (nullable)
    parcel_no = db.Column(db.String(50), nullable=True)  # Parcel number (nullable)
    subdiv_type = db.Column(db.String(50), nullable=True)  # Subdivision type (nullable)
    muncp_desc = db.Column(db.String(255), nullable=True)  # Municipality description (nullable)
    property_type = db.Column(db.String(50), nullable=True)  # Property type (nullable)
    price_per_square_meter = db.Column(db.Numeric(10, 2), nullable=True)  # Price per square meter (nullable)
    area = db.Column(db.String(255), nullable=True)  # Area (nullable)

    def __repr__(self):
        return (f"<Property id={self.id}, id_object={self.id_object}, owner_name='{self.owner_name}', "
                f"city_name='{self.city_name}', parcel_status='{self.parcel_status}', "
                f"property_type='{self.property_type}', price_per_square_meter={self.price_per_square_meter}>")
