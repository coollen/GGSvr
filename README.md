GGSvr (GoodGame Server Framework)
=====================
GGSvr是非常轻量级的使用socket的MMORPG服务端框架.它运行在linux下,适用于手机游戏,网页游戏和大型MMO游戏的服务端.


特性:
---------------------
* 单线程
* 纯python
* 使用gevent网络底层
* 使用MessagePack作作为网络消息协议
* 使用SQLAlchemy作为存储引擎
* 对程序员友好,松散的文件组织方式,中文注释,精简的API接口,容易进行阅读并修改

将来计划加入的特性:
---------------------
* 多进程负载均衡
* 大厅-游戏房间模式支持
* 分场景的场景管理支持
* 无缝地图场景的场景管理支持

使用说明:
--------------------
* 安装easy_install
  * apt-get install python-setuptools

* 安装gevnet:
  * 安装debian编译环境  apt-get install build-essential 
  * 安装python-dev包 apt-get install python-dev   
  * 安装python-dev包 apt-get install libevent-dev
  * easy_install gevent

* 安装MessagePack
  * easy_install msgpack-python

* 安装SQLAlchemy
  * easy_install sqlalchemy

* 获取GGSvr代码
  * git clone https://github.com/coollen/GGSvr.git

* 启动服务器端
  * python init.py

* 启动测试客户端
  * cd test
  * python test_client.py
  * 输入:h (回车) 可以显示出支持的命令


其他资料:
---------------------
* gevent官网:http://www.gevent.org
* MessagePack官网:http://msgpack.org
* SQLAlchemy官网:http://www.sqlalchemy.org

---------------------
我经常打出GG

