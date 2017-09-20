import requests
import os
import uuid
import json

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

# Auth data is obtained from vagrant vm
# wsk action create gaService --kind python:2 ga_service.zip
# wsk action get gaService  --url
# wsk property get --auth


    pop = create_sample(args)
    args['population'] = pop
    AUTH = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

    APIHOST = os.environ.get('API_HOST') or 'https://'+AUTH+'@192.168.33.13'
    NAMESPACE = os.environ.get('NAMESPACE') or 'guest'
    USER_PASS = ('whisk','auth')
    action = 'gaService'


    url = APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + action
    response = requests.post(url, json=args, params={'blocking': 'true'}, verify=False)
    print(response.json())


# It gives me the error:
# {u'end': 1505919403182, u'name': u'gaService', u'namespace': u'guest', u'publish': False, u'response': {u'status': u'action developer error', u'result': {u'error': u'The action did not return a dictionary.'}, u'success': False}, u'logs': [], u'start': 1505919402935, u'activationId': u'b68ae7c992ca4a2e888bd2b56465ebf6', u'version': u'0.0.1', u'duration': 247, u'annotations': [{u'value': {u'logs': 10, u'timeout': 60000, u'memory': 256}, u'key': u'limits'}, {u'value': u'guest/gaService', u'key': u'path'}], u'subject': u'guest'}
