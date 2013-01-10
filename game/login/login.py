# coding:utf-8
# 登陆 账号管理 角色管理


import gnet
import account_mgr, player_mgr
from player import Player
import prt_login


# 正在登陆的连接  {conn_id : account, ..}
conn_acc_map = {}
acc_conn_map = {}

# 初始化
def init():
	print "login>init"
	reg()


def reg():
	gnet.reg(prt_login.LOGIN, on_login)
	gnet.reg(prt_login.ROLE_LIST, on_role_list)
	gnet.reg(prt_login.SELECT_ROLE, on_select_role)
	gnet.reg(prt_login.CREATE_ACCOUNT, on_create_account)
	gnet.reg(prt_login.CREATE_ROLE, on_create_role)
	gnet.reg(prt_login.DELETE_ROLE, on_delete_role)


def on_login(data):
	print "on_login", data
	
	conn_id = data[0]
	account = data[1]
	password = data[2]

	isOk = account_mgr.check_password(account, password)

	if( isOk ):
		# 记录连接,账号
		conn_acc_map[conn_id] = account
		acc_conn_map[account] = conn_id

		# msgid, is_login_ok
		gnet.send( conn_id, [ prt_login.LOGIN, 1 ] )
	else:
		gnet.send( conn_id, [ prt_login.LOGIN, 0 ] )


def on_role_list (data):
	print "on_role_list", data

	conn_id = data[0]

	# 检测连接是否登录
	if not check_conn_logined(conn_id): return

	acc = conn_acc_map[conn_id]
	roles = account_mgr.get_account_roles(acc)
	data = []
	for rid, (idx, name) in roles.iteritems():
		data.append(rid)
		data.append(name)

	# msgid, [ 角色id, 角色名字 ]
	gnet.send( conn_id, [ prt_login.ROLE_LIST, data ] )


def on_select_role (data):
	print "on_select_role", data

	conn_id = data[0]
	role_id = data[1]

	# 检测连接是否登录
	if not check_conn_logined(conn_id): return
	
	# 选择玩家之后, 设置登陆数据
	account = get_account_by_connect_id(conn_id)
	player_mgr.set_login_data(conn_id, account, role_id)

	# msgid, isOk
	gnet.send( conn_id, [ prt_login.SELECT_ROLE, 1 ] )


def on_create_account (data):
	print "on_create_account", data

	conn_id = data[0]
	acc = data[1]
	pwd = data[2]
	
	isOk = account_mgr.create_account(acc, pwd)
	
	if isOk:
		# msgid, isOk
		gnet.send( conn_id, [ prt_login.CREATE_ACCOUNT, 1 ] )		
	else:
		gnet.send( conn_id, [ prt_login.CREATE_ACCOUNT, 0 ] )


def on_create_role (data):
	print "on_create_role", data

	conn_id = data[0]
	role_name = data[1]
	role_class = data[2]
	
	# 检测连接是否登录
	if not check_conn_logined(conn_id): return
		
	account = conn_acc_map[conn_id]
	res = player_mgr.create_role(account, role_name, role_class)
	
	if res:
		# msgid, isOk
		gnet.send( conn_id, [ prt_login.CREATE_ROLE, 1 ] )		
	else:
		gnet.send( conn_id, [ prt_login.CREATE_ROLE, 0 ] )


# 删除角色
def on_delete_role (data):
	print "on_delete_role", data

	conn_id = data[0]
	role_id = data[1]
	
	# 检测连接是否登录
	if not check_conn_logined(conn_id): return
		
	account = conn_acc_map[conn_id]
	res = player_mgr.delete_role(account, role_id)
	
	if res:
		# msgid, isOk
		gnet.send( conn_id, [ prt_login.DELETE_ROLE, 1 ] )		
	else:
		gnet.send( conn_id, [ prt_login.DELETE_ROLE, 0 ] )


# 连接是否登录
def check_conn_logined (conn_id):
	if not is_conn_logined(conn_id):
		gnet.send( conn_id, [ prt_login.ERROR, "连接未登录" ] )
		return False
	return True


# 连接是否登录
def is_conn_logined (conn_id):
	return conn_id in conn_acc_map


# 获取conn_id 和 账号的对应关系
def get_connect_id_by_account (account):
	return acc_conn_map.get(account)


def get_account_by_connect_id (conn_id):
	return conn_acc_map.get(conn_id)


	