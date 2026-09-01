from flask import Flask,render_template,request,redirect,url_for,flash
from config import Config
from extensions import db, login_manager
from models import User, Trek, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime,date
from sqlalchemy import or_

app = Flask(__name__) 
# "Flask(__name__) creates the Flask application
#  object. __name__ tells Flask where the application
#  module is located, so Flask can find resources like 
# templates and static files."

app.config.from_object(Config)
# "app.config.from_object(Config)
#  loads the application settings from the Config class into 
# the Flask app, such as the database URI and secret key."


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# db.init_app(app) → connects SQLAlchemy with the Flask application.
# login_manager.init_app(app) → connects Flask-Login with the Flask application.
# login_manager.login_view = "login" → tells Flask-Login to redirect unauthenticated users to the login route.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# "@login_manager.user_loader tells Flask-Login 
# how to load a user from the user ID stored in the session.
#  load_user() queries the database and returns the corresponding User object."





with app.app_context():
    db.create_all()
# "app.app_context() provides the Flask application context,
#  and db.create_all() creates all tables defined in the 
# SQLAlchemy models if they do not already exist."

# Check blacklisted users before every request
@app.before_request
def check_blacklisted_user():
    if current_user.is_authenticated and current_user.blacklisted:
        logout_user()
        flash("Your account has been blacklisted.")
        return redirect(url_for("login"))


@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))

# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method == "GET"):
        return render_template("registration.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            # Email already exist
            flash("Email already exists.")
            return redirect(url_for("register")) 
    
        # Create new user
        hashed_password = generate_password_hash(password)

        approved = (role == "USER")

        user = User(
            name = name,
            email = email, 
            password = hashed_password, 
            phone = phone, 
            role = role, 
            approved = approved
        )

        db.session.add(user)

        db.session.commit()

        if(role == "USER"):
            login_user(user)
            return redirect(url_for("dashboard"))
            
    
        flash("Registration successful! Please wait for admin approval.")
        return redirect(url_for("login"))

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if(existing_user):

            if(check_password_hash(existing_user.password,password )):
                if existing_user.blacklisted:
                    flash("Your account has been blacklisted.")
                    return redirect(url_for("login"))
                
                if(existing_user.approved):
                    login_user(existing_user)
                    return redirect(url_for("dashboard"))
                else:
                    flash("Not approved by admin")
                    return redirect(url_for("login"))
            else:
                flash("Incorrect password")
                return redirect(url_for("login"))

        else:
            flash("User not found")
            return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():

    if current_user.role == "ADMIN":

        total_treks = Trek.query.count()
        total_users = User.query.filter_by(role="USER").count()
        total_staff = User.query.filter_by(role="STAFF").count()
        total_bookings = Booking.query.count()

        return render_template(
            "dashboard.html",
            total_treks=total_treks,
            total_users=total_users,
            total_staff=total_staff,
            total_bookings=total_bookings
        )

    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("login"))

@app.route("/create-admin")
def create_admin():
    user = User(
                name = "admin",
                email = "admin@gmail.com", 
                password = generate_password_hash("password"), 
                phone = "1111111111", 
                role = "ADMIN", 
                approved = True
            )
    
    db.session.add(user)
    
    db.session.commit()

    return "Admin created successfully"


@app.route("/admin")
@login_required
def admin():
    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))
    
    
    pending_staff = User.query.filter_by(role = "STAFF",approved= False).all()


    return render_template(
        "admin.html",
        pending_staff=pending_staff,
    )

@app.route("/users")
@login_required
def users():
    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    users = User.query.filter(User.role != "ADMIN").all()

    return render_template(
        "users.html",
        users=users
    )

@app.route("/approve/<int:user_id>")
@login_required
def approve_staff(user_id):
    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    user = User.query.filter_by(user_id = user_id).first()
    if user:
        user.approved = True
        db.session.commit()
        flash("Staff approved successfully.")
    else:
        flash("User not found.")

    return redirect(url_for("admin"))

@app.route("/blacklist/<int:user_id>")
@login_required
def blacklist_user(user_id):

    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))
    
    user = User.query.filter_by(user_id = user_id).first()
    if user:
        user.blacklisted = True
        db.session.commit()
        flash("User blacklisted successfully.")
    else:
        flash("User not found")
    return redirect(url_for("users"))


