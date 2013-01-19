# coding: utf-8
import sys, struct, gevent
from gevent import monkey;
import glog
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()


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
            buff = _recv_package(conn.socket)
        except Exception, e:
            raise e
            break
        
        if len(buff):
            _on_data(conn, buff)
        else:
            glog.debug("trans>recv EMPTY buff, main server disconected")
            break

        gevent.sleep(0)

    _on_disconnect()


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
    global connection
    global func_on_data, func_on_disconnect, func_on_connect

    func_on_connect = on_connect_callback
    func_on_disconnect = on_disconnect_callback
    func_on_data = on_data_callback
    
    # 链接主服务器
    s = gevent.socket.socket()
    s.connect(address)
    _on_connect(s, address)



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
    connection.socket.sendall(buff)


# 连接
def _on_connect(socket, address):
    global func_on_connect, connection
    conn = Connection(socket, address)
    
    if func_on_connect:
        func_on_connect(address, conn.connection_id)

    connection = conn


# 断开连接
def _on_disconnect():
    global func_on_disconnect, connection
    conn_id = connection.connection_id

    if func_on_disconnect:
        func_on_disconnect(conn_id)

    try:
        connection.socket.close()
        glog.log("trans>socket close OK")
    except Exception, e:
        raise e

    connection = None


# 数据
def _on_data(connection, buf):
    global func_on_data
    if func_on_data:
        func_on_data(connection.connection_id, buf)
    


