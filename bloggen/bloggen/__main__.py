from bloggen.config import Configure
from bloggen.static_site import Site 
import sys
import argparse
    
def main():
    config = Configure()
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    if args.config:  
        if args.config in ['no_args','create','new']:
            config.create_config()
        elif args.config in ['list','ls']:
            config.list_config_names()
        else:
            if config.config_exists(args.config):
                print(f"Activating {args.config}")
                config.set_active_config(args.config)
            else:
                print(f"Config {args.config} does not exist.")
                print(f"These configs exist:")
                config.list_config_names()
    else:
        site = Site(config)
        if args.add:
            site.add(args.add)
        elif args.generate:
            if args.generate == 'no_args':
                site.generate()
            else:
                site.generate(args.generate)
        elif args.publish:
            if args.publish == 'no_args':
                site.publish()
            else:
                site.publish(args.publish)

def create_parser():
    parser = argparse.ArgumentParser(description="Create a static site!")
    parser.add_argument('-a', '--add', help="Upload a .md file.")
    parser.add_argument('--destroy', help="Terminates bucket!")
    parser.add_argument('-c','--config', help="Activate or create a configuration", nargs='?', const='no_args')
    parser.add_argument('-g','--generate', help="Builds static site locally.", nargs='?', const='no_args')
    parser.add_argument('--remove', help="Removes a file from bucket.")
    parser.add_argument('--sync', help="Uploads directory to bucket.")
    parser.add_argument('-p','--publish', help="Uploads static site to bucket.", action='store_const', const='no_args')
    return parser


if __name__ == '__main__':
    main()