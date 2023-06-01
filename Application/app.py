from flask import Flask, session, redirect, render_template, url_for, request
from functools import wraps
from database_interface import *
import os
from database_engine import employees_session, orders_session, wine_products
from models import Departments, Employees, Clients, OrderTable
## TODO create a separate roads and html documents for client products and admin products

app = Flask(__name__)
app.secret_key = 'qwerty1234'
sessions = {}

def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))

        if not session['admin']:
            return redirect(url_for('products'))

        return f(*args, **kwargs)
    return decorated_function

def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def auth():
     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
          return render_template('login.html')
     if request.method != 'POST': return

     username = request.form['username']
     password = request.form['password']

     result = client_authorize(username, password)

     if not result:
          return render_template('login.html', 
                                 invalid='Incorrect login or password')
     
     session['username'] = username
     session['admin'] = False
     session['logged_in'] = True

     return redirect(url_for('products'))


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
     if request.method == 'GET':
          return render_template('login_admin.html')
     if request.method != 'POST': return

     username = request.form['username']
     password = request.form['password']

     result =  employee_authorize(username, password)

     if not result:
          return render_template('login.html', invalid='Incorrect login or password')
     
     session['username'] = username
     session['admin'] = True
     session['logged_in'] = True

     return redirect(url_for('employees'))

@app.route('/logout')
def logout():
     session.clear()
     return redirect(url_for('products'))


@app.route('/orders')
def orders():
     orders = orders_session.query(OrderTable).all()
     return render_template('wine_orders.html', orders=orders, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/clients')
def clients():
     clients = orders_session.query(Clients).all()
     return render_template('wine_clients.html', clients=clients, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/employees')
def employees():
     employees = employees_session.query(Employees).all()
     print(session.get('logged_in', False))
     return render_template('wine_employees.html', employees=employees, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/products')
def products():
     all_products = wine_products.find()
     return render_template('wine_products.html', products=all_products, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/shopping_cart')
def shopping_cart():
     return render_template('wine_shopping_cart.html', 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

if __name__ == '__main__':
    app.run(debug=True)