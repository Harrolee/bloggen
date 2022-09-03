from distutils.command.config import config
import json
from providers import config_functions as configure_by_provider

class Configure:
    
    def __init__(self):
        self.active_config = self.get_active_config()
        if not self.active_config:
            print("No config selected. Using default.")
            print("Create a new configuration with --config option and activate a configuration with --config activate [name of config here]")
            self.set_active_config('default')
        print( f'Active config: {self.active_config["name"]}' )
        
    def init_bloggen(self):
        active_config = self.active_config
        backend_provider = active_config['data']['backend']
        provider_config = self.get_provider_config(backend_provider)
        configure_by_provider[backend_provider](provider_config)

    def config_exists(self, name):
        return name in self.list_config_names()

    def list_config_names(self):
        with open('.bloggen/config.json') as f:
            configs = json.load(f)
        config_names = [config['name'] for config in configs]
        return config_names

    def get_active_config(self):
        with open('.bloggen/config.json') as f:
            configs = json.load(f)
        return list(filter(lambda config: config['active'] == True, configs))[0]

    def set_active_config(self, name):
        """
        Change the active key to true in the config.json file for the given name.
        """
        with open('.bloggen/config.json') as f:
            configs = json.load(f)
        for config in configs:
            if config['name'] == name:
                config['active'] = True
            else:
                config['active'] = False
        with open('.bloggen/config.json', 'w') as f:
            json.dump(configs, f)
        self.active_config = config['name']

    def get_provider_config(self, backend_provider):
        with open('.bloggen/provider.json') as f:
            providers = json.load(f)
        return providers[backend_provider]

    def create_config(self):
        # A guided config creation segment
        print("creating config")