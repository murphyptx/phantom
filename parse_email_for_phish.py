# adapted from ews_preprocess.py
from bs4 import BeautifulSoup

def parse_container(container):
    name_to_cef_lookup = {
        'URL Artifact': 'requestURL',
        'Domain Artifact': 'destinationDnsDomain',
        'Hash Artifact': 'fileHash',
        'IP Artifact': 'sourceAddress'
    }

    new_artifacts = []

    phish_email_body = ''
    report_email_body = ''

    email_artifacts = []
    other_artifacts = []
    final_artifacts = []

    for artifact in container.get('artifacts', []):
        if artifact['name'] == 'Email Artifact':
            cef = artifact.get('cef')
            body = cef.get('bodyHtml')

            if 'abuis@splunk.com' in artifact['cef']['toEmail']:
                artifact['name'] = 'Transport - Email Artifact'
                report_email_body = body
            else:
                artifact['name'] = 'Reported - Email Artifact'
                phish_email_body = body
                sender_domain = artifact['cef'].get('fromEmail','@').split('@')[1].replace('>','').replace('<','').replace(';','')
                if sender_domain != '':
                    email_artifacts.append({
                        'name': 'Reported - Sender Domain',
                        'cef': {'destinationDnsDomain': sender_domain}
                    })

            cef = artifact.get('cef')
            body = cef.get('bodyHtml')
            if body:
                soup = BeautifulSoup(body, 'html.parser')
                body = soup.get_text()
                cef['bodyText'] = body

            email_artifacts.append(artifact)
        else:
            other_artifacts.append(artifact)

    for artifact in other_artifacts:
        for key in name_to_cef_lookup.keys():
            if artifact['name'] == key and artifact['cef'].get(name_to_cef_lookup[key]):
                if(
                    artifact['cef'][name_to_cef_lookup[key]] in report_email_body
                    and artifact['cef'][name_to_cef_lookup[key]] not in (phish_email_body or '')
                ):
                    artifact['name'] = 'Transport - ' + artifact['name']
                else:
                    artifact['name'] = 'Reported - ' + artifact['name']

        final_artifacts.append(artifact)

    final_artifacts += email_artifacts

    # Define function to remove from the artifacts list the ones that have 'Reported' in their name
    def remove_values_from_list(the_list, val):
        return [value for value in the_list if val not in value['name']]

    # Run remove_values_from_list on the final artifacts
    final_artifacts_filtered = remove_values_from_list(final_artifacts, 'Transport')

    #if final_artifacts_filtered:
    # final_artifacts_filtered[-1]['run_automation'] = True

    container['artifacts'] = final_artifacts_filtered

    container['run_automation'] = True

    return container
