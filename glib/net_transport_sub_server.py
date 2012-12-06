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
global connection
connections = None


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
        except Exception, e:
            raise e
            _on_disconnect(conn)
            break
        else:
            _on_data(conn, buff)
            gevent.sleep(0)

    _on_disconnection(conn)



# 初始化
def init(address, on_connect_callback, on_disconnect_callback, on_data_callback):
    global connection
    global func_on_data, func_on_disconnect, func_on_connect

    func_on_connect = on_connect_callback
    func_on_disconnect = on_disconnect_callback
    func_on_data = on_data_callback
    
    # 链接主服务器
    s =socket.socket()
    s.connect(address)
    
    conn = _on_connect(s, address)
    return conn.connection_id


# 循环
def start_loop():
    global connection          
    spawns = []
    s = gevent.spawn(spawn, connection)
    spawns.append(s)
    gevent.joinall(spawns)


# 发送数据
def send(buff):
    global connection
    connection.socket.send(buff)


# 连接
def _on_connect(socket, address):
    global func_on_connect, connection
    conn = Connection(socket, address)
    
    if func_on_connect:
        func_on_connect(address, conn.connection_id)

    connection = con
    return conn


# 断开连接
def _on_disconnect(connection):
    global func_on_disconnect, connection
    conn_id = connection.connection_id

    if func_on_disconnect:
        func_on_disconnect(conn_id)

    try:
        connection.socket.close()
        glog.log("socket close OK")
    except Exception, e:
        raise e

    connection = None


# 数据
def _on_data(connection, buf):
    global func_on_data
    if func_on_data:
        func_on_data(connection.connection_id, buf)
    


