import sys
from modules.logging import log
import requests


def get_executionId(config, args, iam_api):
    log.info('Fetching Execution ID')
    url = '{}/applications/{}/executions/search?pipelineName={}&size=100'.format(config['gate']['endpoint'], args.application, args.pipeline)
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(iam_api)}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        log.error('Error while fetching execution id from server {url}')
        sys.exit(1)
    response_json = response.json()
    log.info("Execution ID {}".format(response_json[-1]['id']))
    return response_json[-1]['id']
    log.error('Pipeline not Found')
    sys.exit(1)
