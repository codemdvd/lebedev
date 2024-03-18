from flask import Flask, session, jsonify, request
from functools import wraps
from database_interface import *
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SUPERSECRETKEY') or 'qwerty1234'
sessions = {}


def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401

        if not session['admin']:
            return jsonify({'status': 'error', 'message': 'Admin privileges required'}), 403

        return f(*args, **kwargs)

    return decorated_function


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = client_authorize(username, password)
        if not result:
            return jsonify({'status': 'error', 'message': 'Incorrect login or password'}), 401
        session['username'] = username
        session['admin'] = False
        session['logged_in'] = True
        session['cart'] = get_user_cart(username)
        return jsonify({'status': 'success', 'message': 'Login successful'})
    # For GET request, indicate that only POST is allowed
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        result = employee_authorize(username, password)

        if not result:
            # Instead of rendering a template, return a JSON response indicating login failure
            return jsonify({'status': 'error', 'message': 'Incorrect login or password'}), 401

        session['username'] = username
        session['admin'] = True
        session['logged_in'] = True

        # Instead of redirecting, return a JSON response indicating successful admin login
        return jsonify({'status': 'success', 'message': 'Admin login successful'})

    # If the request method is GET or any method other than POST, inform the user about the allowed method
    return jsonify({'status': 'error', 'message': 'Method not allowed. Use POST for login.'}), 405


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        result = client_register(first_name, second_name, phone_number,
                                 email, username, password)

        if result != 0:
            return jsonify({'status': 'error', 'message': 'Registration failed'}), 400
        return jsonify({'status': 'success', 'message': 'Registration successful'}), 201
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})


@app.route('/orders')
def orders():
    if not session.get('username', False):
        return jsonify({'status': 'error', 'message': 'Authentication required'}), 401

    orders = get_my_orders(session['username'])
    total_prices = [sum([(p['price']) * p['amount'] for p in order.order_list.values()]) for order in orders]
    orders_data = [{'order': order.to_dict(), 'total_price': price} for order, price in zip(orders, total_prices)]
    return jsonify({'status': 'success', 'orders': orders_data})


@app.route('/order_info')
@requires_auth
def order_info():
    args = request.args
    if not args.get('order_id', default=False):
        return jsonify({'status': 'error', 'message': 'Order ID required'}), 400

    # Assuming get_order_info and get_product_info functions are modified to return dictionaries
    if session['admin']:
        order = get_order_info(None, args['order_id'])
    else:
        order = get_order_info(session['username'], args['order_id'])

    products = [get_product_info(p).to_dict() for p in order.order_list]
    total_price = sum([(p['price']) * p['amount'] for p in order.order_list.values()])
    return jsonify({'status': 'success', 'order': order.to_dict(), 'products': products, 'total_price': total_price})


@app.route('/products', methods=['GET', 'POST'])
def products():
    if session.get('cart') is None:
        session['cart'] = {}

    if request.method == 'GET':
        if request.args.get("article"):
            article = request.args.get("article")
            cart = session['cart']
            cart[article] = cart.get(article, 0) + 1
            if session.get('logged_in'):
                add_product_to_cart(session['username'], article, cart[article])
            session['cart'] = cart
            return jsonify({'status': 'success', 'message': f'Added article {article} to cart'})

        all_products = get_all_products()
        return jsonify({'status': 'success', 'products': [p.to_dict() for p in all_products]})

    elif request.method == 'POST':
        search_query = request.form.get('search')
        if search_query:
            all_products = search_wines(search_query)
            return jsonify({'status': 'success', 'products': [p.to_dict() for p in all_products]})
        else:
            return jsonify({'status': 'error', 'message': 'Search query not provided'}), 400


# TODO fix order_list filling
@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'GET':
        cart_products = []
        for article, amount in session.get('cart', {}).items():
            product_info = get_product_info(article)
            cart_products.append({'product': product_info.to_dict(), 'amount': amount})
        return jsonify({'status': 'success', 'cart_products': cart_products})

    elif request.method == 'POST':
        cart = session.get('cart', {})
        order_list = {p: {'price': get_product_info(p).to_dict()['price'], 'amount': amount} for p, amount in
                      cart.items()}
        address = request.form.get('address')
        creation_date = datetime.now().date()
        payment_date = datetime.now().date()
        paid = True

        create_order(session['username'], address, creation_date, payment_date, paid, order_list)
        clear_cart(session['username'])
        session['cart'] = {}
        return jsonify({'status': 'success', 'message': 'Order placed successfully'})


@app.route('/manage_clients')
@requires_admin
def manage_clients():
    clients = get_all_clients()
    return jsonify({'status': 'success', 'clients': [c.to_dict() for c in clients]})


@app.route('/manage_orders')
def manage_orders():
    if not session.get('username', False):
        return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
    orders = get_all_orders()
    return jsonify({'status': 'success', 'orders': [o.to_dict() for o in orders]})


@app.route('/manage_employees')
@requires_admin
def manage_employees():
    employees = get_all_employees()
    return jsonify({'status': 'success', 'employees': [e.to_dict() for e in employees]})


@app.route('/manage_products')
@requires_admin
def manage_products():
    all_products = get_all_products()
    return jsonify({'status': 'success', 'products': [p.to_dict() for p in all_products]})


@app.route('/new_product', methods=('GET', 'POST'))
@requires_admin
def new_product():
    if request.method == 'POST':
        # Extract the product data from the form
        article = request.form.get('article')
        name = request.form.get('name')
        type = request.form.get('type')
        country = request.form.get('country')
        region = request.form.get('region')
        vintage_dating = request.form.get('vintage_dating')
        winery = request.form.get('winery')
        alcohol = request.form.get('alcohol')
        capacity = request.form.get('capacity')
        description = request.form.get('description')
        price = request.form.get('price')
        items_left = request.form.get('items_left')

        # Assuming validation and adding product to database
        success = add_product(article, name, type, country, region, vintage_dating,
                              winery, alcohol, capacity, description, price, items_left)
        if success == 0:
            return jsonify({'status': 'success', 'message': 'Product added successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to add product'}), 400

    # For GET request or other methods, indicate that only POST is allowed
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405


@app.route('/new_employee', methods=('GET', 'POST'))
@requires_admin
def new_employee_api():
    if request.method == 'POST':
        # Extract the employee data from the form
        emp_id = request.form.get('emp_id')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        emp_login = request.form.get('emp_login')
        emp_pass = request.form.get('emp_pass')
        emp_phone = request.form.get('emp_phone')
        emp_email = request.form.get('emp_email')
        dept_no = request.form.get('dept_no')

        # Assuming validation and adding employee to database
        success = add_employee(emp_id, first_name, second_name, emp_login, emp_pass,
                               emp_phone, emp_email, dept_no)
        if success == 0:
            return jsonify({'status': 'success', 'message': 'Employee added successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to add employee'}), 400

    # For GET request or other methods, indicate that only POST is allowed
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
