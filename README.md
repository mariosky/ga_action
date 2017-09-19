# ga_action

Please install requirements.txt to test __main()__ 


Input parameters example:

```
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
        'population_size':'POPULATION_SIZE' in os.environ and int(os.environ['POPULATION_SIZE']) or 1000,

        'experiment':
        {
             'experiment_id': 'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
             'owner': 'mariosky',
             'type': 'benchmark'
        },

     'algorithm': {
         'name': 'GA',
         'iterations': 2000,

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

```




Output same as input with a new evolved population plus:


```
 {
    'diversity' :
            {
            'measure':'euclidean',
            'diversity':123
            }

    'iterations':[
     (0, -425.21456490345463, [-0.4316661180759782, 3.9023599854361706, 1.4169751721735144], 258),
     (1, -446.15104470081553, [-4.5856156823256145, 2.271772581290935, 1.6631995281618686], 261)
    ],
    'best': False,
    'best_individual':[-4.5856156823256145, 2.271772581290935, 1.6631995281618686],
    'fopt':-462.09
 }

```



Iterations Tuple:

1. Number of iteration
2. Best Fitness
3. Best Individual
4. Number of Function Evaluations

