# coding:utf-8
# 数据库管理器

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

global Base
Base = declarative_base()
Session = sessionmaker()

# 数据库引擎来源
ENGINE_SOURCE = 'sqlite:///./sqlite.db'
# 引擎实例
global engine
engine = None
# 连接
global session
session = None



def init():
	global engine
	engine = sa.create_engine(ENGINE_SOURCE, echo=True)	
	Base.metadata.create_all(engine)
	Session.configure(bind=engine)
	

def get_session():
	global session
	if session is None:
		session = Session()
	return session

	



