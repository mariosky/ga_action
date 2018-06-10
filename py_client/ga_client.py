from arguments import get_args
from evolution import create_parameters
from evolution import crossover_migration
from evolution import evolve
from evolution import request_evolution_id
from evolution import request_evolved
from goless import chan
from goless import go
from logging_tools import log_to_redis_coco
from logging_tools import log_to_redis_population

# channels
populations = chan()
ids = chan()
evolved = chan()
migrated = chan()
redis_logs = chan()

def create_population_worker(settings):
    """ Creates the amount of populations specified in the settings. """

    for _ in range(0, settings.requests):
        populations.send(create_parameters(settings))

def evolution_id_worker(settings):
    """ Evolves the populations and sends their ids to the ids channel. """

    for _ in range(0, settings.iterations * settings.requests):
        population = populations.recv()
        id = request_evolution_id(settings, population)
        ids.send(id)

def evolved_worker(settings):
    """ Gets the population and sends them to the evolved channel. """

    while True:
        id = ids.recv()
        population = request_evolved(settings, id)
        evolved.send(population)

def migrate_worker(setting):
    """ Migrates the populations and sends them to the migrated channel. """

    population_a = None
    population_b = None
    while True:
        population_a = population_a or evolved.recv()
        population_b = evolved.recv() if population_b else population_a
        population = crossover_migration(
            population_a['population'],
            population_b['population']
        )
        redis_logs.send(population_a)
        migrated.send(population_a)
        population_a = population_b
        parameters = create_parameters(settings, population)
        go(populations.send, parameters)

def print_worker(settings):
    """ Prints the results. """

    for _ in range(0, settings.iterations * settings.requests):
        population = migrated.recv()
        if settings.only_population:
            print(population['population'])
        else:
            print(population)

def log_to_redis_worker(settings):
    """ Logs to redis. """

    for _ in range(0, settings.iterations * settings.requests):
        population = redis_logs.recv()
        if settings.log:
            if settings.only_population:
                log_to_redis_population(population)
            else:
                log_to_redis_coco(population)

if __name__ == "__main__":
    # Gets the settings and makes the requests according to them using channels.

    settings = get_args()
    go(create_population_worker, settings)
    go(evolution_id_worker, settings)
    go(evolved_worker, settings)
    go(migrate_worker, settings)
    go(log_to_redis_worker, settings)
    print_worker(settings)
