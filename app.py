import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein_geheimer_schluessel_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fahrtenbuch_postgres_sql_user:vNEGTiMcWrpbY0BoUBctYhfZQXikv680@dpg-d66t91esb7us73bkdm70-a/fahrtenbuch_postgres_sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
