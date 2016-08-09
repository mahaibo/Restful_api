
##pip install virtualenv
##virtualenv flask

##pip install flask

##pip install flask_httpauth

##pip install flask_restful

##pip install passlib

##sudo pip install flask_sqlalchemy

```python
	pip install gunicorn

	gunicorn -b 127.0.0.1:12345 run:app
```

###其中-b为监听的ip和端口，run为文件名，app为创建的flask对象的名称，另外gunicorn默认使用同步阻塞的网络模型，可用通过配置来进行修改


## Post /api/weibos 
```python
curl -i -X POST -H "Content-Type: application/json" -d '{"title":"test1"}' http://127.0.0.1:5000/api/weibos
```

## Get /api/weibos/<int:id> 
```python
curl -i http://127.0.0.1:5000/api/weibos/1
```