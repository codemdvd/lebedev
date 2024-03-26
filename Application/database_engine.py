from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from models import Wine
import redis


pgpool_ports = [5560, 5570]
port = pgpool_ports[0]
print(f'current pg port:{port}')

employeesDB_url = URL.create(
    'postgresql',
    username='postgres',
    password='qwerty1234',
    host='localhost',
    port=port,
    database='employees'
)

ordersDB_url = URL.create(
    'postgresql',
    username='postgres',
    password='qwerty1234',
    host='localhost',
    port=port,
    database='orders'
)

employees_engine = create_engine(employeesDB_url)
orders_engine = create_engine(ordersDB_url)

employees_session = scoped_session(sessionmaker(bind=employees_engine))
orders_session = scoped_session(sessionmaker(bind=orders_engine))

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

connection.setup(['localhost'], 'wine_catalog', port=9042, protocol_version=3)
sync_table(Wine)
