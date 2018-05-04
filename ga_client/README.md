# ga_client
It's a simple command line client which uses the OpenWhisk REST API from [ga\_service](../ga\_service) to evolve randomly generated populations. The parameters can be tweaked from the command line to test different sets of configurations. To see all the available parameters use the command:
```shell
python ga_client.py --help
```

This client creates a specified number of randomly generated populations and evolves them the number of times requested. The formula to calculate the number of evaluations is given by `requests * iterations`. After each evaluation it logs the population into the command line. A redis connection will be implemented in the future to store each result.
