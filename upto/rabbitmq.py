from .models import Users
from pika import BlockingConnection
import pika

class rabbitmq:


    def create_connection(self):

        # Use plain credentials for authentication
        mq_creds  = pika.PlainCredentials(
        username = "guest",
        password = "guest")

        # Use localhost
        mq_params = pika.ConnectionParameters(
        host         = "localhost",
        credentials  = mq_creds,
        virtual_host = "/")

        # This a connection object
        mq_conn = pika.BlockingConnection(mq_params)

        return mq_conn

    def get_channel(self,_conn):

        # This is one channel inside the connection
        mq_chan = _conn.channel()

        return mq_chan


    def create_queue(self, _users, _channel):
        #Create the queue
        _channel.queue_declare(queue=_users.user.username,durable=True)
        _channel.queue_bind(exchange='amq.direct', queue=_users.user.username, routing_key=_users.user.username)
        _channel.queue_bind(exchange='amq.fanout', queue=_users.user.username)

        #_channel.basic_publish(exchange='', routing_key='test', body='Good morning vietnam')


    def publish_message(self, _routingKey, _message, _channel, _exchange):
        _channel.basic_publish(exchange=_exchange, routing_key=_routingKey, body=_message)

    def close(self, _conn):
        _conn.close()


