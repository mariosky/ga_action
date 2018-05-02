from aiohttp import BasicAuth
from aiohttp import ClientSession
from asyncio import sleep
from json import loads
from string import Template
from util import Logger
from uuid import uuid1

""" Template for the whisk rest api. """
whisk_rest_api = Template(
    '$APIHOST/api/v1/namespaces/$NAMESPACE/$ENDPOINT/$VALUE'
)

def evolution_parameters(function=3, instance=1, dim=3, population_size=20):
    """ Returns the evolution parameters. """

    return {
        'id': str(uuid1()),
        'problem': {
            'name': 'BBOB',
            'function': function,
            'instance': instance,
            'search_space': [-5, 5],
            'dim': dim,
            'error': 1e-8
        },
        'population': [],
        'population_size': population_size,
        'experiment': {
            'experiment_id': 'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
            'owner': 'mariosky',
            'type': 'benchmark'
        },
        'algorithm': {
            'name': 'GA',
            'iterations': 5,
            'selection': {
                'type': 'tools.selTournament',
                'tournsize': 12
            },
            'crossover': {
                'type': 'cxTwoPoint',
                'CXPB': [0, 0.2]
            },
            'mutation': {
                'type': 'mutGaussian',
                'mu': 0,
                'sigma': 0.5,
                'indpb' : 0.05,
                'MUTPB':0.5
            }
        }
    }

def get_request_data(settings, endpoint, value, json={}):
    """ Gets the request data. """

    auth = settings.auth.split(':')
    return {
        'url': whisk_rest_api.safe_substitute(
            APIHOST=settings.apihost,
            NAMESPACE=settings.namespace,
            ENDPOINT=endpoint,
            VALUE=value,
        ),
        'json': json,
        'params': {
            'blocking': str(settings.blocking),
            'result': 'True'
        },
        'auth':BasicAuth(auth[0], auth[1]),
        'verify_ssl': not settings.insecure
    }

def crossover_migration(pop1, pop2, key = lambda p: p['fitness']['score']):
    """ Does the crossover migration. """

    pop1.sort(key=key)
    pop2.sort(key=key)
    size = min(len(pop1), len(pop2))

    cxpoint = round((size - 1) / 2)

    pop1[cxpoint:] = pop2[:cxpoint]

    return pop1

async def request_evolution(settings, population):
    """ Gets the population using blocking. """

    parameters = get_request_data(settings, 'actions', 'gaService', population)

    logger = Logger(settings.verbose)
    logger.log('POST request to ' + parameters['url'])

    async with ClientSession() as session:
        async with session.post(**parameters) as response:
            logger.log('POST complete!')
            return await response.json()

async def request_evolution_id(settings, population):
    """ Evolves a population and returns it's OpenWhisk activationid. """

    response = await request_evolution(settings, population)
    return response['activationId']

async def request_evolved(settings, id):
    """ Gets the population data with it's OpenWhisk activation id. """

    parameters = get_request_data(settings, 'activations', id)

    logger = Logger(settings.verbose)
    logger.log('Polling activationId ' + str(id))

    for _ in range(0, settings.timeout):
        logger.log('GET request to ' + parameters['url'])

        async with ClientSession() as session:
            async with session.get(**parameters) as response:
                logger.log('GET complete!')
                response = await response.json()

                if 'error' not in response:
                    return loads(response['response']['result']['value'])

                await sleep(1)

    raise ValueError('Timeout exception.')

async def evolve(settings, population):
    """ Evolves the population with the given settings. """

    response = await request_evolution(settings, population)
    if 'activationId' in response:
        return await request_evolved(settings, response['activationId'])
    else:
        return loads(response['value'])
