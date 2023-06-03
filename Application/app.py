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
     session.clear()
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
     session['cart'] = get_user_cart(username)

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

     return redirect(url_for('manage_employees'))

@app.route('/register', methods=['GET', 'POST'])
def register():
     if request.method == 'GET':
          return render_template('register.html')
     if request.method != 'POST': return

     first_name = request.form['first_name']
     second_name = request.form['second_name']
     phone_number = request.form['phone_number']
     email = request.form['email']
     username = request.form['username']
     password = request.form['password']

     result = client_register(first_name, second_name, phone_number, 
                     email, username, password)
     
     if result:
          return render_template('register.html')
     
     session['username'] = username
     session['admin'] = False
     session['logged_in'] = True
     return redirect(url_for('products'))


@app.route('/logout')
def logout():
     session.clear()
     return redirect(url_for('products'))


@app.route('/orders')
def orders():
     if not session.get('username', False):
          return redirect(url_for('login'))
     
     orders = get_my_orders(session['username'])
     total_prices = [sum([(p['price']) * p['amount'] for p in order.order_list.values()]) for order in orders]
     return render_template('wine_orders.html', orders=zip(orders, total_prices), 
                            logged_in=True,
                            username=session.get('username', None),
                            total_prices=total_prices)

@app.route('/order_info')
@requires_auth
def order_info():
     args = request.args
     if not args.get('order_id', default=False):
          return redirect(url_for('products'))
     
     if session['admin'] == True:
          order = get_order_info(None, args.get('order_id'))
          products = [get_product_info(p) for p in order.order_list]
          total_price = sum([(p['price']) * p['amount'] for p in order.order_list.values()])
          return render_template('manage_order.html', order=order, products=products, total_price=total_price)
     
     order = get_order_info(session['username'], args.get('order_id'))
     products = [get_product_info(p) for p in order.order_list]
     total_price = sum([(p['price']) * p['amount'] for p in order.order_list.values()])
     return render_template('order.html', order=order, products=products, total_price=total_price)


@app.route('/products', methods=['GET', 'POST'])
def products():
     all_products = None
     if session.get('cart') == None:
          session['cart'] = {}
          if session.get('logged_in'):
               create_emply_cart(session['username'])

     if request.args.get("article"):
          article = request.args.get("article")
          cart = session['cart']
          if cart.get(article) == None:
               cart[article] = 0
          cart[article] += 1

          if session.get('logged_in'):
               add_product_to_cart(session['username'], article, cart[article])
          session['cart'] = cart

     if request.form.get('search'):
          all_products = search_wines(request.form['search'])
     else:
          all_products = get_all_products()
          
     return render_template('wine_products.html', products=all_products, 
                         logged_in=session.get('logged_in', False),
                         username=session.get('username', None), session=session)


@app.route('/shopping_cart')
def shopping_cart():
     cart_products = []
     articles = session['cart'].keys()
     amounts = session['cart'].values()
     for article in articles:
          cart_products.append(wine_products.find_one({'article': article}))
     return render_template('wine_shopping_cart.html', 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None), cart_products=zip(cart_products, amounts))

@app.route('/manage_clients')
@requires_admin
def manage_clients():
     clients = orders_session.query(Clients).all()
     return render_template('manage_wine_clients.html', clients=clients,
                            username=session.get('username', None))

@app.route('/manage_orders')
def manage_orders():
     if not session.get('username', False):
          return redirect(url_for('login'))
     orders = orders_session.query(OrderTable).all()
     return render_template('manage_wine_orders.html', orders=orders, 
                            logged_in=session.get('logged_in', False),
                            username=session.get('username', None))

@app.route('/manage_employees')
@requires_admin
def manage_employees():
     employees = employees_session.query(Employees).all()
     print(session.get('logged_in', False))
     return render_template('manage_wine_employees.html', employees=employees,
                            username=session.get('username', None))

@app.route('/manage_products')
@requires_admin
def manage_products():
     all_products = wine_products.find()
     return render_template('manage_wine_products.html', products=all_products,
                            username=session.get('username', None))


@app.route('/new_product', methods=('GET', 'POST'))
@requires_admin
def new_product():
     if request.method=='POST':
          article = request.form['article']
          name = request.form['name']
          type = request.form['type']
          country = request.form['country']
          region = request.form['region']
          vintage_dating = int(request.form['vintage_dating'])
          winery = request.form['winery']
          alcohol = request.form['alcohol']
          capacity = request.form['capacity']
          description = request.form['description']
          price = request.form['price']
          items_left = int(request.form['items_left'])

          wine_products.insert_one(
               {
                    'article': article,
                    'name': name,
                    'type': type,
                    'country': country,
                    'region': region,
                    'vintage_dating': vintage_dating,
                    'winery': winery,
                    'alcohol': float(alcohol),
                    'capacity': float(capacity),
                    'description': description,
                    'price': float(price),
                    'items_left': items_left
               }
          )
     return render_template('manage_wine_new_product.html',
                            username=session.get('username', None))

@app.route('/new_employee', methods=('GET', 'POST'))
@requires_admin
def new_employee():
     if request.method=='POST':
          emp_id = request.form['emp_id']
          first_name = request.form['first_name']
          second_name = request.form['second_name']
          emp_login = request.form['emp_login']
          emp_pass = request.form['emp_pass']
          emp_phone = request.form['emp_phone']
          emp_email = request.form['emp_email']
          dept_no = request.form['dept_no']

          employee = Employees(
                              emp_id=emp_id, 
                              first_name=first_name, 
                              second_name=second_name,
                              emp_login=emp_login,
                              emp_pass=emp_pass,
                              emp_phone=emp_phone,
                              emp_email=emp_email,
                              dept_no=dept_no
                               )
          employees_session.add(employee)
          employees_session.commit()

     return render_template('manage_wine_new_employee.html',
                            username=session.get('username', None))


if __name__ == '__main__':
    app.run(debug=True)