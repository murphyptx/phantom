"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'run_query_1' block
    run_query_1(container=container)

    return

def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('run_query_1() called')

    # collect data for 'run_query_1' call

    parameters = []
    
    # build parameters list for 'run_query_1' call
    parameters.append({
        'host': "www.splunk.com",
        'max_age': 1,
        'publish': "off",
        'start_new': "off",
        'ignore_mismatch': "off",
        'return_all_data': "on",
    })

    phantom.act(action="run query", parameters=parameters, assets=['qualys_ssl_labs'], callback=format_1, name="run_query_1")

    return

def send_email_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('send_email_2() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'send_email_2' call
    formatted_data_1 = phantom.get_format_data(name='format_1')

    parameters = []
    
    # build parameters list for 'send_email_2' call
    parameters.append({
        'cc': "",
        'to': "pmurphy@splunk.com",
        'bcc': "",
        'body': formatted_data_1,
        'from': "pmurphy@splunk.com",
        'headers': "",
        'subject': formatted_data_1,
        'attachments': "",
    })

    phantom.act(action="send email", parameters=parameters, assets=['smtp'], name="send_email_2")

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_1() called')
    
    template = """SSL Labs Report: {0}  Grade = {1}"""

    # parameter list for template variable replacement
    parameters = [
        "run_query_1:action_result.data.*.host",
        "run_query_1:action_result.data.*.endpoints.*.grade",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    send_email_2(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return