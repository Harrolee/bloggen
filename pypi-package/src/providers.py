from dotenv import load_dotenv
import os

def config_gcp(gcp_config):
    gcp_config['credential_var']

    if not os.getenv(gcp_config['credential_var']):
        input('GCP credential not found. Please add to .env and then continue.')
        load_dotenv()
        return

    if not os.path.exists('.env'):
        with open( '.env','w') as f:
            f.write('# Get a service token from GCP.')
            f.write('\n# Follow this guide https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication' )
            f.write('\n# Save the JSON to your machine. ')
            f.write('\n# Write the path into this env var.')
            f.write(f'\n{gcp_config["credential_var"]}=')

config_functions = {
    'gcp': config_gcp
}
