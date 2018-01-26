
# brew install librdkafka
# pip install confluent-kafka

import confluent_kafka

import json


# Please add your own secret_credentials.json, this is
# generated in IBM CLou on the Service Credentials tab on MessageHub Manager

secret_credentials = "/Users/mario/secret_credentials.json"
secret_opts = {}

with open(secret_credentials) as json_data:
    secret_opts = json.load(json_data)


producer_opts = {
'bootstrap.servers': ','.join(secret_opts['kafka_brokers_sasl']),
'security.protocol': 'SASL_SSL',
#'ssl.ca.location': r'/Users/mario/Certificates.pem',
'sasl.mechanisms': 'PLAIN',
'sasl.username': secret_opts['user'],
'sasl.password': secret_opts['password'],
'api.version.request': True
}


producer = confluent_kafka.Producer (producer_opts)

def on_delivery( err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('Message produced, offset: {0}'.format(msg.offset()))

# Producer

def send_messages( message_list, topic = 'populations-topic' ):
    for pop in message_list:
        producer.produce(topic, json.dumps(pop), 'key', -1, on_delivery)
    producer.flush()




