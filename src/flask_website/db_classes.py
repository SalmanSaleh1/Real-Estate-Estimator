from db_connection import db

# Create the database table schema for the ree database
class Property(db.Model):
    __tablename__ = 'properties'

    # Fields matching the GeoJSON data structure
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_object = db.Column(db.Integer, unique=True, nullable=False)  # id_object must be unique and not null
    coordinates = db.Column(db.JSON, nullable=True)  # Coordinates (nullable)
    shape_area = db.Column(db.Numeric(10, 3), nullable=True)  # Shape area (nullable)
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
    notes = db.Column(db.Text, nullable=True)  # Notes (nullable)
    construction_type = db.Column(db.String(50), nullable=True)  # Construction type (nullable)
    split_type = db.Column(db.String(10), nullable=True)  # Split type (nullable)
    subdiv_type = db.Column(db.String(50), nullable=True)  # Subdivision type (nullable)
    muncp_desc = db.Column(db.String(255), nullable=True)  # Municipality description (nullable)

    def __repr__(self):
        return f"<Property {self.id}, {self.owner_name}>"
