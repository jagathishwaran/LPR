from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'Admin@098'  # Change this to a secure key

# Filepath to the CSV data
CSV_FILE = os.path.join('data', 'vehicle_data.csv')

# Dummy user credentials (you can store them securely)
users = {
    'admin': 'password123'
}

# Helper function to read the CSV file
def read_data():
    return pd.read_csv(CSV_FILE)

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = read_data()
    total_entries = df['Vehicle Number'].count()
    registered = df[df['Is Registered'] == True]
    unregistered = df[df['Is Registered'] == False]
    return render_template('dashboard.html', total_entries=total_entries, registered=len(registered), unregistered=len(unregistered))

# Route for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        df = read_data()
        result = df[df['Vehicle Number'] == vehicle_number]
        return render_template('search.html', result=result.to_dict(orient='records'))
    return render_template('search.html', result=None)

# Route for unregistered vehicles
@app.route('/unregistered')
def unregistered():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = read_data()
    unregistered = df[df['Is Registered'] == False]
    return render_template('unregistered.html', unregistered=unregistered.to_dict(orient='records'))

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
