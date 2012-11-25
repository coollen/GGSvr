# coding:utf-8

import time
import gnet
import prt_test_game

# 初始化
def init():
	print "test_game>init"
	reg()

def reg():
	gnet.reg(prt_test_game.TEST, on_test)

def on_test(data):
	print "on_test", data

	conn_id = data[0]
	msg = data[1]

	time.sleep(1);
	print "sleep 1"
	time.sleep(1);
	print "sleep 1"
	time.sleep(1);
	print "sleep 1"
	gnet.send( conn_id, [msg] )