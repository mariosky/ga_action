from redis import Redis
from json import loads
from json import dumps

class Logger:
    """ Logs messages if the verbose mode is active. """
    def __init__(self, verbose):
        self.verbose = verbose

    def log(self, message):
        if (self.verbose):
            print(message)

HOST="127.0.0.1"
PORT=6379

redis = Redis(host=HOST, port=PORT)

def log_to_redis_coco(population):
    """ Logs to redis. """

    log_name = 'log:test_pop:' + str(population['experiment']["experiment_id"])
    redis.lpush(log_name, dumps(get_benchmark_data(population)))

def log_to_redis_population(population):
    redis.lpush('populations', population['population'])

def get_benchmark_data(population):
    """ Gets the relevant data to log. """

    return {
        "evals": population["iterations"],
        "instance":population["problem"]["instance"],
        "worker_id":"NA",
        "params":{
            "sample_size":population["population_size"],
            "init":"random:[-5,5]",
            "NGEN":population["algorithm"]["iterations"]
        },
        "experiment_id":population['experiment']["experiment_id"],
        "algorithm":population["algorithm"]["name"],
        "dim":population["problem"]["dim"],
        "benchmark":population["problem"]["function"],
        "fopt":population["fopt"]
    }
