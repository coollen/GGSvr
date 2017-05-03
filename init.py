#!/usr/bin/python
# coding: utf-8
import sys;sys.path.append("./comm/")
from helper import patch_sys_path
patch_sys_path()
# ------------------------------
import gconfig, gnet, glog, gdb
#import account_mgr, player_mgr
#import db_tables

def main():

    # 初始化底层库
    # 配置文件
    gconfig.init()

    # 日志
    glog.init()

    # 网络
    gnet.init(gconfig.SVR_MAIN_IP, gconfig.SVR_MAIN_PORT)
    gnet.def_sub_server(gconfig.SVR_SUB_NAME)

    # 数据库
    #gdb.init()

    # mgr
    #account_mgr.init()
    #player_mgr.init()

    # 游戏逻辑
    #import svr_main
    #svr_main.init()
    # 测试 oche
    import oche; oche.init()
    # 测试 client-svr_main-svr_sub
    import svr_test_main; svr_test_main.init()
    

    # 开始服务
    gnet.start_loop()


if __name__ == "__main__":
    main()



