from ga_service import *
import json

## Prototipe implemantation as an OpenWhisk action,
## This function is triggered by MessageHub

def main(kwargs):
    # Read from MeesageHub
    args = kwargs["messages"][0]["value"]

    worker = GA_Worker(args)
    worker.setup()
    result = worker.run()

    # Return with a format for writing to MessageHub
    return { 'value' : json.dumps(result)}