@app.route("/add-trek", methods=["GET", "POST"])
@login_required
def add_trek():
    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    
    if(request.method =="GET"):
        return render_template("add_trek.html")
    else:
        trek_name = request.form["trek_name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        total_slots = request.form["total_slots"]
        trek_price = request.form["trek_price"]

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        total_slots = int(total_slots)

        trek = Trek(
            staff_id=None,
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            description=description,
            start_date=start_date,
            end_date=end_date,
            total_slots=total_slots,
            available_slots=total_slots,
            trek_price = trek_price,
            status="Pending"
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek added successfully.")
        return redirect(url_for("dashboard"))

@app.route("/treks")
@login_required
def treks():

    search = request.args.get("search")

    # Base Query according to role
    if current_user.role == "ADMIN":

        query = Trek.query

    elif current_user.role == "STAFF":

        query = Trek.query.filter_by(
            staff_id=current_user.user_id
        )

    else:   # USER

        query = Trek.query.filter_by(
            status="Open"
        )


    if search:

        query = query.filter(

            or_(
                Trek.trek_name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%"),
                Trek.difficulty.ilike(f"%{search}%")
            )

        )

    treks = query.all()

    booked_treks = []

    if current_user.role == "USER":

        booked_treks = [
            booking.trek_id
            for booking in Booking.query.filter_by(
                user_id=current_user.user_id
            ).all()
        ]

    return render_template(
        "treks.html",
        treks=treks,
        booked_treks = booked_treks
    )

@app.route("/edit-trek/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    if current_user.role not in ["STAFF", "ADMIN"]:
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    trek = Trek.query.filter_by(trek_id=trek_id).first()

    if not trek:
        flash("Trek not found.")
        return redirect(url_for("treks"))

    if current_user.role == "STAFF" and trek.staff_id != current_user.user_id:
        flash("You can only manage your own treks.")
        return redirect(url_for("treks"))
        
    if(request.method == "GET"):
       return render_template(
        "edit_trek.html",
        trek=trek
    )
    else:
        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.description = request.form["description"]
        trek.status = request.form["status"]
        trek.price = request.form['Price']

        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        total_slots = int(request.form["total_slots"])

        trek.start_date = start_date
        trek.end_date = end_date

        booked_count = Booking.query.filter_by(
            trek_id=trek.trek_id,
            status="Booked"
        ).count()

        trek.total_slots = total_slots
        trek.available_slots = max(0, total_slots - booked_count)

        db.session.commit()
        flash("Trek updated successfully.")

        return redirect(url_for("treks"))


    
@app.route("/delete-trek/<int:trek_id>", methods=["GET"])
@login_required
def delete_trek(trek_id):

    if current_user.role not in ["STAFF", "ADMIN"]:
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    trek = Trek.query.filter_by(trek_id=trek_id).first()

    if not trek:
        flash("Trek not found.")
        return redirect(url_for("treks"))

    if current_user.role == "STAFF" and trek.staff_id != current_user.user_id:
        flash("You can only manage your own treks.")
        return redirect(url_for("treks"))
    
    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully.")
    return redirect(url_for("treks"))

@app.route("/book-trek/<int:trek_id>",methods = ["GET"])
@login_required
def book_trek(trek_id):

    if current_user.role not in ["USER"]:
        flash("Only User can book")
        return redirect(url_for("dashboard"))

    trek = Trek.query.filter_by(trek_id=trek_id).first()
    
    if not trek:
        flash("Trek not found.")
        return redirect(url_for("treks"))

    if trek.status != "Open":
        flash("This trek is not open for booking.")
        return redirect(url_for("treks"))
    
    if(trek.available_slots > 0):
        existing_booking = Booking.query.filter_by(
            user_id=current_user.user_id,
            trek_id=trek.trek_id
        ).first()

        if existing_booking:
            flash("You have already booked this trek.")
            return redirect(url_for("treks"))

        booking = Booking(
        user_id=current_user.user_id,
        trek_id=trek.trek_id,
        booking_date=date.today(),
        status="Booked"
        )

        trek.available_slots -= 1

        db.session.add(booking)
        db.session.commit()

        flash("Booking successful.")
        return redirect(url_for("treks"))
    else:
        flash("No slots available.")
        return redirect(url_for("treks"))


@app.route("/my-bookings")
@login_required
def my_bookings():

    if current_user.role != "USER":
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    bookings = Booking.query.filter_by(
    user_id=current_user.user_id
    ).all()

    return render_template(
    "my_bookings.html",
    bookings=bookings
    )       
@app.route("/all-bookings")
@login_required
def all_bookings():
    if(current_user.role != "ADMIN"):
        flash("Access denied.")
        return redirect(url_for("dashboard"))
    
    bookings = Booking.query.all()

    return render_template(
        "all_bookings.html",
        bookings = bookings
    )

@app.route("/assign-staff/<int:trek_id>", methods=["GET", "POST"])
@login_required
def assign_staff(trek_id):
    if current_user.role != "ADMIN":
        flash("Access denied.")
        return redirect(url_for("dashboard"))

    trek = Trek.query.filter_by(trek_id=trek_id).first()

    if not trek:
        flash("Trek not found.")
        return redirect(url_for("treks"))


    staff = User.query.filter_by(
    role="STAFF",
    approved=True
    ).all()

    if request.method == "GET":
        return render_template(
            "assign_staff.html",
            trek=trek,
            staff=staff
    )
    
    else:
        staff_id = request.form["staff_id"]
        trek.staff_id = int(staff_id)

        db.session.commit()

        flash("Staff assigned successfully.")

        return redirect(url_for("treks"))

# route for participants
@app.route("/participants/<int:trek_id>")
@login_required
def participants(trek_id):

    if current_user.role == "USER":
        flash("Access denied")
        return redirect(url_for('dashboard'))

    trek = Trek.query.filter_by(trek_id=trek_id).first()

    if not trek:
        flash("Trek not found.")
        return redirect(url_for("treks"))

    if current_user.role == "STAFF" and trek.staff_id != current_user.user_id:
        flash("Access denied.")
        return redirect(url_for("treks"))

    bookings = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    return render_template(
        "participants.html",
        trek=trek,
        bookings=bookings
    )







if __name__ == "__main__":
    app.run(debug=True,port = 5001)