# brew install librdkafka
# pip install confluent-kafka


import confluent_kafka
import json

secret_credentials = "/Users/mario/secret_credentials.json"

secret_opts = {}

with open(secret_credentials) as json_data:
    secret_opts = json.load(json_data)


consumer_opts = {
'bootstrap.servers': ','.join(secret_opts['kafka_brokers_sasl']),
'security.protocol': 'SASL_SSL',
#'ssl.ca.location': r'/Users/mario/Certificates.pem',
'sasl.mechanisms': 'PLAIN',
'sasl.username': secret_opts['user'],
'sasl.password': secret_opts['password'],
'api.version.request': True,
#'default.topic.config': {'auto.offset.reset': 'smallest'},
'group.id': 'mygroup'
}


# Reads evolved populations from evolved-topic

c = confluent_kafka.Consumer(consumer_opts )
c.subscribe(['evolved-topic'])
running = True
while running:
    print '.',
    msg = c.poll()
    if not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))
    elif msg.error().code() != confluent_kafka.KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False
c.close()
