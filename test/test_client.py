#coding:utf-8
import sys, os, threading, struct
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
    skt.send(_pack(data))
    print "[send]", data

def _pack(data):
    buff = msgpack.packb(data)
    length = len(buff)

    if length > 0xffffffff:
        glog.error("gnet>_pack:data length is OVER")
        return

    len_buff = struct.pack('I', length)
    return len_buff + buff

def recv(skt):
    '''recv message'''
    try:
        buff = _recv_package(skt)
    except Exception, e:
        raise e
        return

    data = msgpack.unpackb(buff)
    print "[recv]", data

def _recv_package(socket):
    len_buff = socket.recv(struct.calcsize('I'))
    if len(len_buff) <= 0:  return ''

    length = struct.unpack('I', len_buff)[0]
    buff = socket.recv(length)
    if len(buff) <= 0:  return ''

    return buff

def login(skt):
    '''send login'''
    net_msg(skt, (1, "coollen", "coollen1"))

def test(skt):
    '''send test'''
    send(skt, (prt_test_game.TEST, "client -> main"))

def stress_test(skt, workder_idx, loop_idx):
    '''send stress_test'''
    send(skt, [prt_test_game.STRESS_TEST,[workder_idx, loop_idx]])

def test_remote_call(skt):
    '''send test_remote_call'''
    send(skt, (prt_test_game.TEST_REMOTE_CALL, "client -> main"))

def test_remote_call_hurge(skt):
    '''test remote_call_hurge'''
    for i in xrange (30000):
        print i
        send(skt, (prt_test_game.TEST_REMOTE_CALL, "client -> main"))

   


FUNC_MAP = {
    "r"     : recv,
    "2"     : login,
    "1"     : test,
    "3"     : test_remote_call,
    "4"     : test_remote_call_hurge,
    "5"     : stress_test,
}




global cskt
cskt = None
global address
address = None
global th_recv
th_recv = None
global t_sum
t_sum = 0
global t_times
t_times = 0

def run (addr):
    global cskt,address,th_recv

    start_time = time.time()
    skt = socket.socket()
    print "connect....", addr
    skt.connect(addr)
    end_time = time.time()
    print "connect use time:", end_time - start_time
    
    cskt = skt    
    address = addr 

    print_help()
    run_cmd()


def run_cmd():
    global cskt, address, th_recv

    is_quit_cmd = False
    while(not is_quit_cmd):
        cmd = raw_input('>>')

        if cmd in FUNC_MAP:
            FUNC_MAP[cmd](cskt)
            recv(cskt)

        elif cmd == "q":
            cskt.close()
            is_quit_cmd = True

        elif cmd == "c":
            try: cskt.close()
            except: pass
            cskt = socket.socket()
            cskt.connect(address)
        
        elif cmd == "st":
            #for i in xrange(30000):
            #    stress_test(cskt)
            #    recv(cskt) 
            run_stress_test()
        else:
            print_help()


def run_stress_test():
    global address, t_sum, t_times
    t_sum = 0
    t_times = 0
    
    WORKER_NUM = 20
    LOOP_NUM = 200

    def __do_stress_test(workder_idx, loop_idx):
        global address, t_sum, t_times
        t1 = time.time()
        
        skt = socket.socket()
        skt.connect(address)
        stress_test(skt, workder_idx, loop_idx)
        recv(skt)
        skt.close()
        
        dt = time.time() - t1
        t_sum += dt
        t_times += 1

        time.sleep(0.01)

    def __st_worker(idx):
        for i in xrange(LOOP_NUM):
            print "%d:%d" % (idx, i)
            __do_stress_test(idx, i) 

    threads = []

    for i in xrange(WORKER_NUM):
        th = threading.Thread(target=__st_worker, args=(i,))
        threads.append(th)

    for th in threads:
        th.start()

    for th in threads:
        th.join()

    print "time sum:",t_sum
    print "times:",t_times
    print "time per time(avg):",t_sum / t_times


def print_help():
    print "useage:"
    print "c : reconnect"
    print "q : quit"
    print "st : run stress test"
    for k,v in FUNC_MAP.iteritems():
        print "%s : %s" % (str(k), str(v.__doc__))

if __name__ == "__main__":
    print "--------------------- start -------------------"
    address = ("192.168.0.104", 5020)
    run(address)
    print "--------------------- end ---------------------"

