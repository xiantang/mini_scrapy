from urllib.parse import urlparse, parse_qsl, urlencode

scheme, netloc, path, params, query, fragment =urlparse('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=netloc&oq=%25E7%25BF%25BB%25E8%25AF%2591&rsv_pq=ca9d9bd900004252&rsv_t=6d26k0km%2FBaDkgpbAaXMdyTEiD0plOwsa6nloUjdX0%2FFXv7siIVsX6by2U4&rqlang=cn&rsv_enter=1&inputT=204&rsv_n=2&rsv_sug3=29&bs=%E7%BF%BB%E8%AF%91')
print("scheme=",scheme)
print('netloc=',netloc)#域名
print('path=',path)
print('params=',params)
print('query=',query)
print('fragment',fragment)
keyvals = parse_qsl(query)
keyvals.sort()
print(keyvals)
query=urlencode(keyvals)
#转换为元祖
print(query)