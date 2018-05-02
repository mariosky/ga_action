from evolution import evolution_parameters

def create_sample(parameters):
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
                          toolbox.attr_float, parameters['problem']['dim'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    pop = toolbox.population(parameters['population_size'])
    return [{"chromosome": ind[:], "id": None, "fitness": {"DefaultContext": 0.0}} for ind in pop]

def create_population(settings):
    """ Creates a population for the evolution process. """

    parameters = evolution_parameters(
        settings.function,
        settings.instance,
        settings.dim,
        settings.population_size
    )
    parameters['population'] = create_sample(parameters)
    return parameters
