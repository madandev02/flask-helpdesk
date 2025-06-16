from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

# ───── APP Y CONFIGURACIÓN ─────
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ───── MODELOS ─────
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(50), default='user')  # 'user' o 'admin'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Abierto')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='tickets')  # ← RELACIÓN INVERSA

# ───── MIDDLEWARE DE ADMIN ─────
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Acceso denegado. Solo para administradores.")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ───── LOGIN MANAGER ─────
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ───── RUTAS PRINCIPALES ─────
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Usuario ya existe')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Usuario creado. Ahora inicia sesión.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ───── DASHBOARD USUARIO ─────
@app.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tickets=tickets)

@app.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        ticket = Ticket(title=title, description=description, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_ticket.html')

@app.route('/ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id and current_user.role != 'admin':
        flash("No tienes permiso para ver este ticket.")
        return redirect(url_for('dashboard'))
    return render_template('view_ticket.html', ticket=ticket)

@app.route('/ticket/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        flash("No tienes permiso para editar este ticket.")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        ticket.title = request.form['title']
        ticket.description = request.form['description']
        ticket.status = request.form['status']
        db.session.commit()
        flash("Ticket actualizado.")
        return redirect(url_for('dashboard'))
    return render_template('edit_ticket.html', ticket=ticket)

@app.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        flash("No tienes permiso para eliminar este ticket.")
        return redirect(url_for('dashboard'))

    db.session.delete(ticket)
    db.session.commit()
    flash("Ticket eliminado.")
    return redirect(url_for('dashboard'))

# ───── DASHBOARD ADMIN ─────
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    tickets = Ticket.query.all()
    return render_template('admin_dashboard.html', tickets=tickets)

# ───── INICIALIZACIÓN ─────
if __name__ == '__main__':
    if not os.path.exists('db.sqlite3'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
