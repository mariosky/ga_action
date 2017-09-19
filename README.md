# ga_action

Please install requirements.txt to test __main()__ 


Input parameters example:

```
 {  'id':'dc74efeb-9d64-11e7-a2bd-54e43af0c111',

    'problem' :
         {
         'name':'BBOB',
         'function':3,
         'instance':1,
         'search_space':[-5,5]
         },

    'population': [],
    'experiment':
       {
       'experiment_id':'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
       'owner':'mariosky',
       'type':'benchmark'
       },

    'algorithm': {
         'name':'GA',
         'iterations' : 20 ,

         'selection':{
                     'type': 'tools.selTournament',
                     'tournsize' : 12
                     },
         'crossover': {'type':'cxTwoPoint',
                       'CXPB':[0,.2]
                      },

         'mutation':  { 'type': 'mutGaussian',
                       'mu': 0,
                       'sigma':0.5,
                       'indpb': 0.05,
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
    'Best': False
 }

```



Iterations Tuple:

1. Number of iteration
2. Best Fitness
3. Best Individual
4. Number of Function Evaluations

