# coding:utf-8
import gnet

PROTOCOL_OCHE_MSG = 0x01    # 消息定义

def init():
    gnet.reg(PROTOCOL_OCHE_MSG, on_oche)  # 注册处理函数

def on_oche(data):
    print "on_oche", data

    conn_id = data[0]
    msg = data[1]

    gnet.send(conn_id, [PROTOCOL_OCHE_MSG, msg])  # 回发数据
