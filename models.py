from extensions import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable = False )
    email = db.Column(db.String(100), nullable = False, unique = True )
    password = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    approved = db.Column(db.Boolean, nullable = False, default = False)
    blacklisted = db.Column(db.Boolean, nullable = False, default = False)

    def get_id(self):
        return str(self.user_id)
    
class Trek(db.Model):
    trek_id = db.Column(db.Integer, primary_key =True)
    staff_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    staff = db.relationship("User")
    trek_name = db.Column(db.String(100) , nullable = False)
    location = db.Column(db.String(100), nullable = False)
    difficulty = db.Column(db.String(20), nullable = False)
    description = db.Column(db.Text, nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    total_slots = db.Column(db.Integer, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False)
    trek_price = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String ,nullable = True, default = "Pending")

class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User")
    trek_id = db.Column(db.Integer, db.ForeignKey("trek.trek_id"))
    trek = db.relationship("Trek")
    booking_date = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, nullable = False , default = "Booked")


