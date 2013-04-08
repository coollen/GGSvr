GGSvr (GoodGame Server Framework) Ver:0.1
=====================
GGSvr是非常轻量级的使用socket的MMORPG服务端框架.它运行在linux下,适用于手机游戏,网页游戏和大型MMO游戏的服务端.


特性:
---------------------
* 纯python
* 支持多进程负载均衡
* 支持远程调用(RPC),进程间使用RPC通信
* 使用gevent网络底层
* 使用MessagePack作作为网络消息协议
* 使用SQLAlchemy作为存储引擎(可选)
* 对程序员友好,松散的文件组织方式,中文注释,极其精简的API接口,容易进行阅读并修改

将来计划加入的特性:
---------------------
* 大厅-游戏房间模式支持
* 分场景的场景管理支持
* 无缝地图场景的场景管理支持

设计理念:
---------------------
* 从简单易用出发设计API,尽量使用函数式API
* 快速学习后就可以开始游戏逻辑编码,快速上手写逻辑
* 少做出错处理,尽量将错误暴露出来

详细资料:
---------------------
github wiki: https://github.com/coollen/GGSvr/wiki

示例代码:
---------------------
github: https://github.com/coollen/GGSvr/blob/master/test/oche.py

其他资料:
---------------------
* gevent官网:http://www.gevent.org
* MessagePack官网:http://msgpack.org
* SQLAlchemy官网:http://www.sqlalchemy.org

---------------------
* 最近开搞手机游戏啦
* 通过一轮单机的压力测试,结果比我预期的较稳定,也修改了很多bug
* 先把目前的版本定位0.1版本吧,开始稳定这个版本了
* 我将gnet这一层叫做level 1,表示是最低层的上面一层
* 思考账号部分和玩家管理部分
* 认真你就输了

*微薄 http://weibo.com/coollenmmx
