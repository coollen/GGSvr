#!/usr/bin/python
# coding: utf-8
import sys;sys.path.append("./comm/")
from helper import patch_sys_path
patch_sys_path()
# ------------------------------
import gconfig, gnet, glog, gdb

def main():

    # 初始化底层库
    # 配置文件
    gconfig.init()

    # 日志
    glog.init()

    # 网络
    gnet.init_sub_server(gconfig.SVR_MAIN_IP, gconfig.SVR_MAIN_PORT, gconfig.SVR_SUB_NAME, gconfig.SVR_SUB_ID)

    # 数据库
    #gdb.init()

    # 测试 client-svr_main-svr_sub
    import svr_test_sub
    svr_test_sub.init()

    # 开始服务
    gnet.start_loop()


if __name__ == "__main__":
    main()



