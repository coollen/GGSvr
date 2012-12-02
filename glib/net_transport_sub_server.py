# coding: utf-8
import gevent
from gevent import monkey;
import socket
import glog

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

# 网络消息最大长度
NET_MESSAGE_MAX_LEN = 1024 * 1024

# 回调函数(from gnet)
global func_on_data, func_on_disconnect, func_on_connect
# 所有连接
global connections
connections = {}


class Connection(object):
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    @property
    def connection_id(self):
        return id(self)
    

# spawn
def spawn(conn):
    while True:
        try:
            buff = conn.socket.recv(NET_MESSAGE_MAX_LEN)
            raise e
            _on_disconnect(conn)
            break
        else:
            _on_data(conn, buff)
            gevent.sleep(0)

    _on_disconnection(conn)



# 初始化
def init(address, on_connect_callback, on_disconnect_callback, on_data_callback):
    global connections
    global func_on_data, func_on_disconnect, func_on_connect

    func_on_connect = on_connect_callback
    func_on_disconnect = on_disconnect_callback
    func_on_data = on_data_callback
    
    # 链接主服务器
    s =socket.socket()
    s.connect(address)
    
    # 放入链接表
    conn = Connection(s, None)      
    connections[conn.connection_id] = conn
    return conn.connection_id


# 循环
def start_loop():
    global connections          
    spawns = []
    for conn_id, conn in connections.iteritems(): 
        s = gevent.spawn(spawn, conn)
        spawns.append(s)
    gevent.joinall(spawns)


# 发送数据
def send(connection_id, buff):
    global connections
    conn = connections[connection_id]
    conn.socket.send(buff)


# 连接
def _on_connect(socket, address):
    global func_on_connect
    conn = Connection(socket, address)
    connections[conn.connection_id] = conn

    if func_on_connect:
        func_on_connect(address, conn.connection_id)

    return conn


# 断开连接
def _on_disconnect(connection):
    global func_on_disconnect
    conn_id = connection.connection_id

    if func_on_disconnect:
        func_on_disconnect(conn_id)

    conn = connections.pop(conn_id)
    try:
        conn.socket.close()
        glog.log("socket close OK")
    except Exception, e:
        raise e


# 数据
def _on_data(connection, buf):
    global func_on_data
    if func_on_data:
        func_on_data(connection.connection_id, buf)
    


