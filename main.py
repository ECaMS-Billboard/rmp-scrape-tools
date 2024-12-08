import argparse
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
    print(f'{file} uploaded to collection {collection_name} of {db_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file.')
    parser.add_argument('-o', '--output', type=str, help='Path for output file.')
    parser.add_argument('-u', '--upload_to_collection', type=str, help='Upload a JSONL file to the specified collection on MongoDB Atlas.')
    parser.add_argument('-n', '--dbname', type=str, default='EcamsBB', help='Database name on MongoDB Atlas (default: "EcamsBB").')
    parser.add_argument('-m', '--merge', help='Combine properties of matching professor objects between two separate JSON array files.')
    parser.add_argument('-b', '--beautify', help='"Beautify" a JSON array file by formatting it with proper indentation.')
    parser.add_argument('-a' '--array_to_jsonl', help='')
    parser.add_argument('-l' '--jsonl_to_array', help='')

    args = parser.parse_args()

    if args.upload_to_collection:
        warning = f'{c.BOLD}{c.RED}WARNING:{c.ENDC}{c.RED} You are about to upload the file {c.BLUE}{args.input}{c.RED} ' + \
                  f'to collection {c.BLUE}{args.upload_to_collection}{c.RED} of {c.BLUE}{args.dbname}{c.RED}.\n{c.UNDERLINE}' + \
                  f'This will overwrite the collection if it already exists.{c.ENDC}\n\nEnter "CONFIRM" to proceed with the upload: '

        if input(warning) == 'CONFIRM':
            upload_to_mongodb(args.dbname, args.upload, args.input)
            print(f'{c.BLUE}{args.input}{c.ENDC} uploaded successfully.')
            exit()
        else:
            print('Upload cancelled.')
            exit()

    if not args.output:
        if input('No output file is specified, the input file will be overwritten. Continue? (y/n) ').lower() != 'y':
            exit()

    elif args.beautify:
        jf.beautify_json(args.input, args.out)

    elif args.array_to_jsonl:
        jf.array_to_jsonl(args.input, args.out)

    elif args.jsonl_to_array:
        jf.jsonl_to_array(args.input, args.out)

    elif args.merge:
        print('WIP. See function merge() in json_formatter.py for an example.')

