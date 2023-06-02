
from sqlalchemy import Column
from sqlalchemy import String, Integer, Date, Boolean, JSON, Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Departments(Base):
    __tablename__ = 'departments'
    dept_no = Column('dept_no', String(4), primary_key=True)
    dept_name = Column('dept_name', String(40))


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


class Clients(Base):
    __tablename__ = 'clients'
    client_id = Column('client_id', Integer, Sequence('client_id_seq'), primary_key=True)
    first_name = Column('first_name', String(30))
    second_name = Column('second_name', String(30))
    log = Column('client_login', String(30))
    password = Column('client_password', String(50))
    phone_number = Column('phone_number', String(17))
    email = Column('email', String(40))


class OrderTable(Base):
    __tablename__ = 'order_table'
    order_id = Column('order_id', Integer, Sequence('order_id_seq'), primary_key=True)
    address = Column('address', String(70))
    creation_date = Column('creation_date', Date)
    payment_date = Column('payment_date', Date)
    paid = Column('paid', Boolean)
    order_list = Column('order_list', JSON)
    client_id = Column('client_id', Integer, ForeignKey('clients.client_id'))
