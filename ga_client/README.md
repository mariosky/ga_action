# ga_client
It's a simple command line client which uses the OpenWhisk REST API from [ga\_service](../ga\_service) to evolve randomly generated populations. It uses [goless channels](http://goless.readthedocs.io/en/latest/) as a way to transfer data from one function to another.

This client creates a specified number of randomly generated populations and evolves them the number of times requested. The formula to calculate the number of evaluations is given by `requests * iterations`. After each evaluation it logs the population into the command line. A redis connection is implemented through localhost on port 6379 to log the populations for further analysis.

## Quick Start
The client may run on different python interpreters. To install the requirements use the following command:
```shell
# cpython
pip install -r requirements.txt

# pypy
pip install -r pypy_requirements.txt
```

The parameters can be tweaked from the command line to test different sets of configurations. To see all the available parameters use:
```shell
python ga_client.py --help
```

## Benchmarks
Some benchmarks were made to know which python platform and backend ran faster. There were some problems with stackless and cptyhon so the results on those benchmarks which resulted in failures can be ignored. Here are the results:

platform|backend|benchmark|time
--------|-------|---------|----
pypy|stackless|2 requests 2 iterations| 10.00s
python|stackless|2 requests 2 iterations| 1.05s
python3|stackless|2 requests 2 iterations| 0.39s
pypy|gevent|2 requests 2 iterations| 8.88s
python|gevent|2 requests 2 iterations| 9.21s
python3|gevent|2 requests 2 iterations| 8.04s
pypy|stackless|3 requests 3 iterations| 19.27s
python|stackless|3 requests 3 iterations| 0.11s
python3|stackless|3 requests 3 iterations| 0.32s
pypy|gevent|3 requests 3 iterations| 20.82s
python|gevent|3 requests 3 iterations| 23.66s
python3|gevent|3 requests 3 iterations| 25.39s
pypy|stackless|4 requests 4 iterations| 38.02s
python|stackless|4 requests 4 iterations| 1.10s
python3|stackless|4 requests 4 iterations| 1.00s
pypy|gevent|4 requests 4 iterations| 39.01s
python|gevent|4 requests 4 iterations| 45.93s
python3|gevent|4 requests 4 iterations| 36.54s
pypy|stackless|5 requests 5 iterations| 74.57s
python|stackless|5 requests 5 iterations| 1.09s
python3|stackless|5 requests 5 iterations| 1.04s
pypy|gevent|5 requests 5 iterations| 57.89s
python|gevent|5 requests 5 iterations| 69.74s
python3|gevent|5 requests 5 iterations| 61.17s
pypy|stackless|6 requests 6 iterations| 95.63s
python|stackless|6 requests 6 iterations| 0.57s
python3|stackless|6 requests 6 iterations| 0.49s
pypy|gevent|6 requests 6 iterations| 100.99s
python|gevent|6 requests 6 iterations| 94.52s
python3|gevent|6 requests 6 iterations| 99.20s

These results can be replicated by running the [benchmark.sh](benchmarks/benchmark.sh) script and providing a path for a virtual environment for pypy`PYPY_VENV` and cpython `CPTYHON_VENV`.
