# 🏔️ Trekking Management System

A full-stack web application for managing trekking activities, staff, trekkers, bookings, and trek operations through a role-based management system.

## ✨ Features

### Admin
- Secure admin login
- Dashboard with trekking statistics
- Create, edit, and delete treks
- Approve Trek Staff registrations
- Assign staff to treks
- View all users, staff, and bookings
- Search and manage users
- Blacklist users or staff
- Manage trek status and availability

### Trek Staff
- Register and log in
- Admin approval required
- View assigned treks
- Update trek details, slots, and status
- View participants of assigned treks
- Mark treks as completed

### Trekkers
- Register and log in
- Browse available treks
- Search and filter treks
- Book treks
- View booking status and history
- Prevent duplicate bookings and overbooking

## 🔐 Role-Based Access

| Role | Permissions |
|------|-------------|
| Admin | Full system management |
| Trek Staff | Manage assigned treks and participants |
| Trekker | Browse and book available treks |

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

### Frontend
- HTML5
- Jinja2
- Bootstrap 5
- CSS

### Database
- SQLite
- SQLAlchemy ORM

## 🏗️ Architecture

```text
User Request
     ↓
Flask Route
     ↓
Controller Logic
     ↓
SQLAlchemy ORM
     ↓
SQLite Database
     ↓
Jinja2 Template
     ↓
HTML Response
```

## 📂 Project Structure

```text
Trekking-Management-System/
│
├── app.py
├── models.py
├── config.py
├── extensions.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── registration.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── users.html
│   ├── treks.html
│   ├── add_trek.html
│   ├── edit_trek.html
│   ├── assign_staff.html
│   ├── participants.html
│   ├── my_bookings.html
│   └── all_bookings.html
│
└── database.db
```

## 🗄️ Database Design

Main entities:

- `User`
- `Trek`
- `Booking`

Relationships:

- **User → Booking:** One-to-Many
- **Trek → Booking:** One-to-Many
- **User ↔ Trek:** Many-to-Many through `Booking`
- **Staff → Trek:** One-to-Many

`Booking` acts as the association/junction table between users and treks.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd Trekking-Management-System
```

### 2. Create a virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:5001
```

## 🗃️ Database Initialization

The SQLite database is created programmatically using SQLAlchemy:

```python
with app.app_context():
    db.create_all()
```

## 🔄 Booking Flow

```text
User Login
    ↓
View Open Treks
    ↓
Select Trek
    ↓
Check Available Slots
    ↓
Check Trek Status
    ↓
Check Duplicate Booking
    ↓
Create Booking
    ↓
Decrease Available Slots
```

The application prevents:
- Booking closed treks
- Booking when no slots are available
- Duplicate bookings

## 🔒 Authentication & Security

- Flask-Login for authentication and sessions
- Werkzeug password hashing
- Role-based authorization
- Admin approval for staff
- User/staff blacklisting
- Server-side validation

## 🧩 Key Concepts

- Flask routing
- GET and POST requests
- Jinja2 templating
- SQLAlchemy ORM
- Foreign keys and relationships
- CRUD operations
- Authentication and authorization
- Sessions
- Form handling
- Flash messages
- Search and filtering

## 🎥 Demo

[Watch the Demo Video](https://drive.google.com/file/d/1ddD2ZgHT78xr3LY78HFrHtOTjRMzdpBc/view?usp=drivesdk)

## 🤖 AI / LLM Usage

AI/LLM tools were used during development as a learning and development aid for understanding concepts, debugging, reviewing implementation logic, and preparing documentation.

The developer understands the implemented functionality and can explain the application's architecture, database design, routes, and core logic.

## 📌 Future Improvements

- REST API endpoints
- Email notifications
- Trek images and galleries
- Online payment integration
- Advanced analytics
- Automated booking cancellation
- Production deployment

## 👨‍💻 Author

**Vivek Sarathe**

Computer Science & AI Student

## 📄 License

This project is intended for educational and demonstration purposes.
