# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/doctors')
def doctors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors_data = cur.fetchall()
    cur.close()
    return render_template('doctors.html', doctors=doctors_data)

@app.route('/hospitals')
def hospitals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hospitals")
    hospitals_data = cur.fetchall()
    cur.close()
    return render_template('hospitals.html', hospitals=hospitals_data)

@app.route('/medical_shops')
def medical_shops():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medical_shops")
    shops_data = cur.fetchall()
    cur.close()
    return render_template('medical_shops.html', shops=shops_data)

@app.route('/emergency')
def emergency():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM emergency_services")
    emergencies = cur.fetchall()
    cur.close()
    return render_template('emergency.html', emergencies=emergencies)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form.get('email')

#         cur = mysql.connection.cursor()

#         if email:
#             cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
#             mysql.connection.commit()
#             cur.close()
#             flash("Signup successful. Please log in.")
#             return redirect(url_for('login'))
#         else:
#             cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#             user = cur.fetchone()
#             cur.close()
#             if user:
#                 session['user'] = user[1]
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("Invalid credentials")
#                 return redirect(url_for('login'))

#     return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        cur = mysql.connection.cursor()

        if email:
            # Signup logic
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing = cur.fetchone()
            if existing:
                flash("Username already exists.")
                return redirect(url_for('login'))

            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            mysql.connection.commit()
            flash("Signup successful. Please login.")
            return redirect(url_for('login'))
        else:
            # Login logic
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            cur.close()

            if user:
                session['user'] = user[1]  # username
                session['user_id'] = user[0]  # user id
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials")
                return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please login first.")
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    cur = mysql.connection.cursor()
    cur.execute("SELECT recorded_at FROM health_metrics WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 1", (user_id,))
    last_health = cur.fetchone()
    last_health = last_health[0].strftime('%Y-%m-%d %H:%M') if last_health else None

    cur.execute("SELECT consulted_at FROM virtual_consults WHERE user_id = %s ORDER BY consulted_at DESC LIMIT 1", (user_id,))
    last_consult = cur.fetchone()
    last_consult = last_consult[0].strftime('%Y-%m-%d %H:%M') if last_consult else None

    cur.close()

    return render_template('dashboard.html', last_health=last_health, last_consult=last_consult, username=session['user'])

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (session['user'],))
    user = cur.fetchone()
    field_names = [desc[0] for desc in cur.description]
    user_data = dict(zip(field_names, user))

    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        file = request.files.get('profile_pic')

        filename = user_data.get('profile_pic')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur.execute("""
            UPDATE users SET full_name = %s, phone = %s, profile_pic = %s WHERE username = %s
        """, (full_name, phone, filename, session['user']))
        mysql.connection.commit()
        flash("Profile updated successfully.")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user_data)

@app.route('/virtual_doctor')
def virtual_doctor():
    return render_template('virtual_doctor.html')


# @app.route('/track', methods=['GET', 'POST'])
# def health_tracker():
#     if 'user' not in session:
#         flash("Please log in to access your health tracker.")
#         return redirect(url_for('login'))

#     cur = mysql.connection.cursor()

#     # Get user_id
#     cur.execute("SELECT id FROM users WHERE username = %s", (session['user'],))
#     user = cur.fetchone()
#     user_id = user[0]

#     if request.method == 'POST':
#         weight = request.form['weight']
#         bp = request.form['bp']
#         sugar = request.form['sugar']
#         hr = request.form['hr']

#         cur.execute("""
#             INSERT INTO health_metrics (user_id, weight, blood_pressure, sugar_level, heart_rate)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (user_id, weight, bp, sugar, hr))

#         mysql.connection.commit()
#         flash("Health data added successfully!")

#     # Fetch health history
#     cur.execute("SELECT weight, blood_pressure, sugar_level, heart_rate, recorded_at FROM health_metrics WHERE user_id = %s ORDER BY recorded_at DESC", (user_id,))
#     history = cur.fetchall()
#     cur.close()

#     return render_template('health_tracker.html', history=history)


# @app.route('/tracker')
# def health_tracker():
#     if 'user' not in session:
#         flash("Please login first.")
#         return redirect(url_for('login'))

#     return render_template('tracker.html')


@app.route('/track', methods=['GET', 'POST'])
def health_tracker():
    if 'user' not in session:
        flash("Please log in to access your health tracker.")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Get user_id from session
    cur.execute("SELECT id FROM users WHERE username = %s", (session['user'],))
    user = cur.fetchone()
    user_id = user[0]

    if request.method == 'POST':
        weight = request.form['weight']
        bp = request.form['bp']
        sugar = request.form['sugar']
        hr = request.form['hr']

        cur.execute("""
            INSERT INTO health_metrics (user_id, weight, blood_pressure, sugar_level, heart_rate)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, weight, bp, sugar, hr))

        mysql.connection.commit()
        flash("Health data added successfully!")

    # Fetch health history
    cur.execute("""
        SELECT weight, blood_pressure, sugar_level, heart_rate, recorded_at
        FROM health_metrics
        WHERE user_id = %s
        ORDER BY recorded_at DESC
    """, (user_id,))
    history = cur.fetchall()
    cur.close()

    return render_template('health_tracker.html', history=history)


if __name__ == '__main__':
    app.run(debug=True)
