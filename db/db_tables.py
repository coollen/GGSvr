# coding:utf-8
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


# 用户表
class User(Base):
	__tablename__ = 'user'

	id = Column(String(32), primary_key=True)
	name = Column(String(10))
	password = Column(String(20))
	create_time = Column(Integer(11))
	last_login_time = Column(Integer(11))
	state = Column(Integer(1))
	
	def __init__(self, id, name, password, create_time, last_login_time, state):
		self.id = id
		self.name = name
		self.password = password
		self.create_time = create_time
		self.last_login_time = last_login_time
		self.state = state
	
	def __repr__(self):
		return "<User('%s','%s')>" % (self.id, self.name)

# 角色表
class Role(Base):
	__tablename__ = 'role'

	id = Column(String(32), primary_key=True) 
	user_id = Column(String(32))
	name = Column(String(10))
	race = Column(Integer(2))

	def __init__(self, id, user_id, name, race):
		self.id = id
		self.user_id = user_id
		self.name = name
		self.race = race
	
	def __repr__(self):
		return "<Role('%s','%s')>" % (self.id, self.name)