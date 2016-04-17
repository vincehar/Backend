from pika import BlockingConnection
from pika import channel
import json
import pika

class rabbitmq:

    channel = channel
    connection = BlockingConnection()

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
        self.connection = pika.BlockingConnection(mq_params)

        # This is one channel inside the connection
        self.channel = self.connection.channel()


    def create_queue(self, _users):
        #Create the queue
        self.channel.queue_declare(queue=_users.user.username,durable=True)
        self.channel.queue_bind(exchange='amq.direct', queue=_users.user.username, routing_key=_users.user.username)
        self.channel.queue_bind(exchange='amq.fanout', queue=_users.user.username)

        #_channel.basic_publish(exchange='', routing_key='test', body='Good morning vietnam')

    def publish_message(self, _users, _message, _general):
        if _general ==  True:
            self.channel.basic_publish(exchange='amq.fanout', routing_key='General', body=_message)
        else:
            self.channel.basic_publish(exchange='amq_direct', routing_key=_users.user.username, body=_message)

    def publish_newweesh(self, _weeshid):
        properties = pika.BasicProperties(headers={'type': 'weesh', 'id': str(_weeshid)})
        self.channel.basic_publish(exchange='amq.fanout', routing_key='General', body='New weesh', properties=properties)


    def close(self):
        self.connection.close()


