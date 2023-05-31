from flask import Flask, session, redirect, render_template, url_for, request
from database_engine import *
app = Flask(__name__)

@app.route('/')
def auth():
     return render_template('auth.html')

@app.route('/home')
def home():
     orders = orders_session.query(OrderTable).all()
     for order in orders:
          print('Address:', order.address)
          print('Order List', order.order_list)
     return render_template('wine_orders.html', orders=orders)

if __name__ == '__main__':
    app.run()