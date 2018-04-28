from aiohttp import BasicAuth
from aiohttp import ClientSession
from asyncio import sleep
from json import loads
from population import create_pop
from string import Template
from util import Logger

""" Template for the whisk rest api. """
whisk_rest_api = Template(
    '$APIHOST/api/v1/namespaces/$NAMESPACE/$ENDPOINT/$VALUE'
)

async def request_pop(args):
    """ Gets the population using blocking. """

    logger = Logger(args.verbose)

    url = whisk_rest_api.safe_substitute(
        APIHOST=args.apihost,
        NAMESPACE=args.namespace,
        ENDPOINT='actions',
        VALUE='gaService'
    )
    EVOLUTION_PARAMETERS = create_pop(args)
    auth = args.auth.split(':')
    AUTH = BasicAuth(auth[0], auth[1])
    BLOCKING = 'true' if args.blocking else 'false'
    RESULT = 'true'
    VERIFY_SSL = not args.insecure

    logger.log('POST request to ' + url)
    async with ClientSession() as session:
        async with session.post(
                url,
                json=EVOLUTION_PARAMETERS,
                params={ 'blocking': BLOCKING, 'result': RESULT },
                auth=AUTH,
                verify_ssl=VERIFY_SSL
        ) as response:
            logger.log('POST complete!')
            return await response.json()

async def get_id(args):
    """ Gets the id of a population using the OpenWhisk REST API. """
    response = await request_pop(args)
    return response['activationId']

async def get_pop(args, id):
    """ Gets the population data with it's OpenWhisk action id. """

    logger = Logger(args.verbose)

    url = whisk_rest_api.safe_substitute(
        APIHOST=args.apihost,
        NAMESPACE=args.namespace,
        ENDPOINT='activations',
        VALUE=id
    )
    auth = args.auth.split(':')
    AUTH = BasicAuth(auth[0], auth[1])
    BLOCKING = 'true' if args.blocking else 'false'
    RESULT = 'true'
    VERIFY_SSL = not args.insecure

    logger.log('Polling activationId ' + str(id))
    for _ in range(0, args.timeout):
        logger.log('GET request to ' + url)
        async with ClientSession() as session:
            async with session.get(
                    url,
                    params={ 'blocking': BLOCKING, 'result': RESULT },
                    auth=AUTH,
                    verify_ssl=VERIFY_SSL
            ) as response:
                response = await response.json()
                logger.log('GET complete!')
                if 'error' not in response:
                    return loads(response['response']['result']['value'])
                await sleep(1)

    raise ValueError('Timeout exception.')

async def get_handled_pop(args):
    response = await request_pop(args)
    if 'activationId' in response:
        return await get_pop(args, response['activationId'])
    else:
        return response
