
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

print(secret_opts)



producer_opts = {
'bootstrap.servers': ','.join(secret_opts['kafka_brokers_sasl']),
'security.protocol': 'SASL_SSL',
#'ssl.ca.location': r'/Users/mario/Certificates.pem',
'sasl.mechanisms': 'PLAIN',
'sasl.username': secret_opts['user'],
'sasl.password': secret_opts['password'],
'api.version.request': True
}

args_json = """{"algorithm": {"mutation": {"mu": 0, "sigma": 0.5, "indpb": 0.05, "type": "mutGaussian", "MUTPB": 0.5}, "selection": {"type": "tools.selTournament", "tournsize": 12}, "name": "GA", "iterations": 100, "crossover": {"type": "cxTwoPoint", "CXPB": [0, 0.2]}}, "experiment": {"owner": "mariosky", "type": "benchmark", "experiment_id": "dc74efeb-9d64-11e7-a2bd-54e43af0c111"}, "population_size": 20, "problem": {"function": 3, "dim": 3, "name": "BBOB", "search_space": [-5, 5], "instance": 1, "error": 1e-08}, "id": "6d40f0c2-fa8d-11e7-b31b-003ee1bf3fb9", "population": [{"id": null, "chromosome": [-3.7541260735036976, 1.190005602859479, -2.761050982364952], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-2.3907218729912016, -0.15201852407129302, -1.8432725359062618], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [2.6580708929421792, 2.892096612170362, -4.700643043448157], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [3.5345628722900777, 2.8779597633012166, -1.6807480887744997], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-1.9451234493927547, -4.266902139190254, -2.512951897707975], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [1.6556698589796461, 1.8400045603763049, 1.6983578926438074], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [4.7242237810032535, 3.5115092884323023, -2.247600041653542], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-2.1116012502476735, -3.719171219772531, -4.097785454007119], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-4.061863336224404, -3.338466361003216, -3.080484819300829], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [2.060019553162612, -4.7638862366308565, 4.1681405766243635], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-2.007823185709856, -3.944661228364427, 2.2361269395093153], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-2.8629165294833325, -4.984498242523072, 2.989172344955165], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [1.5001078347207493, -0.9423567838220892, 4.414334768172184], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [1.400223979842373, 1.285056358826445, 0.3972638679063403], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-1.1920192813531392, 1.7467660049688671, -4.732754392400893], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [1.0578000211434624, -1.072506318073465, -0.34620839804052395], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [4.212554544577921, 3.8113673203666405, -3.1544400360101985], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [0.6151419347595031, 2.6388020080714414, -3.383434739446962], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [-3.4640642995965143, -4.501144055813432, 1.8152238389226172], "fitness": {"DefaultContext": 0.0}}, {"id": null, "chromosome": [4.267135269165335, 2.018241728617067, 1.5461714565193576], "fitness": {"DefaultContext": 0.0}}]}"""

producer = confluent_kafka.Producer (producer_opts)

def on_delivery( err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('Message produced, offset: {0}'.format(msg.offset()))



producer.produce('populations-topic', args_json, 'key', -1, on_delivery)
producer.flush()








service = "amqps://amqp02-prod02.messagehub.services.eu-gb.bluemix.net:5671"
mhuser = "QLsAUGHHiekiH536"
mhpassword = "UWLDNRAWXWFMqMSG9D6mZkOKQ18ZRDdm"



