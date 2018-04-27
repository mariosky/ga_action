from argparse import ArgumentParser

def get_arguments():
    """ Gets the arguments given to the script.  """

    parser = ArgumentParser(
        description='Makes requests to ga_service using a whisk REST API.'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='verbose output'
    )
    parser.add_argument(
        '-b',
        '--blocking',
        action='store_true',
        help='blocking mode'
    )
    parser.add_argument(
        '-r',
        '--requests',
        type=int,
        default=1,
        help='number of requests (default 1)'
    )
    parser.add_argument(
        '-o',
        '--only-population',
        action='store_true',
        help='return only the population'
    )
    parser.add_argument(
        '--timeout',
        metavar='SECONDS',
        type=int,
        default=60,
        help='seconds for timeout (default 60)'
    )
    parser.add_argument(
        '--apihost',
        metavar='APIHOST',
        type=str,
        help='whisk API HOST (default $APIHOST)'
    )
    parser.add_argument(
        '--namespace',
        type=str,
        help='whisk NAMESPACE (default $NAMESPACE)'
    )
    parser.add_argument(
        '-u',
        '--auth',
        metavar='KEY',
        type=str,
        help='authorization KEY (default wsk property)'
    )
    parser.add_argument(
        '-i',
        '--insecure',
        action='store_true',
        help='bypass certificate checking'
    )
    parser.add_argument(
        '--function',
        type=int,
        default=3,
        help='(default $FUNCTION or 3)'
    )
    parser.add_argument(
        '--instance',
        type=int,
        default=1,
        help='(default $INSTANCE or 1)'
    )
    parser.add_argument(
        '--dim',
        type=int,
        default=3,
        help='(default $DIM or 3)'
    )
    parser.add_argument(
        '--population-size',
        type=int,
        default=20,
        help='population size (default $POPULATION_SIZE or 20)'
    )

    parser.set_defaults(verbose=False, insecure=False)

    return parser.parse_args()
