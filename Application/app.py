from flask import Flask, session, redirect, render_template, url_for, request
from database_engine import *
from models import *

app = Flask(__name__)

@app.route('/')
def auth():
     return render_template('auth.html')

@app.route('/orders')
def orders():
     orders = orders_session.query(OrderTable).all()
     return render_template('wine_orders.html', orders=orders)

@app.route('/clients')
def clients():
     clients = orders_session.query(Clients).all()
     return render_template('wine_clients.html', clients=clients)

@app.route('/employees')
def employees():
     employees = employees_session.query(Employees).all()
     return render_template('wine_employees.html', employees=employees)

@app.route('/products')
def products():
     all_products = wine_products.find()
     return render_template('wine_products.html', products=all_products)

@app.route('/shopping_cart')
def shopping_cart():
     return render_template('wine_shopping_cart.html')

if __name__ == '__main__':
    app.run()