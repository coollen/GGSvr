# coding:utf-8
import sys, os, socket, urllib, urllib2, hashlib, ssl, time, datetime, json, uuid, types, pickle, math

# 网络请求超时
URLOPEN_TIMEOUT = 10

# 把指定目录下所有目录加入python的查找目录
# 可以绕过python的包结构, 但是不能有重名文件
def patch_sys_path(root="./"):
    sys_paths = []

    def add_path(path):
        if os.path.isdir(path) and path.find(".svn") == -1:
            sys_paths.append(path)
            sub_paths = os.listdir(path)
            for p in sub_paths:
                abs_path = path + p
                if abs_path[-1] != "/": abs_path += "/"
                add_path(abs_path)

    add_path(root)

    for p in sys_paths:
        sys.path.insert(0, p)


# 返回md5
def md5(str_in):
    m = hashlib.md5()
    m.update(str_in)
    return m.hexdigest()


# http_header : dict
def http_call(url, params={}, is_GET=False, http_header=None):
    # print "http_call:", url, params, is_GET
    import glog
    if (is_GET) and params:
        d = ""
        for (k, v) in params.iteritems():
            d += str(k) + "=" + str(v) + "&"
        url += "?" + d
    try:
        request = urllib2.Request(url)
        #http header
        if http_header:
            for k, v in http_header.iteritems():
                request.add_header(str(k), str(v))
        #enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        
        if not is_GET:
            params = urllib.urlencode(params)
            response = opener.open(request, params, timeout=URLOPEN_TIMEOUT)
        else:
            response = opener.open(request, None, timeout=URLOPEN_TIMEOUT)
        result = response.read()
        # print "http_call result:", result
        return result
    except urllib2.HTTPError,e:
        glog.error("HTTPError:%s" % str(e.code))
    except urllib2.URLError,e:
        glog.error("URLErrror:%s" % str(e))
    except socket.timeout, e:
        glog.error("socket.timeout:%s" % str(e))
    except ssl.SSLError, e:
        glog.error("ssl.SSLError:%s" % str(e))
    return None


# 火币网使用了一种数字组合的方式表示时间, 这里称为int_time, 
def inttime2datetime(it):
    time_str = str(it)
    assert len(time_str)==17, "int_time format error"
    y = int(time_str[0:4])
    m = int(time_str[4:6])
    d = int(time_str[6:8])
    h = int(time_str[8:10])
    mi = int(time_str[10:12])
    s = int(time_str[12:14])
    ms = int(time_str[14:17])    
    # ms的定义应该为毫秒, datetime的最后一位是微秒(us)
    return datetime.datetime(y,m,d,h,mi,ms*1000)


def datetime2inttime(dt):
    res = "%0.4d" % dt.year
    res += "%0.2d" % dt.month
    res += "%0.2d" % dt.day
    res += "%0.2d" % dt.hour
    res += "%0.2d" % dt.minute
    res += "%0.2d" % dt.second
    res += dt.microsecond // 1000 # ms的定义应该为毫秒, datetime的最后一位是微秒(us)
    return int(res)

# PS:会损失毫秒
def inttime2timestamp(it):
    dt = inttime2datetime(it)
    return time.mktime(dt.timetuple())

def timestamp2inttime(tt):
    dt = datetime.datetime.fromtimestamp(tt)
    return datetime2inttime(dt)

def timestamp2datetime(tt, is_utc=False):
    dt = None
    if is_utc:
        dt = datetime.datetime.utcfromtimestamp(tt)
    else:
        dt = datetime.datetime.fromtimestamp(tt)
    return dt

def datetime2timestamp(dt, is_utc=False):
    tt = None
    if is_utc:
        tt = time.mktime(dt.utctimetuple())
    else:
        tt = time.mktime(dt.timetuple())
    return tt


# 返回UUID
def UUID(name_space=None):
    if name_space is None:
        return str( uuid.uuid4() )
    else:
        return str( uuid.uuid5(uuid.NAMESPACE_DNS, str(name_space)) )


# 是否为数值
def is_number(v):
    return type(v) in [types.IntType, types.LongType, types.FloatType]


# 空对象, 方便存数据
class EmptyObject():
    pass


# 持久化数据
def write_data(path, data):
    buff = pickle.dumps(data)
    f = open(path, "w")
    f.write(buff)
    f.flush()
    f.close()

def read_data(path):
    f = open(path)
    buff = f.read()
    f.close()
    return pickle.loads(buff)


# 小数位数裁剪, i:保留位数
def floor_cut(number, i):
    mask = pow(10, i)
    return math.floor(number * mask) / mask
