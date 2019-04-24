import pika


# 链接到rabbitmq服务器
credentials = pika.PlainCredentials('itheima', '123456')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672,'/',credentials))
# 创建频道，声明消息队列
channel = connection.channel()
channel.queue_declare(queue='zxc')
# 定义接受消息的回调函数
def callback(ch, method, properties, body):
    print(body)
    # 告诉RabbitMQ使用callback来接收信息
channel.basic_consume(queue='zxc', on_message_callback=callback, auto_ack=True)
# 开始接收信息
channel.start_consuming()
