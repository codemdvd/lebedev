from database_engine import employees_session, orders_session, redis_client as r
from models import Employees, Clients, OrderTable
from sqlalchemy import func
from datetime import date
from models import Wine


# Get all instances methods
def get_all_orders():
    return orders_session.query(OrderTable).all()


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
    return orders[::-1]


def get_order_info(username: str, order_id: int):
    if username:
        order = orders_session.query(OrderTable).join(Clients)\
            .where(Clients.log == username and OrderTable.order_id == order_id).first()
    else:
        order = order = orders_session.query(OrderTable).join(Clients)\
            .where(OrderTable.order_id == order_id).first()
        
    return order


def get_product_info(article: str):
    try:
        product = Wine.objects(article=article).get()
        return product
    except Wine.DoesNotExist:
        return None


def search_wines(search_text: str):
    wines = Wine.objects.filter(name__icontains=search_text).allow_filtering()
    return list(wines)


def add_product_to_cart(username: str, article: str, amount: int = 1):
    cart_key = f"cart:{username}"
    item_key = f"item:{article}"  
    existing_item = r.hget(cart_key, item_key)
    if existing_item:
        item_amount = int(existing_item)
        item_amount += amount
    else:
        item_amount = amount
    r.hset(cart_key, item_key, item_amount)
    print(f"Product {article} updated/added to {username}'s cart with amount {item_amount}.")


def get_user_cart(username: str):
    cart_key = f"cart:{username}"
    cart_items = r.hgetall(cart_key)
    if not cart_items:
        print("Cart not found")
        return None
    cart = {}
    for item_key, amount in cart_items.items():
        article = item_key.split(":")[1]
        cart[article] = int(amount)
    print("Cart found")
    return cart if cart else None


def clear_cart(username: str):
    cart_key = f"cart:{username}"
    r.delete(cart_key)
    print(f"Cart for {username} has been cleared.")


def create_order(
    username: str,
    address: str,
    creation_date: date,
    payment_date: date,
    paid: bool,
    order_list: dict
):
    client_id = orders_session.query(Clients).where(Clients.log == username).first().client_id
    order = OrderTable(
        address = address,
        creation_date = creation_date,
        payment_date = payment_date,
        paid = paid,
        order_list = order_list,
        client_id = client_id
    )
    orders_session.add(order)
    orders_session.commit()


# Admin methods
def get_all_clients():
    return orders_session.query(Clients).all()


def get_all_employees():
    return employees_session.query(Employees).all()


def get_all_products():
    try:
        products = Wine.objects.all()
        return list(products)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def add_product(
    article: str,
    name: str,
    type: str,
    country: str,
    region: str,
    vintage_dating: int,
    winery: str,
    alcohol: float,
    capacity: float,
    description: str,
    price: float,
    items_left: int
):
    try:
        Wine.create(
            article=article,
            name=name,
            type=type,
            country=country,
            region=region,
            vintage_dating=vintage_dating,
            winery=winery,
            alcohol=alcohol,
            capacity=capacity,
            description=description,
            price=price,
            items_left=items_left
        )
        return 0
    except:
        return 1


def add_employee(
        emp_id, 
        first_name, 
        second_name,
        emp_login,
        emp_pass,
        emp_phone,
        emp_email,
        dept_no
):
    try:
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
        return 0
    except Exception as e:
        print(e.with_traceback())
        return 1
