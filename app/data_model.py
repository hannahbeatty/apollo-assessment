from app.database import db

# use ORM (sql alchemy)
# class = table, objects in class = rows

class Vehicle(db.Model):  # rely on db model
    __tablename__ = "vehicles"  # for the orm

    vin = db.Column(db.String, primary_key=True)  # index by
    manufacturer_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    horse_power = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Numeric, nullable=False)
    fuel_type = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        # make it case insensitive! add everything as upper
        if "vin" in kwargs:
            kwargs["vin"] = kwargs["vin"].upper()
        super().__init__(**kwargs)
    
    def to_dict(self):
        """
        Convert the Vehicle model into a JSON-serializable dictionary.

        Returns:
            dict: Public-facing representation of the vehicle,
                  converting Decimal purchase_price to float.
        """
        return {
            "vin": self.vin,
            "manufacturer_name": self.manufacturer_name,
            "description": self.description,
            "horse_power": self.horse_power,
            "model_name": self.model_name,
            "model_year": self.model_year,
            "purchase_price": float(self.purchase_price),  # make it a float
            "fuel_type": self.fuel_type
        }
