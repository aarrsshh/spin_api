import argparse
import yaml
from modules.logging import log

def parse_args():
    parser = argparse.ArgumentParser()

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--config', dest='config', required=True,
                               help='Provide Configuration File')
    common_parser.add_argument('--application', dest='application', required=True,
                               help='Spinnaker Application.')
    common_parser.add_argument('--pipeline', dest='pipeline', required=True,
                               help='Spinnaker Application Pipeline.')

    execution_parser = argparse.ArgumentParser(add_help=False)
    execution_parser.add_argument('--delay', dest='delay', default=5, type=int,
                                  help='Waiting time in seconds. Default is 5 sec')

    subparsers = parser.add_subparsers(dest="Operation")
    subparsers.add_parser('check_status', parents=[common_parser, execution_parser],
                          help='Check the current status of the Application.')
    subparsers.add_parser('wait_for_start', parents=[common_parser, execution_parser],
                          help='Wait for the Pipeline to start execution.')
    subparsers.required = True
    args = parser.parse_args()
    return args

def read_config(args):
    import sys
    log.info('Reading test configuration')
    if args.config:
        log.info('Test Configuration Found at %s' % args.config)
        with open(args.config, 'r') as file:
            test_config_yaml = yaml.load(file.read(), yaml.FullLoader)
    else:
        log.error('No Configuration Found')
        sys.exit(1)
    log.info(test_config_yaml)
    return test_config_yaml
