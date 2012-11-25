# coding: utf-8
# 网络模块
import traceback
import msgpack
import net_transport as trans
import glog

# 注册的消息表
global MSG_MAP


# 初始化
def init():
    global MSG_MAP
    MSG_MAP = {}

    ip = ''
    port = 5018
    
    glog.log("server at " + ip +"("+ str(port) +")" )
    trans.init(ip, port, on_connect, on_disconnect, on_data)


# 循环
def start_loop():
    glog.log("gnet>start_loop ------------------")    
    trans.start_loop()



# 注册数据
def reg(id, func):
    global MSG_MAP
    if id in MSG_MAP:
        print "gnet>id already exist|id:%d func:%s" % (id, repr(func))
        return False

    MSG_MAP[id] = func
#    print "MSG_MAP:", MSG_MAP
    return True


# 发送数据
def send(connection_id, data):
    print "gnet>[send]", connection_id, data

    packer = msgpack.Packer()
    serialized = packer.pack(data)
    trans.send(connection_id, serialized)


# client连接
def on_connect(address, connection_id):
    print "on_connect", address, connection_id
    pass


# client断开
def on_disconnect(connection_id):
    print "on_disconnect", connection_id
    pass


# 收到网络消息
def on_data(connection_id, data):
    global MSG_MAP
#    print "gnet>[recv]", connection_id, data
    
    try:
        up = msgpack.Unpacker()
        up.feed(data)
        msg = up.unpack()
    except Exception as e:
        print "gnet>ERROR message format"
        raise e
        return

    # 强制转成[]
    msg = list(msg)
    print "gnet>[recv]", msg
    msgid = msg[0]

    if not msgid in MSG_MAP:
        print "gnet>on_data msgid not in MSG_MAP|msgid:%d" % msgid
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

