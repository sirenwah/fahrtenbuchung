import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///fahrten.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

ADMIN_PASSWORD = 'admin123'

@app.route('/admin')
def admin():
    if session.get('admin_logged_in') != True:
        return render_template('admin_login.html')
    
    users = User.query.all()
    fahrten = Fahrt.query.all()
    buchungen = Buchung.query.all()
    
    return render_template('admin_dashboard.html', users=users, fahrten=fahrten, buchungen=buchungen)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        flash('Falsches Passwort!', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin'))

@app.route('/admin/fahrt-loeschen/<int:fahrt_id>')
def admin_fahrt_loeschen(fahrt_id):
    if session.get('admin_logged_in') != True:
        return redirect(url_for('admin'))
    
    fahrt = Fahrt.query.get_or_404(fahrt_id)
    db.session.delete(fahrt)
    db.session.commit()
    flash('Fahrt gelöscht!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/buchung-loeschen/<int:buchung_id>')
def admin_buchung_loeschen(buchung_id):
    if session.get('admin_logged_in') != True:
        return redirect(url_for('admin'))
    
    buchung = Buchung.query.get_or_404(buchung_id)
    db.session.delete(buchung)
    db.session.commit()
    flash('Buchung gelöscht!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
