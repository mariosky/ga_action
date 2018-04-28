from argparse import ArgumentParser
import os
import subprocess

def get_auth():
    """ Gets the authorization token. """

    return subprocess.check_output(
        'wsk property get --auth',
        shell=True
    ).split()[2].decode('utf-8')

def get_args():
    """ Gets the arguments given to the script.  """

    parser = ArgumentParser(
        description='Makes requests to ga_service using a whisk REST API.'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
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
        default=os.environ['APIHOST'],
        help='whisk API HOST (default $APIHOST)'
    )
    parser.add_argument(
        '--namespace',
        type=str,
        default=os.environ['NAMESPACE'],
        help='whisk NAMESPACE (default $NAMESPACE)'
    )
    parser.add_argument(
        '-u',
        '--auth',
        metavar='KEY',
        type=str,
        default=get_auth(),
        help='authorization KEY (default wsk property)'
    )
    parser.add_argument(
        '-i',
        '--insecure',
        action='store_true',
        default=False,
        help='bypass certificate checking'
    )
    parser.add_argument(
        '--function',
        type=int,
        default='FUNCTION' in os.environ and int(os.environ['FUNCTION']) or 3,
        help='(default $FUNCTION or 3)'
    )
    parser.add_argument(
        '--instance',
        type=int,
        default='INSTANCE' in os.environ and int(os.environ['INSTANCE']) or 1,
        help='(default $INSTANCE or 1)'
    )
    parser.add_argument(
        '--dim',
        type=int,
        default='DIM' in os.environ and int(os.environ['DIM']) or 3,
        help='(default $DIM or 3)'
    )
    parser.add_argument(
        '--population-size',
        type=int,
        default='POPULATION_SIZE' in os.environ and
        int(os.environ['POPULATION_SIZE']) or 20,
        help='population size (default $POPULATION_SIZE or 20)'
    )

    return parser.parse_args()
