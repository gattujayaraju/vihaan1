from flask import Flask, render_template, request, redirect
import pymysql
from datetime import date

app = Flask(__name__)

# ---------------- MySQL Connection ----------------
conn = pymysql.connect(
    host="localhost",
    user="root",          # change if your username is different
    password="Raju@2002", # your MySQL password
    database="vds"        # ensure this database exists
)
cursor = conn.cursor()

# ---------------- Home Page ----------------
@app.route('/')
def home():
    return render_template('index.html')  # opens your main page first

# ---------------- Dashboard Page ----------------
@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM collections ORDER BY date DESC")
    data = cursor.fetchall()
    cursor.execute("SELECT SUM(amount) FROM collections")
    total = cursor.fetchone()[0] or 0
    return render_template('dashboard.html', collections=data, total=total)

# ---------------- Add Collection ----------------
@app.route('/add', methods=['POST'])
def add_collection():
    amount = request.form['amount']
    desc = request.form['description']
    today = date.today()

    cursor.execute(
        "INSERT INTO collections (date, description, amount) VALUES (%s, %s, %s)",
        (today, desc, amount)
    )
    conn.commit()
    return redirect('/dashboard')  # redirect back to dashboard

# ---------------- Delete Collection ----------------
@app.route('/delete/<int:id>')
def delete_collection(id):
    cursor.execute("DELETE FROM collections WHERE id=%s", (id,))
    conn.commit()
    return redirect('/dashboard')

# ---------------- Services Page ----------------
@app.route('/services')
def services():
    return render_template('services.html')

# ---------------- Contact Page ----------------
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------------- Products Page ----------------
@app.route('/products')
def products():
    return render_template('products.html')

# ---------------- Main Entry ----------------
if __name__ == "__main__":
    app.run(debug=True)
