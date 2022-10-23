import os
from bloggen.config import Configure
from bloggen.static_site import Site 
from bloggen.site_info import Site_Info
import sys
import argparse
import pathlib

def main():
    config = Configure()
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
    else: 
        args = parser.parse_args()
        if args.config:
            argument: str = args.config
            if argument in ['no_args','create','new']:
                config.create_user_config()
            elif argument in ['list','ls']:
                config.list_config_names()
            elif argument.__contains__('='):
                key, value = argument.split('=')
                config.update_user_config(key,value)
            else:
                if config.user_config_exists(argument):
                    print(f"Activating {argument}")
                    config.set_active_config(argument)
                else:
                    print(f"User config {argument} does not exist.")
                    print(f"These configs exist:")
                    config.list_config_names()
        else:
            if not config.valid_user_config(config.active_config):
                pass
            else:
                site = Site(config)
                if args.add:
                    site.add(args.add)
                elif args.generate:
                    # TODO
                    # if args.generate == 'no_args':
                    #     site.generate()
                    # else:
                    path_to_md_dir: str = args.generate
                    if path_to_md_dir[:3] == '../':
                        path_to_md_dir = clean_parent(path_to_md_dir)
                    site_info = Site_Info(path_to_md_dir, config.active_config["name"])
                    site.generate(pathlib.Path(path_to_md_dir), site_info.site_info)
                elif args.publish:
                    # TODO
                    # if args.publish == 'no_args':
                    #     site.publish()
                    # else:
                    path_to_static_site = args.publish
                    if path_to_static_site[:3] == '../':
                        path_to_static_site = clean_parent(path_to_static_site)
                    site.publish(pathlib.Path(path_to_static_site))

def create_parser():
    parser = argparse.ArgumentParser(description="Create a static site!")
    parser.add_argument('-a', '--add', help="Upload a .md file.")
    parser.add_argument('--destroy', help="Terminates bucket!")
    parser.add_argument('-c','--config', help="Activate or create a configuration", nargs='?', const='no_args')
    parser.add_argument('-g','--generate', help="Builds static site locally. Provide path to md directory.", nargs='?', const='no_args')
    parser.add_argument('--remove', help="Removes a file from bucket.")
    parser.add_argument('--sync', help="Uploads directory to bucket.")
    parser.add_argument('-p','--publish', help="Uploads static site to bucket.", nargs='?', const='no_args')
    return parser

def clean_parent(path: str):
    count = path.count('../')
    cwd = pathlib.Path(os.getcwd())
    while count > 0:
       cwd = cwd.parent
       path = path[3:]
       count-=1
    return pathlib.Path.joinpath(cwd,path)

if __name__ == '__main__':
    main()
