# coding: utf-8
# 远程调用模块
import sys, traceback, socket
import gevent
import glog, gnet


# 远程调用超时 秒
REMOTE_CALL_TIMEOUT = 30

# 远程调用消息头
MSGID_REMOTE_CALL = 'REMOTE_CALL'
MSGID_REMOTE_CALL_RETURN = 'REMOTE_CALL_RETURN'

# 数据 {call_id :gevent.event.AsyncResult}
global call_data
call_data = {}

global next_id
next_id = 0

# 初始化
def init():
    # 注册子服务器RPC
    gnet.reg(MSGID_REMOTE_CALL, on_remote_call)
    gnet.reg(MSGID_REMOTE_CALL_RETURN, on_remote_call_return)


# 发送远程调用
def remote_call(sub_svr_name, sub_svr_id, func, args, kwds):
    global call_data
    if not gnet.is_sub_server:
        call_id = _get_next_id()
        async_result = gevent.event.AsyncResult()
        call_data[call_id] = async_result 
                
        gnet.sends(sub_svr_name, sub_svr_id, [MSGID_REMOTE_CALL, call_id, func, args, kwds])
        # 等待返回
        is_seccess, return_data = async_result.get(True, REMOTE_CALL_TIMEOUT) 
        if is_seccess:
            glog.debug("remote_call>remote_call return:%s" % repr(return_data))
            return return_data
        else:
            glog.error("remote_call>remote_call return Exception:\n%s" % return_data)

            
        
# 收到远程调用
def on_remote_call(data):
    conn_id = data[0]
    call_id = data[1]
    func = data[2]
    args = data[3]
    kwds = data[4]

    try:
        module = func.split('.')[0]
        exec('import ' + module)
        method = eval(func)
        res = apply(method, args, kwds)
    except:
        traceback.print_exc()
        gnet.sendm([MSGID_REMOTE_CALL_RETURN, call_id, False, traceback.format_exc()])
    else:
        gnet.sendm([MSGID_REMOTE_CALL_RETURN, call_id, True, res])

 
# 远程调用结果返回
def on_remote_call_return(data):
    global call_data
    conn_id = data[0]
    call_id = data[1]
    is_seccess = data[2]
    return_data = data[3]
 
    async_result = call_data[call_id]
    async_result.set((is_seccess, return_data))
    
 
def _get_next_id():
    global next_id
    next_id += 1
    return next_id
