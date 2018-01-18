import requests
import os
import uuid
import json
import subprocess

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
                          toolbox.attr_float, conf['problem']['dim'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)




    pop = toolbox.population(conf['population_size'])
    return [{"chromosome": ind[:], "id": None, "fitness": {"DefaultContext": 0.0}} for ind in pop]


if __name__ == "__main__":

    args= {'id': str(uuid.uuid1()),
           'problem': {
             'name': 'BBOB',
             'function': 'FUNCTION' in os.environ and int(os.environ['FUNCTION']) or  3,
             'instance': 'INSTANCE' in os.environ and int(os.environ['INSTANCE']) or  1,
             'search_space': [-5, 5],
             'dim': 'DIM' in os.environ and int(os.environ['DIM']) or  3,
             'error': 1e-8
            },

        'population': [],
        'population_size':'POPULATION_SIZE' in os.environ and int(os.environ['POPULATION_SIZE']) or 20,

        'experiment':
        {
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




    pop = create_sample(args)
    args['population'] = pop

    APIHOST = os.environ['APIHOST']

    AUTH_KEY = subprocess.check_output("bx wsk property get --auth", shell=True).split()[2]
    NAMESPACE = os.environ['NAMESPACE']

    ACTION = 'ga_service'
    PARAMS = args
    BLOCKING = 'true'
    RESULT = 'true'

    url = APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
    user_pass = AUTH_KEY.split(':')

    response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))


    result = response.json()

    print result.keys()
    for row in result['iterations']:
        print row

    print result['population']


