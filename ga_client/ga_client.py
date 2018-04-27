import os
import uuid
import json
import subprocess
from string import Template
import asyncio
import aiohttp
from aiohttp import BasicAuth
from arguments import get_arguments

""" Template for the whisk rest api. """
whisk_rest_api = Template(
    '$APIHOST/api/v1/namespaces/$NAMESPACE/$ENDPOINT/$VALUE'
)

""" List of evolved responses. """
responses = []

### FUNCTION DEFINITIONS

class Logger:
    """ Logs messages if the verbose mode is active. """
    def __init__(self, verbose):
        self.verbose = verbose

    def log(self, message):
        if (self.verbose):
            print(message)

def create_sample(conf):
    """ Creates a sample for the evolution process. """

    import random
    from deap import base
    from deap import creator
    from deap import tools

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizing Negative
    creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, -5, 5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                          toolbox.attr_float, conf['problem']['dim'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    pop = toolbox.population(conf['population_size'])
    return [{"chromosome": ind[:], "id": None, "fitness": {"DefaultContext": 0.0}} for ind in pop]

async def ga_action_request(args, i):
    """ Makes a request to evolve a population. """

    logger = Logger(args.verbose)

    url = whisk_rest_api.safe_substitute(
        APIHOST=args.apihost or os.environ['APIHOST'],
        NAMESPACE=args.namespace or os.environ['NAMESPACE'],
        ENDPOINT='actions',
        VALUE='gaService'
    )

    evolution_parameters = {
        "id": str(uuid.uuid1()),
        "problem": {
            "name": "BBOB",
            "function": args.function or
            'FUNCTION' in os.environ and int(os.environ['FUNCTION']) or 3,
            "instance": args.instance or
            'INSTANCE' in os.environ and int(os.environ['INSTANCE']) or 1,
            "search_space": [-5, 5],
            "dim": args.dim or
            'DIM' in os.environ and int(os.environ['DIM']) or 3,
            "error": 1e-8
        },
        "population": [],
        "population_size": args.population_size or
        'POPULATION_SIZE' in os.environ and
        int(os.environ['POPULATION_SIZE']) or 20,
        "experiment": {
            "experiment_id": "dc74efeb-9d64-11e7-a2bd-54e43af0c111",
            "owner": "mariosky",
            "type": "benchmark"
        },
        "algorithm": {
            "name": "GA",
            "iterations": 5,
            "selection": {
                "type": "tools.selTournament",
                "tournsize": 12
            },
            "crossover": {
                "type": "cxTwoPoint",
                "CXPB": [0, 0.2]
            },
            "mutation": {
                "type": "mutGaussian",
                "mu": 0,
                "sigma": 0.5,
                "indpb" : 0.05,
                "MUTPB":0.5
            }
        }
    }
    pop = create_sample(evolution_parameters)
    evolution_parameters['population'] = pop
    EVOLUTION_PARAMETERS = evolution_parameters

    auth = args.auth
    if not auth:
        auth = subprocess.check_output(
            'wsk property get --auth',
            shell=True
        ).split()[2].decode('utf-8')
    auth = auth.split(':')
    AUTH = BasicAuth(auth[0], auth[1])

    BLOCKING = 'true' if args.blocking else 'false'
    RESULT = 'true'

    VERIFY_SSL = not args.insecure

    logger.log('POST[' + str(i) + '] request to ' + url)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url,
                json=EVOLUTION_PARAMETERS,
                params={ 'blocking': BLOCKING, 'result': RESULT },
                auth=AUTH,
                verify_ssl=VERIFY_SSL
        ) as response:
            response = await response.json()
    logger.log('POST[' + str(i) + '] complete!')

    if 'activationId' in response:
        url = whisk_rest_api.safe_substitute(
            APIHOST=args.apihost or os.environ['APIHOST'],
            NAMESPACE=args.namespace or os.environ['NAMESPACE'],
            ENDPOINT='activations',
            VALUE=response['activationId']
        )

        logger.log('Polling[' + str(i) + '] activationId ' +
                   response['activationId'])
        for _ in range(0, args.timeout):
            logger.log('GET[' + str(i) + '] request to ' + url)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        url,
                        params={ 'blocking': BLOCKING, 'result': RESULT },
                        auth=AUTH,
                        verify_ssl=VERIFY_SSL
                ) as response:
                    response = await response.json()
                    logger.log('GET[' + str(i) + '] complete!')
                    if 'error' not in response:
                        break
            await asyncio.sleep(1)

        if ('error' in response):
            raise ValueError('Timeout exception[' + str(i) + '].')

        logger.log('Polling[' + str(i) + '] complete!')
        response = response['response']['result']

    data = json.loads(response['value'])
    responses[i] = data

if __name__ == "__main__":
    """ Gets the arguments and makes the requests according to them. """

    args = get_arguments()
    responses = [None] * args.requests
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        *[ga_action_request(args, i) for i in range(0, args.requests)]
    ))
    loop.close()
    if (args.only_population):
        population = [
            individual
            for response in responses
            for individual in response['population']
        ]
        print(population)
    else:
        print(responses)
