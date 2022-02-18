import sys
import base64
from modules import rest_api
from modules import auth as Auth
from modules import args_parser
from modules.logging import log
from modules import spin_pipe as pipeline
from modules import spin_exec as execution
import requests
from time import sleep

def wait_for_start(config, iam_api, execution_id, args):
    log.info("Checking Execution Status")
    execution_status = "NOT STARTED"
    while(execution_status != "RUNNING"):
        url = '{}/executions?executionIds={}'.format(config['gate']['endpoint'], execution_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(iam_api)}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
           log.error(f'Error while fetching execution status from server {url}')
           sys.exit(1)
        response_json = response.json()
        execution_status = response_json[0]['status']
        if execution_status != 'RUNNING':
            log.info("Pipeline not started yet. Waiting {} sec".format(args.delay))
            sleep(args.delay)
    log.info("Pipeline Status is %s" % execution_status)

def check_execution_status(config, iam_api, execution_id, args):
    log.info("Checking Execution Status")
    excepted_statuses = ['SUSPENDED', 'SUCCEEDED', 'TERMINAL', 'CANCELED', 'STOPPED']
    execution_status = "RUNNING"
    while(execution_status not in excepted_statuses):
        url = '{}/executions?executionIds={}'.format(config['gate']['endpoint'], execution_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(iam_api)}
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            log.error('Error while fetching execution status from server {url}')
            sys.exit(1)
        response_json = response.json()
        execution_status = response_json[0]['status']
        if execution_status not in excepted_statuses:
            log.info("Pipeline is in {} state. Waiting {} sec".format(execution_status, args.delay))
            sleep(args.delay)
    log.info("Pipeline Status is %s" % execution_status)

def main():
    args = args_parser.parse_args()
    config = args_parser.read_config(args)
    iam_api, iam_refresh = Auth.get_iam_api_key(config)
    if args.Operation == 'wait_for_start':
        pipeline_id = pipeline.get_pipelineId(config, args, iam_api)
        execution_id = execution.get_executionId(config, args, iam_api)
        wait_for_start(config, iam_api, execution_id, args)
    elif args.Operation == 'check_status':
        pipeline_id = pipeline.get_pipelineId(config, args, iam_api)
        execution_id = execution.get_executionId(config, args, iam_api)
        check_execution_status(config, iam_api, execution_id, args)

if __name__ == '__main__':
    main()
