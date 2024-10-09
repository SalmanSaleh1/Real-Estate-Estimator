from db_connection import db

# Create the database table schema for the ree database
class Property(db.Model):
    __tablename__ = 'properties'

    # Fields matching the GeoJSON data structure
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    type = db.Column(db.String(20), nullable=False)  # Type of the geometry (e.g., Polygon)
    coordinates = db.Column(db.JSON, nullable=False)  # Store coordinates in JSON format
    shape_area = db.Column(db.Numeric(10, 3), nullable=False)  # Shape area (numeric)
    owner_name = db.Column(db.String(255), nullable=False)  # Owner's name
    parcel_land_use = db.Column(db.String(50), nullable=False)  # Land use type
    district_name = db.Column(db.String(100), nullable=False)  # District name
    subdiv_name = db.Column(db.String(255), nullable=False)  # Subdivision name
    city_name = db.Column(db.String(100), nullable=False)  # City name
    muncp_name = db.Column(db.String(100), nullable=False)  # Municipality name
    parcel_status = db.Column(db.String(50), nullable=False)  # Parcel status
    muncp_id = db.Column(db.Integer, nullable=False)  # Municipality ID
    block_no = db.Column(db.String(50), nullable=True)  # Block number
    subdiv_no = db.Column(db.String(50), nullable=False)  # Subdivision number
    parcel_no = db.Column(db.String(50), nullable=False)  # Parcel number
    notes = db.Column(db.Text, nullable=True)  # Notes (optional)
    construction_type = db.Column(db.String(50), nullable=True)  # Construction type (optional)
    split_type = db.Column(db.String(10), nullable=True)  # Split type (optional)
    subdiv_type = db.Column(db.String(50), nullable=True)  # Subdivision type
    muncp_desc = db.Column(db.String(255), nullable=False)  # Municipality description

    def __repr__(self):
        return f"<Property {self.id}, {self.owner_name}>"
