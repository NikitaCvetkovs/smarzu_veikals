from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'shop.db'

def create_database(): #izveido datubāzi
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users ( #izveido lietotāju tabulu
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS perfumes ( #izveido smaržu tabulu
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                volume INTEGER NOT NULL,
                price REAL NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS orders ( #izveido pasūtījumu tabulu
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                perfume_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                order_date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

@app.route('/') #maršruts uz galveno lapu
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST']) #maršruts uz reģistrācijas lapu ar post un get metodēm
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", #pievieno datus tabulai
                 (username, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) #maršruts uz autentifikācijas lapu
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password)) #paņem datus no lietotāju tabulas
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard', user_id=user[0]))
        return "Nepareizs e-pasts vai parole"
    
    return render_template('login.html')

@app.route('/dashboard/<int:user_id>') #maršruts uz smaržu lapu
def dashboard(user_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM perfumes") 
    perfumes = c.fetchall()
    conn.close()
    return render_template('dashboard.html', perfumes=perfumes, user_id=user_id)

@app.route('/add_to_cart', methods=['POST']) #funkcija "Pievienot grozam"
def add_to_cart():
    user_id = session.get('user_id')
    if not user_id:
        return "Nav autorizācijas", 401
    
    perfume_id = request.form['perfume_id']
    perfume_name = request.form['perfume_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, perfume_name, quantity, total_price, order_date) VALUES (?, ?, ?, ?, ?)", #pievieno informāciju pasūtījumu tabulā
             (user_id, perfume_name, quantity, price*quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    return redirect(url_for('cart'))

@app.route('/cart') #maršruts uz grozu
def cart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT perfume_name, quantity, total_price FROM orders WHERE user_id = ?", (user_id,)) #paņem informāciju no pasūtījumu tabulas
    orders = c.fetchall()
    
    total = sum(order[2] for order in orders)
    conn.close()
    
    return render_template('cart.html', orders=orders, total=total, user_id=user_id)

@app.route('/remove_from_cart', methods=['POST']) #funkcija noņemšanai no groza
def remove_from_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    perfume_name = request.form['perfume_name']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE user_id = ? AND perfume_name = ?", #izdzēš informāciju par pasūtījumu no pasūtījuma tabulas 
             (session['user_id'], perfume_name))
    conn.commit()
    conn.close()
    
    return redirect(url_for('cart'))

@app.route('/complete_order', methods=['POST'])  #funkcija pasūtījuma pabeigšanai
def complete_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,)) #paņem informāciju no pasūtījuma tabulas, lai pievienot teksta failam
    orders = c.fetchall()
    
    with open('order_history.txt', 'a', encoding='utf-8') as f:
        for order in orders:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                   f"User:{user_id}, Product:{order[2]}, "
                   f"Qty:{order[3]}, Price:{order[4]}€\n")
    
    c.execute("DELETE FROM orders WHERE user_id = ?", (user_id,)) #izdzēš no pasūtījuma tabulas
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard', user_id=user_id))

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
