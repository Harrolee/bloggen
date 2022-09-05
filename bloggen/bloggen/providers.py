import os

def config_gcp(gcp_config):
    if not os.getenv(gcp_config['credential_var']):
        print('GCP credential not found in this environment. Could not find variable GOOGLE_APPLICATION_CREDENTIALS')
        print('Step 1: Get a service token from GCP. Follow this guide https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication')
        print('Step 2: Save the JSON to your machine.')
        print('Step 3: Set environment variable GOOGLE_APPLICATION_CREDENTIALS to path of your JSON.')

config_functions = {
    'gcp': config_gcp
}
