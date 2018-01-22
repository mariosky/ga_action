
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



_opts = {
'bootstrap.servers': ','.join(secret_opts['kafka_brokers_sasl']),
'security.protocol': 'SASL_SSL',
#'ssl.ca.location': r'/Users/mario/Certificates.pem',
'sasl.mechanisms': 'PLAIN',
'sasl.username': secret_opts['user'],
'sasl.password': secret_opts['password'],
'api.version.request': True
}



def on_delivery( err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('Message produced, offset: {0}'.format(msg.offset()))


producer = confluent_kafka.Producer (_opts)


c = confluent_kafka.Consumer(_opts )
c.subscribe(['evolved-topic'])


running = True
while running:
    msg = c.poll()
    if not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))

        producer.produce('populations-topic', msg.value().decode('utf-8'), 'key', -1, on_delivery)
        producer.flush()


    elif msg.error().code() != confluent_kafka.KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False

print ("Bye")
c.close()








