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

    def config_exists(self, name):
        return name in self.list_config_names()

    def list_config_names(self):
        with open(self.config_path) as f:
            configs = json.load(f)
        config_names = [config['name'] for config in configs]
        return config_names

    def get_active_config(self):
        with open(self.config_path) as f:
            configs = json.load(f)
        return list(filter(lambda config: config['active'] == True, configs))[0]

    def set_active_config(self, name):
        """
        Change the active key to true in the config.json file for the given name.
        """
        with open(self.config_path) as f:
            configs: list = json.load(f)
        for config in configs:
            if config['name'] == name:
                self.apply_config(config)
                config['active'] = True
            else:
                config['active'] = False
        with open(self.config_path, 'w') as f:
            json.dump(configs, f)
        self.active_config = config['name']

    def get_provider_config(self, backend_provider):
        with open('.bloggen/provider.json') as f:
            providers = json.load(f)
        return providers[backend_provider]

    def add_config(self, new_config):
        with open(self.config_path) as f:
            config = json.load(f)
        config.append(new_config)
        with open(self.config_path, 'w') as f:
            json.dump(config, f)

    def create_config(self):
        print("creating config")
        new_config = {
            'name': '',
            'active': False,
            'data': {
                'backend': 'gcp',
                "credentials": "path_to_credentials",
                "buckets": []
            }
        }
        new_config['name'] = input("Name: ")
        new_config['data']['credentials'] = input("Path to your GCP credentials json: ")
        new_config['data']['buckets'].append(input("Name of GCP Bucket: ").lower().replace(' ', '-'))
        self.add_config(new_config)


    def add_bucket(self):
        pass

    def apply_config(self, config):
        # set credentials of blog host 
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['data']['credentials']