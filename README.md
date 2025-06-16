# Flask HelpDesk Ticket System

A simple yet functional HelpDesk ticket management system built with Python and Flask.  
This project features user authentication, role-based access (admin and user), ticket creation, status management, and a clean Bootstrap 5-based UI.

---

## Features

- User registration and secure login with password hashing  
- Role-based access control (admin vs regular user)  
- Create, view, edit, and manage support tickets  
- Admin dashboard to view all tickets and update their statuses  
- User dashboard to view personal tickets  
- Responsive and modern UI using Bootstrap 5  
- Flash messages for real-time user feedback  

---

## Technologies Used

- Python 3.x  
- Flask Web Framework  
- Flask-Login for user session management  
- Flask-SQLAlchemy ORM with SQLite database  
- Werkzeug for password hashing  
- Bootstrap 5 for UI styling  

---

## Getting Started

### Prerequisites

- Python 3.x installed on your machine  
- `pip` package manager  

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/user/flask-helpdesk.git
   cd flask-helpdesk

2. (Optional but recommended) Create and activate a virtual environment:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py
 
5. Open your browser and navigate to:
http://localhost:5000

### Default Admin User
If you haven’t created any users yet, you can create an admin user manually in your database or modify the app.py to auto-create the admin user on first run with these credentials:

Username: admin

Password: admin123

(Admin role is defined by the role attribute in the User model.)

### Usage
Register as a new user or login as admin.

Users can create new support tickets and view their own tickets.

Admin can view all tickets and update the status of any ticket.

Use the UI to navigate between dashboards and ticket details.

### Contributing
Contributions are welcome! Feel free to fork the repo and submit pull requests.

### License
This project is licensed under the MIT License.

### Contact
Created by Mauricio Narváez.
mauricionarvilla@gmail.com

Thank you for checking out my HelpDesk project!
Feel free to reach out if you have questions or suggestions.
