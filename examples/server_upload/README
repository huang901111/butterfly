## 上传文件

## 访问方式

```
curl -v  --data-binary @meetbill.tar.gz  "http://127.0.0.1:8585/put"
or
curl -v  --data-binary @meetbill.tar.gz  "http://127.0.0.1:8585/put?md5=078d291f3452e3483ce0f2f58e219124"
```

## 注意

GET 请求没有请求体，POST 请求有请求体

上传文件时，将文件放到了 POST 的请求体中，则不能将参数请求放到 POST 的请求体中，以免混淆

即注册路由时为：

```
addapi("put", upload.put, False, True)
```
