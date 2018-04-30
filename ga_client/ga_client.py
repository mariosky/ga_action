from arguments import get_args
from asyncio import gather
from asyncio import get_event_loop
from evolution import evolve_handled_pop
from population import create_pop

responses = []
populations = []

async def requests(args):
    """ Makes requests to evolve the populations. """

    for i in range(0, args.iterations):
        await gather(
            *[request(args, i) for i in range(0, args.requests)]
        )

async def request(args, i):
    """ Makes a request to evolve a population. """

    responses[i] = await evolve_handled_pop(
        args,
        populations[i]
    )
    populations[i]['population'] = responses[i]['population']

if __name__ == "__main__":
    """ Gets the arguments and makes the requests according to them. """

    args = get_args()
    responses = [None] * args.requests
    populations = [create_pop(args) for _ in responses]
    loop = get_event_loop()
    loop.run_until_complete(requests(args))
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
