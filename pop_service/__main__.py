from pop_service import *
import json

## Prototipe implemantation as an OpenWhisk action,
## This function is triggered by MessageHub

def main(kwargs):
    # Read from MeesageHub
    args = kwargs

    # Return with a format for writing to MessageHub
    return { 'value' : json.dumps(create_sample(args)) }
