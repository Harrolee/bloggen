from static_site import Site 
from dotenv import load_dotenv
load_dotenv()
import os
import argparse

GCP_TOKEN_NAME = 'GOOGLE_APPLICATION_CREDENTIALS'
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    config()
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


def config():
    if not os.getenv(GCP_TOKEN_NAME):
        input('GCP credential not found. Please add to .env and then continue.')
        load_dotenv()
        return

    if not os.path.exists('.env'):
        with open( '.env','w') as f:
            f.write('# Get a service token from GCP.')
            f.write('\n# Follow this guide https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication' )
            f.write('\n# Save the JSON to your machine. ')
            f.write('\n# Write the path into this env var.')
            f.write(f'\n{GCP_TOKEN_NAME}=')

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