from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from models import Wine
import redis

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

redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

connection.setup(['127.0.0.1'], "wine_catalog", port=9042, protocol_version=3)
sync_table(Wine)
# client = MongoClient('mongos', 27017, username='admin', password='qwerty1234')
# db = client.products
# wine_products = db.wine
# carts = db.cart