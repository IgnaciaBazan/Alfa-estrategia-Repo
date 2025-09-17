from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
import bcrypt
from functools import wraps
from flask import redirect, url_for



pwd = b"clave123"       # aquí defines la contraseña real
hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
print(hashed)  # imprime el hash para copiar y pegar en la base de datos



app = Flask(__name__)

# app.py


# ===== Config =====
app.config['SECRET_KEY'] = '123456789'  # Necesaria para WTForms/CSRF y sesiones
app.config['WTF_CSRF_ENABLED'] = True

# MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'           # <-- ajusta
app.config['MYSQL_PASSWORD'] = 'ruta'       # <-- ajusta
app.config['MYSQL_DB'] = 'colegio2_bd'  # <-- ajusta
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ===== Formularios =====
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

# ===== Helper: login_required =====
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ===== Rutas =====
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, password, is_active FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if not user:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('login.html', form=form)

        if not user['is_active']:
            flash('Usuario deshabilitado. Contacta al administrador.', 'danger')
            return render_template('login.html', form=form)

        # password es VARBINARY, traerá bytes; asegúrate del tipo:
        hashed = user['password']
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed):
            # Guardar sesión mínima
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            flash('¡Bienvenido/a, {}!'.format(user['name']), 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():  # (si tu función se llama Dashboard, mantén el nombre idéntico)
    return render_template('dashboard.html', name=session.get('user_name'))

@app.route('/plan/liderazgo')
@login_required
def plan_liderazgo():
    return render_template('section.html', title='Liderazgo')

@app.route('/plan/gestion-pedagogica')
@login_required
def plan_gestion_pedagogica():
    return render_template('section.html', title='Gestión Pedagógica')

@app.route('/plan/convivencia-escolar')
@login_required
def plan_convivencia_escolar():
    return render_template('section.html', title='Convivencia Escolar')

@app.route('/plan/gestion-recursos')
@login_required
def plan_gestion_recursos():
    return render_template('section.html', title='Gestión de Recursos')

@app.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Opcional: desactivar cualquier registro


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Escucha en todas las interfaces de red
        port=5000,       # Puerto (puedes cambiarlo, por ejemplo 8080)
        debug=True       # Solo para desarrollo, no en producción
    )
