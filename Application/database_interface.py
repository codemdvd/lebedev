from database_engine import employees_session, orders_session, wine_products
from models import Departments, Employees, Clients, OrderTable
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

def search_wine(string: str, limit: int):
    wines = wine_products.find({'$text': {'$search': string}}).limit(limit)
    return wines

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