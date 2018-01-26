
# brew install librdkafka
# pip install confluent-kafka

import confluent_kafka
import json

import redis_log


REDIS_LOG = True

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
'api.version.request': True,
    'group.id': 'mygroup'}


def on_delivery( err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('offset: {0}'.format(msg.offset())),



def experiment(env):
    producer = confluent_kafka.Producer(globals()['_opts'])

    c = confluent_kafka.Consumer(globals()['_opts'])
    c.subscribe(['evolved-topic'])

    max_messages = env["problem"]["max_iterations"]

    count = 0
    # Counter for experiments, some times we receive from earlier problems
    # Set to zero if not exists
    problem_id = env["problem"]["problem_id"]

    running = True


    while running and count <= max_messages:
        msg = c.poll()
        if not msg.error():

            pop = json.loads( msg.value().decode('utf-8'))
            # Increment counter only if message from this experiment
            if problem_id == pop["problem"]["problem_id"]:
                count+=1
                print count, pop["problem"]["problem_id"]

                #TO DO: CROSSOVER POPULATION HERE

                # Only return if we are in the same experiment
                producer.produce('populations-topic', msg.value().decode('utf-8'), 'key', -1, on_delivery)

            else:
                print "old", pop["problem"]["problem_id"]

            #Log any way, there is no problem if we evaluate more
            if (REDIS_LOG):
                redis_log.log_to_redis_coco(json.loads(msg.value().decode('utf-8')))

        elif msg.error().code() != confluent_kafka.KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    producer.flush()
    print ("Bye")
    c.close()








