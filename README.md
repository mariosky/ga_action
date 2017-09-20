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


## How to create the action in Vagrant

First you log in to your vm
```
vagrant ssh
```
Clone the source:
```
git clone https://github.com/mariosky/ga_action
```
Generate the vitualenv folder
```
docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh   -c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"
```
Create the zip files with files needed
```
zip -r ga_service.zip  __main__.py virtualenv ga_service.py bbobbenchmarks.py
```
Create or Update the action
```
wsk action create gaService --kind python:2 ga_service.zip
wsk action update gaService --kind python:2 ga_service.zip
```
Get the url
```
wsk action get gaService  --url
ok: got action gaService
https://192.168.33.13/api/v1/namespaces/guest/actions/gaService
```
Get the auth data
```
wsk property get --auth
whisk auth		23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```

## Test from the host
1. Again clone the code
2. Create your virtualenv, pip install the *requests* library (only needed for client)
3. Edit your ga_client

## TO DO:
1. Environment Variables for client
2. Move client to other repo?



