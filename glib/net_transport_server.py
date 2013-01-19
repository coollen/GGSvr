# coding: utf-8
import sys, struct, gevent
from gevent import monkey;
from gevent.server import StreamServer
import glog
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()


# 服务器实例
global server
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
    

# this handler will be run for each incoming connection in a dedicated greenlet
def spawn(socket, address):
    conn = _on_connect(socket, address)
    while True:
        try:
            buff = _recv_package(socket)
        except Exception, e:
            raise e
            break

        if len(buff):
            _on_data(conn, buff)
        else:
            glog.debug("trans>recv EMPTY buff, client disconected")
            break

        gevent.sleep(0)

    _on_disconnect(conn)


# 
def _recv_package(socket):
    from gnet import NET_MESSAGE_MAX_LEN_SIZE

    len_buff = socket.recv(NET_MESSAGE_MAX_LEN_SIZE)
    if len(len_buff) <= 0:  return ''

    length = struct.unpack('I', len_buff)[0]
    buff = socket.recv(length)
    if len(buff) <= 0:  return ''

    return buff


# 初始化
def init(address, on_connect_callback, on_disconnect_callback, on_data_callback):
    global server
    global func_on_data, func_on_disconnect, func_on_connect

    func_on_connect = on_connect_callback
    func_on_disconnect = on_disconnect_callback
    func_on_data = on_data_callback

    server = StreamServer(address, spawn)


# 循环
def start_loop():
    global server
    server.serve_forever()


# 发送数据
def send(connection_id, buff):
    global conections
    conn = connections[connection_id]
    conn.socket.sendall(buff)


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
        glog.log("trans>socket close OK")
    except Exception, e:
        raise e


# 数据
def _on_data(connection, buff):
    global func_on_data
    if func_on_data:
        func_on_data(connection.connection_id, buff)
    


