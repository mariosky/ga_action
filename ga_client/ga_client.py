from arguments import get_args
from asyncio import gather
from asyncio import get_event_loop
from evolution import crossover_migration
from evolution import evolve
from population import create_population

responses = []
populations = []

async def requests(settings):
    """ Makes requests to evolve the populations. """

    for i in range(0, settings.iterations):
        await gather(
            *[request(settings, i) for i in range(0, settings.requests)]
        )
        for j in range(0, len(populations)):
            populations[j]['population'] = crossover_migration(
                populations[j]['population'],
                populations[(j + 1) % len(populations)]['population']
            )

async def request(settings, i):
    """ Makes a request to evolve a population. """

    responses[i] = await evolve(
        settings,
        populations[i]
    )
    populations[i]['population'] = responses[i]['population']

if __name__ == "__main__":
    """ Gets the settings and makes the requests according to them. """

    settings = get_args()
    responses = [None] * settings.requests
    populations = [create_population(settings) for _ in responses]
    loop = get_event_loop()
    loop.run_until_complete(requests(settings))
    loop.close()
    if (settings.only_population):
        population = [
            individual
            for response in responses
            for individual in response['population']
        ]
        print(population)
    else:
        print(responses)
