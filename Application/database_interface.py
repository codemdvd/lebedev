from database_engine import employees_session, orders_session, wine_products, carts
from models import Departments, Employees, Clients, OrderTable
from bson.objectid import ObjectId
from sqlalchemy import func
import os

# Get all instances methods
def get_all_orders():
    return orders_session.query(OrderTable).all()

def get_all_clients():
    return orders_session.query(Clients).all()

def get_all_employees():
    return employees_session.query(Employees).all()

def get_all_products():
    return wine_products.find()

# Auth methods
def employee_authorize(username: str, password: str):
    if not (isinstance(username, str) and isinstance(password, str)):
        raise TypeError('Both arguments should be str')

    auth_result = employees_session.query(func.public.auth_employee_correct(username, password)).first()[0]
    if auth_result is None:
        return False
    return auth_result

def client_authorize(username: str, password: str):
    if not (isinstance(username, str) and isinstance(password, str)):
        raise TypeError('Both arguments should be str')

    auth_result = orders_session.query(func.public.auth_client_correct(username, password)).first()[0]
    if auth_result is None:
        return False
    return auth_result

def client_register(
    first_name: str,
    second_name: str,
    phone_number: str,
    email: str,
    login: str,
    password: str
):
    try:
        client = Clients(
            first_name=first_name,
            second_name=second_name,
            log=login,
            password=password,
            phone_number=phone_number,
            email=email
        )

        orders_session.add(client)
        orders_session.commit()
        return 0
    except Exception as e:
        print(e.with_traceback())
        return 1


# Client methods
def get_my_orders(username: str):
    orders = orders_session.query(OrderTable).join(Clients).where(Clients.log == username).all()
    return orders

def get_order_info(username: str, order_id: int):
    if username:
        order = orders_session.query(OrderTable).join(Clients)\
            .where(Clients.log == username and OrderTable.order_id == order_id).first()
    else:
        order = order = orders_session.query(OrderTable).join(Clients)\
            .where(OrderTable.order_id == order_id).first()
        
    return order

def get_product_info(product_id: str):
    product = wine_products.find_one({'article': product_id})
    return product

def search_wines(search_text: str):
    wines = wine_products.find({"$text": {"$search": search_text}})
    return wines

def add_product_to_cart(username: str, article: str, amount: int = 1):
    wine_id = ObjectId(wine_products.find_one({'article': article})['_id'])
    cart = carts.find_one({'client_username': username})['cart_list']

    if wine_id not in [p['wine'] for p in cart]:
        cart.append({'wine': wine_id, 'amount': amount})
        print(cart)
        carts.update_one({'client_username': username}, {'$set': {'cart_list': cart}})
        return
    
    cart = [{'wine': wine_id, 'amount': amount} if p['wine'] == wine_id else p for p in cart]
    carts.update_one({'client_username': username}, {'$set': {'cart_list': cart}})


def create_emply_cart(username: str):
    carts.insert_one({'client_username': username, 'cart_list': []})

def get_user_cart(username: str):
    cart_list = carts.find_one({'client_username': username})
    if cart_list == None: return None

    cart = {}
    for c in cart_list['cart_list']:
        wine = wine_products.find_one({'_id': c['wine']})
        cart[wine['article']] = c['amount']
    return cart if cart else None