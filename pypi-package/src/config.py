from distutils.command.config import config
import json
from providers import config_functions as configure_by_provider

def configure_bloggen():
    active_config = get_active_config()
    if not active_config:
        print("No config selected. Using default.")
        print("Create a new configuration with --config option and activate a configuration with --config activate [name of config here]")
        set_active_config('default')
        active_config = get_active_config()
    print(active_config)
    backend_provider = active_config['data']['backend']
    provider_config = get_provider_config(backend_provider)
    configure_by_provider[backend_provider](provider_config)

    
def get_active_config():
    with open('.bloggen/config.json') as f:
        configs = json.load(f)
    return list(filter(lambda config: config['active'] == True, configs))[0]

def set_active_config(name):
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

def get_provider_config(backend_provider):
    with open('.bloggen/provider.json') as f:
        providers = json.load(f)
    return providers[backend_provider]