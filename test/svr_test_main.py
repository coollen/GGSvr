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
    gnet.reg(prt_test_game.STRESS_TEST, on_stress_test)
    gnet.reg(prt_test_game.STRESS_TEST_SUB, on_stress_test_sub)
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
    gnet.send( player_conn_id, [prt_test_game.TEST, "main -> client"] ) 



def on_test_remote_call(data):
    print "on_test_remote_call", data
    
    conn_id = data[0]
    msg = data[1]

    res = gnet.call(SVR_SUB_NAME, SVR_SUB_ID, "svr_test_sub.remote_call_test", msg, dc="kwds")
    print "remote call return:",res

    gnet.send( conn_id, [prt_test_game.TEST_REMOTE_CALL, msg])



global t_sum, t_times
t_sum = 0
t_times = 0

def on_stress_test(data):
    print "on_stress_test", data
    global t_sum, t_times, no_return

    conn_id = data[0]
    ex_data = data[1]
    """
    t_sum = 0
    t_times = 0
    
    for i in xrange(1000):
        gnet.sends(SVR_SUB_NAME, SVR_SUB_ID, [prt_test_game.STRESS_TEST_SUB, conn_id, time.time()])
        no_return += 1
    """

    #gnet.sends(SVR_SUB_NAME, SVR_SUB_ID, [prt_test_game.STRESS_TEST_SUB, conn_id, time.time()])

    gnet.send( conn_id, [prt_test_game.STRESS_TEST,ex_data])


def on_stress_test_sub(data):
    print "on_stress_test_sub", data
    global t_sum, t_times, no_return

    conn_id = data[0]
    client_conn_id = data[1]
    t1 = data[2]

    gnet.send( client_conn_id, [prt_test_game.STRESS_TEST, "with sub server"] )
    
    dt = time.time() - t1
    t_sum += dt
    t_times += 1
    print "cost time avg:", t_sum / t_times, "times:", t_times


