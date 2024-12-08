import ratemyprofessor
from ratemyprofessor.school import School
import json

def get_all_professors(school):
    all_professors = []

    # Try all single letters to catch different name starts
    for letter in string.ascii_lowercase:
        profs = ratemyprofessor.get_professors_by_school_and_name(school, letter)
        for prof in profs:
            if prof not in all_professors:  # Avoid duplicates
                all_professors.append(prof)

    # Also try with an empty string to catch any others
    profs = ratemyprofessor.get_professors_by_school_and_name(school, "")
    for prof in profs:
        if prof not in all_professors:
            all_professors.append(prof)

    return all_professors


def update_ratings(school, input_file: str, output_file=None):
    # Load the existing professor data from a JSON file
    with open(input_file, 'r') as file:
        professors = json.load(file)

    # Loop through each professor and update their information
    for professor in professors:
        try:
            prof = ratemyprofessor.get_professor_by_school_and_name(school, f"{professor['fname']} {professor['lname']}")

            if prof is not None:
                # Extract and normalize the first and last names from the scrape result
                api_fname, api_lname = map(str.lower, prof.name.split(" ", 1))
                local_fname, local_lname = professor['fname'].strip().lower(), professor['lname'].strip().lower()

                if api_fname == local_fname and api_lname == local_lname:
                    print(f"Updating info for {professor['fname']} {professor['lname']}...")
                    professor['num_ratings'] = prof.num_ratings
                    professor['overall_rating'] = str(prof.rating)  # Convert rating to string to match existing format
                else:
                    print(f"Name mismatch: API returned '{prof.name}' for '{professor['fname']} {professor['lname']}' — Skipping.")
            else:
                print(f"Professor {professor['fname']} {professor['lname']} not found on RateMyProfessor.")
        except Exception as e:
            print(f"Error updating {professor['fname']} {professor['lname']}: {e}")

        if output_file is None:
            output_file = input_file

        with open(output_file, 'w') as file:
            json.dump(professors, file, indent=4)

        print(f'Output saved to {output_file}.')


def main():
    lewisu = School(515)
    update_ratings(lewisu, 'data/professors.json', 'data/out.json')

    #all_profs = get_all_professors(lewisu)
    #print(f"Found {len(all_profs)} professors")

    #for prof in all_profs:
    #print(prof)


if __name__ == '__main__':
   main()