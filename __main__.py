from ga_service import *


import os
import uuid


def create_sample(conf):

    import random
    from deap import base
    from deap import creator
    from deap import tools

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizing Negative
    creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, -5, 5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                          toolbox.attr_float, conf['dim'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)



    pop = toolbox.population(conf['sample_size'])
    return [{"chromosome": ind[:], "id": None, "fitness": {"DefaultContext": 0.0}} for ind in pop]





def main(args):
    worker = GA_Worker(conf)
    worker.setup()
    result = worker.run()
    return result


if __name__ == "__main__":

    args= {'id': 'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
           'problem': {
             'name': 'BBOB',
             'function': 3,
             'instance': 1,
             'search_space': [-5, 5]
            },

        'population': [],

        'experiment':
        {
             'experiment_id': 'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
             'owner': 'mariosky',
             'type': 'benchmark'
        },

     'algorithm': {
         'name': 'GA',
         'iterations': 20,

         'selection': {
             'type': 'tools.selTournament',
             'tournsize': 12
         },
         'crossover': {'type': 'cxTwoPoint',
                       'CXPB': [0, .2]
                       },

         'mutation': {'type': 'mutGaussian',
                      'mu': 0,
                      'sigma': 0.5,
                      'indpb' : 0.05,
                       'MUTPB':0.5
                       }
        }
     }




    conf = {}
    conf['function'] = 'FUNCTION' in os.environ and int(os.environ['FUNCTION']) or  3
    conf['instance'] = 'INSTANCE' in os.environ and int(os.environ['INSTANCE']) or  1
    conf['sample_size'] = 'SAMPLE_SIZE' in os.environ and int(os.environ['SAMPLE_SIZE']) or 300
    conf['dim'] = 'DIM' in os.environ and int(os.environ['DIM']) or  5
    conf['benchmark'] = 'BENCHMARK' in os.environ
    conf['NGEN'] = 'NGEN' in os.environ and int(os.environ['NGEN']) or 20
    conf['experiment_id'] = 'EXPERIMENT_ID' in os.environ and int(os.environ['EXPERIMENT_ID']) or str(uuid.uuid1())
    print conf['experiment_id']
    pop = create_sample(conf)

    conf['pop'] = pop




    print main(conf)

