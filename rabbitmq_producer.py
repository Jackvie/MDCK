import pika


# 链接到RabbitMQ服务器
credentials = pika.PlainCredentials('itheima', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.118.130',5672,'/',credentials))
#创建频道
channel = connection.channel()
# 声明消息队列
channel.queue_declare(queue='zxc')
# routing_key是队列名 body是要插入的内容
channel.basic_publish(exchange='', routing_key='zxc', body='Hello RabbitMQ!')
print("开始向 'zxc' 队列中发布消息 'Hello RabbitMQ!'")
# 关闭链接
connection.close()
