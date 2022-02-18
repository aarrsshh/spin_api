import requests
import sys
from modules.logging import log

def get_pipelineId(config, args, iam_api):
    log.info('Fetching Pipeline ID')
    url = '{}/applications/{}/pipelines?expand=false'.format(config['gate']['endpoint'], args.application)
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(iam_api)}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        log.error('Error while fetching pipeline id from server {url}')
        sys.exit(1)
    response_json = response.json()
    for pipelines in response_json:
        if pipelines['name'] == args.pipeline:
            log.info("Pipeline {} Found with ID {}".format(pipelines['name'], pipelines['id']))
            return pipelines['id']
    log.error('Pipeline not Found')
    sys.exit(1)
