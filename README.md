GGSvr (GoodGame Server Framework)
=====================
GGSvr是非常轻量级的使用socket的MMORPG服务端框架.它运行在linux下,适用于手机游戏,网页游戏和大型MMO游戏的服务端.


特性:
---------------------
* 纯python
* 多进程负载均衡
* 使用gevent网络底层
* 使用MessagePack作作为网络消息协议
* 使用SQLAlchemy作为存储引擎
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

其他资料:
---------------------
* gevent官网:http://www.gevent.org
* MessagePack官网:http://msgpack.org
* SQLAlchemy官网:http://www.sqlalchemy.org

---------------------
* 我经常打出GG,lol
* 不过,最近在玩dnf
* 增加极简RPC功能
* 学之者生,用之者死,切记切记
* 差不多要写点wiki了
* 认真你就输了
