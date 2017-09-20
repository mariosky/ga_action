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


# Now Works!
# {u'end': 1505919403182, u'name': u'gaService', u'namespace': u'guest', u'publish': False, u'response': {u'status': u'action developer error', u'result': {u'error': u'The action did not return a dictionary.'}, u'success': False}, u'logs': [], u'start': 1505919402935, u'activationId': u'b68ae7c992ca4a2e888bd2b56465ebf6', u'version': u'0.0.1', u'duration': 247, u'annotations': [{u'value': {u'logs': 10, u'timeout': 60000, u'memory': 256}, u'key': u'limits'}, {u'value': u'guest/gaService', u'key': u'path'}], u'subject': u'guest'}
# {u'end': 1505923984186, u'name': u'gaService', u'namespace': u'guest', u'publish': False, u'response': {u'status': u'success', u'result': {u'fopt': -462.09, u'algorithm': {u'mutation': {u'mu': 0, u'sigma': 0.5, u'indpb': 0.05, u'MUTPB': 0.5, u'type': u'mutGaussian'}, u'selection': {u'type': u'tools.selTournament', u'tournsize': 12}, u'name': u'GA', u'iterations': 5, u'crossover': {u'type': u'cxTwoPoint', u'CXPB': [0, 0.2]}}, u'best_individual': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'experiment': {u'owner': u'mariosky', u'type': u'benchmark', u'experiment_id': u'dc74efeb-9d64-11e7-a2bd-54e43af0c111'}, u'population_size': 20, u'iterations': [[0, -432.25878496443374, [-4.255880199850831, 0.8976971997883512, 2.938209472963189], 20], [1, -441.5101001341946, [-4.255880199850831, 3.4062982223470133, 2.938209472963189], 20], [2, -449.1728207891296, [-4.255880199850831, 2.874474334879608, 2.938209472963189], 19], [3, -454.75476557698397, [-4.255880199850831, 2.874474334879608, 2.2400800307063466], 20], [4, -454.75476557698397, [-4.255880199850831, 2.874474334879608, 2.2400800307063466], 20]], u'problem': {u'function': 3, u'dim': 3, u'name': u'BBOB', u'search_space': [-5, 5], u'instance': 1, u'error': 1e-08}, u'id': u'908c865c-9e1e-11e7-b5ea-54e43af0c111', u'best': False, u'population': [{u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.938209472963189], u'fitness': {u'DefaultContext': -449.1728207891296, u'score': -449.1728207891296}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.938209472963189], u'fitness': {u'DefaultContext': -449.1728207891296, u'score': -449.1728207891296}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}, {u'id': None, u'chromosome': [-4.255880199850831, 2.874474334879608, 2.2400800307063466], u'fitness': {u'DefaultContext': -454.75476557698397, u'score': -454.75476557698397}}]}, u'success': True}, u'logs': [], u'start': 1505923980625, u'activationId': u'62c281b99f804ea5ab96c341935916e8', u'version': u'0.0.2', u'duration': 3561, u'annotations': [{u'value': {u'logs': 10, u'timeout': 60000, u'memory': 256}, u'key': u'limits'}, {u'value': u'guest/gaService', u'key': u'path'}], u'subject': u'guest'}
