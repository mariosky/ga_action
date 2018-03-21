# ga_action

This is a general framework for carrying out evolution in a serverless framework. It runs, in principle, in a Bluemix environment, but this is actually vendor implementation of open source frameworks such as Kafka and OpenWhisk.

Please install requirements.txt to test __main()__


Input parameters example:
```python
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


Output is the same as input with a new evolved population plus:
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
Clone the source
```
git clone https://github.com/mariosky/ga_action
```
Change directory to ga_service
```
cd ga_service
```
Generate the vitualenv directory
```
docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh -c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"
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
wsk action get gaService --url
ok: got action gaService
https://192.168.33.13/api/v1/namespaces/guest/actions/gaService
```
Get the auth data
```
wsk property get --auth
whisk auth		23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP
```
For updates with out new virtualenv
```
git fetch
```

## Test from the host
1. Again clone the code
2. Create your virtualenv, pip install the *aiohttp* library (only needed for client)
3. Edit your ga_client

## Using the client
The client uses the *asyncio* library which handles asynchronous processes so it requires *python 3* to be executed. You can input different parameters for the script such as the number of request, verbose mode, timeouts, and algorithm specific parameters.

To get a full list of the options you can run the command:
```
python3 ga_client.py --help
```

## Results
If the *--only-population* flag is set then it returns an array of objects which represent each individual with it's id, chromosome and fitness.
```python
[{'id': None, 'chromosome': [-3.0208012286451758, -1.9901786287762588, 0.4746940069424692], 'fitness': {'DefaultContext': -328.99633706375687, 'score': -328.99633706375687}}, {'id': None, 'chromosome': [-3.0208012286451758, -1.9901786287762588, 0.4746940069424692], 'fitness': {'DefaultContext': -328.99633706375687, 'score': -328.99633706375687}}]
```

If the *--only-population* flag is not set then it returns an array of objects which contain the following keys:
```python
[u'fopt', u'algorithm', u'best_individual', u'experiment', u'population_size', u'iterations', u'problem', u'id', u'best', u'population']
```

The results of each iteration look like this:
```python
[0, -422.3189885289348, [-2.3750799310197834, 0.26363257691378017, 1.9725786083712151], 17] -462.09
[1, -450.63219848002547, [-2.3750799310197834, 2.8617458011276007, 1.9725786083712151], 16] -462.09
[2, -450.63219848002547, [-2.3750799310197834, 2.8617458011276007, 1.9725786083712151], 20] -462.09
[3, -450.63219848002547, [-2.3750799310197834, 2.8617458011276007, 1.9725786083712151], 18] -462.09
[4, -450.7095245606381, [-2.3090028418986184, 2.8617458011276007, 1.9725786083712151], 15] -462.09
```
```
[iteration number, best fitness, best solution, number of FE] function optima
```

## TO DO:
1. Environment Variables for client
2. Split the clients request function into smaller functions
3. Move the algorithm parameters to a different json file?

bx wsk action create ga_service --kind python:2 ga_service.zip
