from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein_geheimer_schluessel_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fahrten.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Fahrt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fahrer = db.Column(db.String(100))
    start = db.Column(db.String(100))
    ziel = db.Column(db.String(100))
    datum = db.Column(db.String(20))
    zeit = db.Column(db.String(10))
    preis = db.Column(db.Float)
    plaetze = db.Column(db.Integer)
    telefon = db.Column(db.String(20))
    beschreibung = db.Column(db.Text)

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fahrt_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefon = db.Column(db.String(20))
    plaetze = db.Column(db.Integer)

# --- Datenbank erstellen ---
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    fahrten = Fahrt.query.all()
    return render_template('index.html', fahrten=fahrten)

@app.route('/registrieren', methods=['GET', 'POST'])
def registrieren():
    if request.method == 'POST':
        user = User(
            username=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        flash('Account erstellt!', 'success')
        return redirect(url_for('login'))
    return render_template('registrieren.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Login fehlgeschlagen!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/fahrt-anbieten', methods=['GET', 'POST'])
def fahrt_anbieten():
    if request.method == 'POST':
        fahrt = Fahrt(
            fahrer=request.form['fahrer'],
            start=request.form['start'],
            ziel=request.form['ziel'],
            datum=request.form['datum'],
            zeit=request.form['zeit'],
            preis=float(request.form['preis']),
            plaetze=int(request.form['plaetze']),
            telefon=request.form['telefon'],
            beschreibung=request.form.get('beschreibung', '')
        )
        db.session.add(fahrt)
        db.session.commit()
        flash('Fahrt erfolgreich erstellt!', 'success')
        return redirect(url_for('index'))
    return render_template('fahrt_anbieten.html')

@app.route('/fahrt/<int:fahrt_id>')
def fahrt_details(fahrt_id):
    fahrt = Fahrt.query.get_or_404(fahrt_id)
    return render_template('fahrt_details.html', fahrt=fahrt)

@app.route('/buchen/<int:fahrt_id>', methods=['GET', 'POST'])
def buchen(fahrt_id):
    fahrt = Fahrt.query.get_or_404(fahrt_id)
    if request.method == 'POST':
        plaetze = int(request.form['plaetze'])

fahrt.plaetze -= plaetze
        buchung = Buchung(
            fahrt_id=fahrt_id,
            name=request.form['name'],
            email=request.form['email'],
            telefon=request.form['telefon'],
            plaetze=plaetze
        )
        db.session.add(buchung)
        db.session.commit()
        flash('Buchung erfolgreich!', 'success')
        return redirect(url_for('index'))
    return render_template('buchen.html', fahrt=fahrt)

if __name__ == '__main__':
    app.run(debug=True)
