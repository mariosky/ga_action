from ga_service import *


import os
import uuid


def main(args):
    worker = GA_Worker(args)
    worker.setup()
    result = worker.run()
    return result
