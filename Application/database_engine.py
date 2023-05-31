from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Departments, Employees, Clients, OrderTable

employeesDB_url = URL.create(
    'postgresql',
    username='postgres',
    password='qwerty1234',
    host='127.0.0.1',
    database='employees'
)

ordersDB_url = URL.create(
    'postgresql',
    username='postgres',
    password='qwerty1234',
    host='127.0.0.1',
    database='orders'
)

employees_engine = create_engine(employeesDB_url)
orders_engine = create_engine(ordersDB_url)

employees_session = scoped_session(sessionmaker(bind=employees_engine))
orders_session = scoped_session(sessionmaker(bind=orders_engine))