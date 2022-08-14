from config import configure_bloggen
from static_site import Site 
from dotenv import load_dotenv
load_dotenv()
import argparse
    
def main():
    configure_bloggen()
    parser = create_parser()
    args = parser.parse_args()
    site = Site()
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
    parser.add_argument('-g','--generate', help="Builds static site locally.", nargs='?', const='no_args')
    parser.add_argument('--remove', help="Removes a file from bucket.")
    parser.add_argument('--sync', help="Uploads directory to bucket.")
    parser.add_argument('-p','--publish', help="Uploads static site to bucket.", action='store_const', const='no_args')
    return parser


if __name__ == '__main__':
    main()