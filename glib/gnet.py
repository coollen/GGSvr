# coding: utf-8
# 网络模块
import struct, traceback, socket, msgpack
import net_transport_server as trans
import net_transport_sub_server as trans_sub
import glog

# 注册的消息表
global MSG_MAP
MSG_MAP = {}
# 子服务器表 {name:{id:connection_id},..}
global SUB_SERVER_MAP
SUB_SERVER_MAP = {}
# 子服务器登录消息头
MSGID_SUB_SERVER_LOGIN = 'SUB_SERVER_LOGIN'
# 初始化状态
global is_sub_server
is_sub_server = False

# 网络消息最大长度
NET_MESSAGE_MAX_LEN = 0xFFFFFFFF
NET_MESSAGE_MAX_LEN_SIZE = struct.calcsize('I')


# 初始化
def init(ip, port): 
    glog.log("server at (%s : %d)" % (ip, port))
    trans.init((ip, port), on_connect, on_disconnect, on_data)

    import remote_call;remote_call.init()

    # 注册子服务器登录
    reg(MSGID_SUB_SERVER_LOGIN, on_sub_server_login)


# 初始化子服务器
def init_sub_server(main_ip, main_port, sub_name, sub_id):
    global is_sub_server
    glog.log("server sub_server (%s : %d) at %s:%d" % (sub_name, sub_id, main_ip, main_port)) 
    trans_sub.init((main_ip, main_port), on_connect, on_disconnect, on_data)
    
    import remote_call;remote_call.init()

    # 发送子服务器登录
    trans_sub.send(_pack([MSGID_SUB_SERVER_LOGIN, sub_name, sub_id]))

    is_sub_server = True


# 循环
def start_loop():
    global is_sub_server
    glog.log("gnet>start_loop ------------------")    
    if is_sub_server:    
        trans_sub.start_loop()
    else:
        trans.start_loop()


# 注册数据
def reg(id, func):
    global MSG_MAP
    if id in MSG_MAP:
        glog.warning("gnet>id already exist|id:%d func:%s" % (id, repr(func)))
        return False

    MSG_MAP[id] = func
    return True


# 服务端给客户端发送数据
def send(connection_id, data):
    glog.log("gnet>[send] %d %s" % (connection_id, str(data)))
    trans.send(connection_id, _pack(data))


# 主服务器发送给子服务器
def sends(sub_svr_name, sub_svr_id, data):
    global SUB_SERVER_MAP, is_sub_server
    glog.log("gnet>[sends] (%s : %d) %s" % (sub_svr_name, sub_svr_id, str(data)))

    if is_sub_server:
        glog.error("gnet>can NOT do sends()")
        return

    trans.send(SUB_SERVER_MAP[sub_svr_name][sub_svr_id], _pack(data))


# 子服务器发送给主服务器
def sendm(data):
    global is_sub_server
    glog.log("gnet>[sendm] %s" % str(data))

    if not is_sub_server:
        glog.error("gnet>can NOT do sendm()")
        return

    trans_sub.send(_pack(data))


# 远程调用
def call(sub_svr_name, sub_svr_id, func, *args, **kwds):
    import remote_call
    return remote_call.remote_call(sub_svr_name, sub_svr_id, func, args, kwds)


# client连接
def on_connect(address, connection_id):
    glog.log("on_connect: %s %d" % (address, connection_id))


# client断开
def on_disconnect(connection_id):
    name, id =  _get_sub_server_by_connection(connection_id)
    if name:
        glog.log("on_disconnect sub server: (%s : %d)" % (name, id))
    else:
        glog.log("on_disconnect: %d" % connection_id)    


# 收到网络消息
def on_data(connection_id, buff):
    global MSG_MAP

    try:
        msg = msgpack.unpackb(buff)
    except Exception as e:
        glog.error("gnet>ERROR message format")
        raise e
        return

    # 强制转成[]
    msg = list(msg)
    glog.log("gnet>[recv] %s" % str(msg))
    msgid = msg[0]

    if not msgid in MSG_MAP:
        glog.error("gnet>on_data msgid not in MSG_MAP|msgid:%s" % str(msgid))
        return

    # 调用注册的函数
    func = MSG_MAP[msgid]
    # msg[0]原来是msgid, 在逻辑中没有用处, 所以改成connection_id
    msg[0] = connection_id

    try:
        func(msg) 
    except Exception, e:
        traceback.print_exc()
        #raise e
        

# 断开玩家
def disconnect():
    pass


# 
def _pack(data):
    buff = msgpack.packb(data)
    length = len(buff)

    if length > NET_MESSAGE_MAX_LEN:
        glog.error("gnet>_pack:data length is OVER")
        return

    len_buff = struct.pack('I', length)
    return len_buff + buff


# 设置服务器
def def_sub_server(name):
    global SUB_SERVER_MAP
    SUB_SERVER_MAP[name] = {}


# 子服务器登录
def on_sub_server_login(data):
    global SUB_SERVER_MAP
    
    connection_id = data[0]
    name = data[1]
    id = data[2]

    if not name in SUB_SERVER_MAP:
        glog.error("gnet>on_sub_server_login sub_server NOT def:%s" % name)     
        return

    # 记录链接为服务器链接
    glog.info("gnet>sub server login sucees: (%s : %d)" % (name, id))
    SUB_SERVER_MAP[name][id] = connection_id
    
    # test
    '''
    send(connection_id, ["msgid", "test message"])
    import gevent
    gevent.sleep(2)
    send(connection_id, ["msgid", "test 2"])
    '''

# 检测链接是否是
def _get_sub_server_by_connection(conn_id):
    global SUB_SERVER_MAP
    for name, servers in SUB_SERVER_MAP.iteritems():
        for id, _conn_id in servers.iteritems():
            if _conn_id == conn_id:
                return name, id
    return None, None
