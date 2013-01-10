#coding:utf-8
import sys, os
# 脚本路径
SCRIPT_ROOT_PATH = '../'

def patch_sys_path():
    sys_paths = []

    def add_path(path):
        paths = os.listdir(path)
        for p in paths:
            abs_path = path + p
            if abs_path[-1] != "/": abs_path += "/"
            if p == ".svn" or not os.path.isdir(abs_path):
                pass        # 过滤掉.svn  文件
            else:
                add_path(abs_path)
                sys_paths.append(abs_path)

    add_path(SCRIPT_ROOT_PATH)

    for p in sys_paths:
        sys.path.insert(0, p)
    print "patch_sys_path() ok"
patch_sys_path()

#print "sys.path:", sys.path
# ------------------------------------------

import socket, time
import msgpack
import prt_test_game

def send(skt, data):
    buff = msgpack.packb(data)
    skt.send(buff)
    print "[send]"+repr(buff)

def recv(skt):
    '''recv message'''
    buff = skt.recv(10240)
    msg = msgpack.unpackb(buff)
    print "[recv]"+repr(msg)

def login(skt):
    '''send login'''
    net_msg(skt, (1, "coollen", "coollen1"))

def test(skt):
    '''send test'''
    send(skt, (prt_test_game.TEST, "client -> main"))

def test_remote_call(skt):
    '''send test_remote_call'''
    send(skt, (prt_test_game.TEST_REMOTE_CALL, "client -> main"))

FUNC_MAP = {
    "r"    : recv,
    "2"    : login,
    "1"    : test,
    "3"    : test_remote_call,
}


def run (address):
    start_time = time.time()
    client = socket.socket()
    print "connect....", address
    client.connect(address)
    end_time = time.time()
    print "connect use time:", end_time - start_time

    print_help() 

    isExit = False
    while(not isExit):
        cmd = raw_input('>>')

        if cmd in FUNC_MAP:
            FUNC_MAP[cmd](client)
        elif cmd == "q":
            client.close()
            isExit = True
        elif cmd == "c":
            try: client.close()
            except: pass
            client = socket.socket()
            client.connect(address)
        else:
            print_help()


def print_help():
    print "useage:"
    print "c : reconnect"
    print "q : quit"
    for k,v in FUNC_MAP.iteritems():
        print "%s : %s" % (str(k), str(v.__doc__))

if __name__ == "__main__":
    print "--------------------- start -------------------"
    address = ("127.0.0.1", 5020)
    run(address)
    print "--------------------- end ---------------------"

