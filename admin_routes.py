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
    return redirect(url_for('index'))

@app.route('/admin/fahrt-loeschen/<int:fahrt_id>')
def admin_fahrt_loeschen(fahrt_id):
    if session.get('admin_logged_in') != True:
        return redirect(url_for('index'))
    fahrt = Fahrt.query.get_or_404(fahrt_id)
    db.session.delete(fahrt)
    db.session.commit()
    flash('Fahrt geloescht!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/buchung-loeschen/<int:buchung_id>')
def admin_buchung_loeschen(buchung_id):
    if session.get('admin_logged_in') != True:
        return redirect(url_for('index'))
    buchung = Buchung.query.get_or_404(buchung_id)
    db.session.delete(buchung)
    db.session.commit()
    flash('Buchung geloescht!', 'success')
    return redirect(url_for('admin'))
