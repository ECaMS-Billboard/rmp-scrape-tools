import sys
import argparse
import json
import pymongo
from pymongo import MongoClient, InsertOne

from secrets import MONGO_URI  # be sure to create secrets.py and add MONGO_URI string variable
import json_formatter as jf


class c:  # terminal color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def upload_to_mongodb(db_name:str, collection_name:str, file:str):
    """
    Upload a JSONL file to MongoDB Altas.
    """

    client = pymongo.MongoClient(MONGO_URI)
    db = client[db_name]
    collection = db[collection_name]
    requesting = []

    with open(file) as f:
        for jsonObj in f:
            myDict = json.loads(jsonObj)
            requesting.append(InsertOne(myDict))

    result = collection.bulk_write(requesting)
    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Required input file argument
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Path to input file (required)')

    parser.add_argument('-o', '--output', type=str,
                        help='Path for output file (if not specified, will prompt before overwriting input)')

    parser.add_argument('-u', '--upload_to_collection', type=str,
                        help='Upload a JSONL file to the specified collection on MongoDB Atlas')

    parser.add_argument('-n', '--dbname', type=str, default='EcamsBB',
                        help='Database name on MongoDB Atlas (default: %(default)s)')

    # only one file operation can be performed at a time
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--beautify', action='store_true',
                        help='Format JSON array file with proper indentation')
    group.add_argument('-m', '--merge', action='store_true',
                        help='Combine properties of matching professor objects between two JSON array files')

    group.add_argument('-a', '--array_to_jsonl', action='store_true',
                        help='Convert JSON array to JSONL format')

    group.add_argument('-l', '--jsonl_to_array', action='store_true',
                        help='Convert JSONL to JSON array format')

    # print help message if no args are given
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    args = parser.parse_args()

    # handle MongoDB upload
    if args.upload_to_collection:
        warning = (f'{c.BOLD}{c.RED}WARNING:{c.ENDC}{c.RED} You are about to upload the file {c.BLUE}{args.input}{c.RED} '
                  f'to collection {c.BLUE}{args.upload_to_collection}{c.RED} of {c.BLUE}{args.dbname}{c.RED}.\n'
                  f'{c.UNDERLINE}This will overwrite the collection if it already exists.{c.ENDC}\n\n'
                  f'Enter "CONFIRM" to proceed with the upload: ')

        if input(warning) == 'CONFIRM':
            upload_to_mongodb(args.dbname, args.upload_to_collection, args.input)
            print(f'{c.BLUE}{args.input}{c.ENDC} uploaded to collection {c.BLUE}{args.upload_to_collection}{c.ENDC}')
            exit()
        else:
            print('Upload cancelled.')
        exit()

    # handle file operations
    output_path = args.output if args.output else args.input
    if not args.output:
        if input('No output file specified. Input file will be overwritten. Continue? (y/n) ').lower() != 'y':
            exit()

    if args.beautify:
        jf.beautify_json(args.input, output_path)

    elif args.array_to_jsonl:
        jf.array_to_jsonl(args.input, output_path)

    elif args.jsonl_to_array:
        jf.jsonl_to_array(args.input, output_path)

    elif args.merge:
        print('WIP. See function merge() in json_formatter.py for an example.')
