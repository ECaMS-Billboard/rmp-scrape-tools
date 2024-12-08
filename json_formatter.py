import json


def array_to_jsonl(input_file, output_file=None):
    """
    Convert a JSON array file to JSONL.
    input_file will be overwritten if a name is not provided for a new output_file.
    """

    if output_file is None:
        output_file = input_file

    with open(input_file, "r") as file:
        data = json.load(file)

    with open(output_file, "w") as file:
        for obj in data:
            json.dump(obj, file)
            file.write("\n")

    print(f"Converted JSONL to JSON and saved to {output_file}")


def jsonl_to_array(input_file, output_file=None):
    """
    Convert a JSONL file to a JSON array file.
    input_file will be overwritten if a name is not provided for a new output_file.
    """

    if output_file is None:
        output_file = input_file

    json_list = []
    with open(input_file, 'r') as file:
        for line in file:
            if line.strip():  # skip empty lines
                # remove trailing comma if it exists
                line = line.strip().rstrip(',')
                json_list.append(json.loads(line))

    with open(output_file, 'w') as file:
        json.dump(json_list, file, indent=4)

    print(f"Converted JSONL to JSON and saved to {output_file}")


def beautify_json(input_file, output_file=None, indent=4):
    """
    'Beautify' a JSON array file by formatting it with proper indentation.
    input_file will be overwritten if a name is not provided for a new output_file.
    """

    with open(input_file, 'r') as file:
        data = json.load(file)

    if output_file is None:
        output_file = input_file

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=indent, sort_keys=True)

    print(f"JSON file beautified and saved to {output_file}")


# TODO
# This function has not been modularized yet. As is, it parses two JSON array files (MAIN.json and RMP.json),
# attempting to find matching (by fname/lname properties) professor objects that are in both files.
# It then combines the dept, num_ratings, and overall_rating properties from RMP.json and the rest of the
# properties from the corresponding objects in MAIN.json. A new file is output.
def merge():
    def load_json(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    rmp_data = load_json('data/RMP.json')
    main_data = load_json('data/MAIN.json')

    merged_data = []

    for main_entry in main_data:
        # Default values
        rmp_info = {
            'dept': 'N/A',
            'num_ratings': 0,
            'overall_rating': 'N/A'
        }

        # Look for matching entries in RMP
        for rmp_entry in rmp_data:
            if (main_entry['fname'].lower() == rmp_entry['fname'].lower() and 
                main_entry['lname'].lower() == rmp_entry['lname'].lower()):
                # If match found, update rmp_info with actual values
                rmp_info = {
                    'dept': rmp_entry['dept'],
                    'num_ratings': rmp_entry['num_ratings'],
                    'overall_rating': rmp_entry['overall_rating']
                }
                break  # Exit loop once a match is found

        # Create merged entry with all MAIN fields plus RMP fields
        merged_entry = {
            '_id': main_entry['_id'],
            'fname': main_entry['fname'],
            'lname': main_entry['lname'],
            'email': main_entry['email'],
            'dept': rmp_info['dept'],
            'num_ratings': rmp_info['num_ratings'],
            'overall_rating': rmp_info['overall_rating']
        }

        merged_data.append(merged_entry)

    # write the merged data to a new JSON file
    with open('merged_professors.json', 'w') as f:
        json.dump(merged_data, f, indent=4)

    print(f"Merged {len(merged_data)} entries into merged_professors.json")
