import os
import json
from bloggen.providers import config_functions as configure_by_provider
from pathlib import Path, PurePath

class Configure:
    
    def __init__(self):
        self.config_path = PurePath.joinpath(Path(__file__).parent, '.bloggen/config.json')
        self.active_config = self.get_active_config()
        if not self.active_config:
            print("No config selected. Using default.")
            print("Create a new configuration with --config option. Activate a configuration with --config [name of config here]")
            self.set_active_config('default')
        self.apply_config(self.active_config)
        print( f'Active config: {self.active_config["name"]}' )
        
    def init_bloggen(self):
        active_config = self.active_config
        backend_provider = active_config['data']['backend']
        provider_config = self.get_provider_config(backend_provider)
        configure_by_provider[backend_provider](provider_config)

    def user_config_exists(self, name):
        return name in self.list_config_names()

    def list_config_names(self):
        with open(self.config_path) as f:
            configs = json.load(f)
        config_names = [config['name'] for config in configs]
        return config_names

    def get_active_config(self):
        with open(self.config_path) as f:
            configs = json.load(f)
        active_config_ls = list(filter(lambda config: config['active'] == True, configs))
        if len(active_config_ls) == 0:
            self.set_active_config('default')
            return self.get_active_config()
        return active_config_ls[0] 

    def set_active_config(self, name):
        """
        Change the active key to true in the config.json file for the given name.
        """
        with open(self.config_path) as f:
            configs: list = json.load(f)
        for user_config in configs:
            if user_config['name'] == name:
                if self.valid_user_config(user_config):
                    self.apply_config(user_config)
                user_config['active'] = True
            else:
                user_config['active'] = False
        with open(self.config_path, 'w') as f:
            json.dump(configs, f)
        self.active_config = user_config['name']

    def get_provider_config(self, backend_provider):
        with open('.bloggen/provider.json') as f:
            providers = json.load(f)
        return providers[backend_provider]

    def add_user_config(self, new_config):
        with open(self.config_path) as f:
            config = json.load(f)
        config.append(new_config)
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
    
    def update_user_config(self, key, value):
        updated_config = self.active_config
        if type(updated_config['data'][key]) is list:
            updated_config['data'][key].append(value)
        else: 
            updated_config['data'][key] = value
        with open(self.config_path) as f:
            config = json.load(f)
        for i, user_config in enumerate(config):
            if user_config['active'] == True:
                config[i] = updated_config
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
        print(f'Set {key} of {self.active_config["name"]} to {value}')
        self.apply_config(self.active_config)

    def create_user_config(self):
        print("creating config")
        new_config = {
            'name': '',
            'active': False,
            'data': {
                'backend': 'gcp',
                "credentials": "path_to_credentials",
                "buckets": [],
                "project": '',
            }
        }
        new_config['name'] = input("Name: ")
        new_config['data']['credentials'] = input("Path to your GCP credentials json: ")
        new_config['data']['buckets'].append(input("Name of GCP Bucket (does not have to exist): ").lower().replace(' ', '-'))
        new_config['data']['project'] = input("Name of GCP Project (project must exist): ").lower().replace(' ', '-')
        self.add_user_config(new_config)
        self.set_active_config(new_config['name'])

    def add_bucket(self):
        pass

    def valid_user_config(self, user_config):
        error = "Please set the path to your credentials file with this command: bloggen --config credentials=path/to/credential"
        if not user_config['data']['credentials']:
            print(error)
            return False
        else:
            config_path = Path(user_config['data']['credentials'])
            if not Path.exists(config_path):
                print(f"Could not find a file at {user_config['data']['credentials']}")
                print(error)
                return False
            return True

    def apply_config(self, config):
        # set credentials of blog host 
        print(config)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['data']['credentials']
        os.environ['GCLOUD_PROJECT'] = config['data']['project']