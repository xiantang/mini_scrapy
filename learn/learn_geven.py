# import gevent
# from gevent import socket
# urls = ['www.baidu.com', 'www.python.org']
# jobs = [gevent.spawn(socket.gethostbyname,url) for url in urls]
# gevent.joinall(jobs,timeout=2)
# for job in jobs:
#     print(job.value)
# from gevent import monkey;monkey.patch_socket()
# import gevent
#
# def f(n):
#     for i in range(n):
#         print(gevent.getcurrent(),i)
#         gevent.sleep(0)
# g1 = gevent.spawn(f,5000)
# g2 = gevent.spawn(f,5000)
# g3 = gevent.spawn(f,5000)
# g1.join()
# g2.join()
# g3.join()

from gevent import monkey;monkey.patch_all()
import gevent
from urllib import request
def f(url):
    print('GET: %s' % url)
    resp = request.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))

gevent.joinall([
        gevent.spawn(f, 'https://www.python.org/'),
        gevent.spawn(f, 'https://www.yahoo.com/'),
        gevent.spawn(f, 'https://github.com/'),
])