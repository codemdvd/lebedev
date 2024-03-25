from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from sqlalchemy import Column
from sqlalchemy import String, Integer, Date, Boolean, JSON, Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Departments(Base):
    __tablename__ = 'departments'
    dept_no = Column('dept_no', String(4), primary_key=True)
    dept_name = Column('dept_name', String(40))

    def to_dict(self):
        return {
            'dept_no': self.dept_no, 
            'dept_name': self.dept_name
            }


class Employees(Base):
    __tablename__ = 'employees'
    emp_id = Column('emp_id', Integer, Sequence('emp_id_seq'), primary_key=True)
    first_name = Column('first_name', String(30))
    second_name = Column('second_name', String(30))
    emp_login = Column('emp_login', String(30))
    emp_pass = Column('emp_pass', String(50))
    emp_phone = Column('emp_phone', String(30))
    emp_email = Column('emp_email', String(40))
    dept_no = Column('dept_no', String(4), ForeignKey('departments.dept_no'))

    def to_dict(self):
        return {
            'emp_id': self.emp_id, 
            'first_name': self.first_name, 
            'second_name': self.second_name,
            'emp_login': self.emp_login, 
            'emp_phone': self.emp_phone,
            'emp_email': self.emp_email, 
            'dept_no': self.dept_no
        }


class Clients(Base):
    __tablename__ = 'clients'
    client_id = Column('client_id', Integer, Sequence('client_id_seq'), primary_key=True)
    first_name = Column('first_name', String(30))
    second_name = Column('second_name', String(30))
    log = Column('client_login', String(30))
    password = Column('client_password', String(50))
    phone_number = Column('phone_number', String(17))
    email = Column('email', String(40))

    def to_dict(self):
        return {
            'client_id': self.client_id, 
            'first_name': self.first_name, 
            'second_name': self.second_name,
            'log': self.log, 
            'phone_number': self.phone_number, 
            'email': self.email
        }


class OrderTable(Base):
    __tablename__ = 'order_table'
    order_id = Column('order_id', Integer, Sequence('order_id_seq'), primary_key=True)
    address = Column('address', String(70))
    creation_date = Column('creation_date', Date)
    payment_date = Column('payment_date', Date)
    paid = Column('paid', Boolean)
    order_list = Column('order_list', JSON)
    client_id = Column('client_id', Integer, ForeignKey('clients.client_id'))
    
    def to_dict(self):
        return {
            'order_id': self.order_id, 'address': self.address, 'creation_date': str(self.creation_date),
            'payment_date': str(self.payment_date), 'paid': self.paid, 'order_list': self.order_list,
            'client_id': self.client_id
        }


class Wine(Model):
    __keyspace__ = 'wine_catalog'
    article = columns.Text(primary_key=True)
    name = columns.Text()
    type = columns.Text()
    country = columns.Text()
    region = columns.Text()
    vintage_dating = columns.Integer()
    winery = columns.Text()
    alcohol = columns.Double()
    capacity = columns.Double()
    description = columns.Text()
    price = columns.Double()
    items_left = columns.Integer()

    def to_dict(self):
        return {
            'article': self.article,
            'name': self.name,
            'type': self.type,
            'country': self.country,
            'region': self.region,
            'vintage_dating': self.vintage_dating,
            'winery': self.winery,
            'alcohol': self.alcohol,
            'capacity': self.capacity,
            'description': self.description,
            'price': self.price,
            'items_left': self.items_left
        }
