from uuid import uuid1

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

def create_pop(args):
    """ Creates a population for the evolution process. """

    conf = evolution_conf(
        args.function,
        args.instance,
        args.dim,
        args.population_size
    )
    conf['population'] = create_sample(conf)
    return conf

def evolution_conf(function=3, instance=1, dim=3, population_size=20):
    """ Returns the evolution configuration. """

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
