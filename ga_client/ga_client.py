from arguments import get_args
from asyncio import gather
from asyncio import get_event_loop
from evolution import get_handled_pop
from population import create_pop

""" List of evolved responses. """
responses = []

async def ga_action_request(args, i):
    pop = create_pop(args)
    responses[i] = await get_handled_pop(args, pop)

if __name__ == "__main__":
    """ Gets the arguments and makes the requests according to them. """

    args = get_args()
    responses = [None] * args.requests
    loop = get_event_loop()
    loop.run_until_complete(gather(
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
