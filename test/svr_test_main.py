# coding:utf-8

import time
import gnet
import prt_test_game
from gconfig import SVR_SUB_NAME, SVR_SUB_ID


global player_conn_id

# 初始化
def init():
    print "test_game>init"
    reg()

def reg():
    gnet.reg(prt_test_game.TEST, on_test)
    gnet.reg(prt_test_game.TEST_SUB, on_test_sub)
    gnet.reg(prt_test_game.TEST_REMOTE_CALL, on_test_remote_call)

def on_test(data):
    print "on_test", data
    global player_conn_id

    conn_id = data[0]
    msg = data[1]

    player_conn_id = conn_id

    time.sleep(1);
    print "sleep 1"
    time.sleep(1);
    print "sleep 1"
    time.sleep(1);
    print "sleep 1"
    #gnet.send( conn_id, [msg] )
    gnet.sends(SVR_SUB_NAME, SVR_SUB_ID, [prt_test_game.TEST_SUB, "mian -> sub"])


def on_test_sub(data):
    print "on_test_sub", data
    global player_conn_id

    conn_id = data[0]
    msg = data[1]

    time.sleep(1)
    print "sleep 1"
    time.sleep(1)
    print "sleep 1"
    time.sleep(1)
    print "sleep 1"
    gnet.send( player_conn_id, [prt_test_game.TEST, "main -> client"]) 
    


def on_test_remote_call(data):
    print "on_test_remote_call", data
    
    conn_id = data[0]
    msg = data[1]

    res = gnet.call(SVR_SUB_NAME, SVR_SUB_ID, "svr_test_sub.remote_call_test", msg, dc="kwds")
    print "remote call return:",res
