import argparse
import json
from shutil import copy2
from os.path import exists
from os.path import expanduser

credential_file_path = (expanduser("~") + "/.aws/credentials")
profile_file_path = (expanduser("~") + "/.aws/profiles.json")

parser = argparse.ArgumentParser(description='Help for this script:')
parser.add_argument('-p', '--profile', type=str, default=None, help="Input an existing profile AWS")
parser.add_argument('-a', '--profile_path', type=str, default=credential_file_path, help="Input path to your AWS credential file")
parser.add_argument('-j', '--json_path', type=str, default=profile_file_path, help="Input path to the AWS profiles generated file in JSON format.")
parser.add_argument('-g', '--generate', nargs='?', const=profile_file_path, help="Generate a JSON file for the application to run")
parser.add_argument('-e', '--append_profile', nargs='?', const=profile_file_path, help="Append a new profile to JSON file")
parser.add_argument('-d', '--delete_profile', type=str, help="Remove an existing profile from a JSON file")
parser.add_argument('-o', '--original', nargs='?', const=credential_file_path + ".original", help="Save the original AWS credential file")
parser.add_argument('-l', '--list', action='store_true', help="Display all existing AWS profiles")
parser.add_argument('-c', '--current', action='store_true', help="Display the current active AWS profile")

arguments = parser.parse_args()
json_profiles = arguments.json_path
profiles_exist = exists(json_profiles)


def mask_key(key):
    if len(key) <= 8:
        return key[:2] + "..." + key[-2:]
    return key[:4] + "..." + key[-4:]


def original_save():
    try:
        copy2(credential_file_path, arguments.original)
    except FileNotFoundError as error:
        print(f"The requested file was not found: \n\n {error}")


def profile_create(profiles_file_name, data_generate):
    while True:
        aws_name = input("Enter the profile name: ")
        aws_access = input("Enter the access key: ")
        aws_secret = input("Enter the secret key: ")
        aws_region = input("Enter the region (leave empty to skip): ")

        profile_entry = {
            "name": aws_name,
            "aws_access_key_id": aws_access,
            "aws_secret_access_key": aws_secret
        }

        if aws_region.strip():
            profile_entry["region"] = aws_region.strip()

        data_generate['profiles'].append(profile_entry)

        break_from_cycle = False

        while True:
            repeat = input("\nEnter Y/N to continue: ")
            if repeat.lower() == 'n':
                break_from_cycle = True
                break
            if repeat.lower() == 'y':
                break
        if break_from_cycle is True:
            break

    with open(profiles_file_name, 'w') as data:
        json.dump(data_generate, data, indent=4)


def show_current():
    if not exists(credential_file_path):
        print("The credential file was not found.")
        return

    with open(credential_file_path, 'r') as f:
        first_line = f.readline().strip()

    if first_line.startswith("# Current profile is "):
        profile_name = first_line.replace("# Current profile is ", "")
        print(f"Current active profile: {profile_name}")
    else:
        print("No profile was set by this tool.")


def main():

    if arguments.original:
        original_save()
        return

    if arguments.generate:
        data_generate = {'profiles': []}
        profiles_file_name = arguments.generate
        profile_create(profiles_file_name, data_generate)
        return

    if arguments.append_profile:
        profiles_file_name = arguments.append_profile
        with open(profiles_file_name, "r") as append:
            data_generate = json.load(append)
        profile_create(profiles_file_name, data_generate)
        return

    if arguments.current:
        show_current()
        return

    if not profiles_exist:
        print("The file on the path", json_profiles, "was not found. Generate or add it manually!")
        return

    with open(json_profiles, "r") as f:
        data = json.load(f)

    if arguments.delete_profile:
        for value in data['profiles']:
            if value['name'] == arguments.delete_profile:
                data['profiles'].remove(value)
                print(f"The AWS profile with name {arguments.delete_profile} has been successfully deleted.")
                with open(json_profiles, 'w') as file:
                    file.write(json.dumps(data, indent=4))
                break
        else:
            print(f"The AWS profile with name {arguments.delete_profile} is not found.")
        return

    if arguments.list:
        for value in data['profiles']:
            region_line = f"region = {value['region']}\n" if 'region' in value else ""
            print(f"[{value['name']}]\n"
                    f"aws_access_key_id = {mask_key(value['aws_access_key_id'])}\n"
                    f"aws_secret_access_key = {mask_key(value['aws_secret_access_key'])}\n"
                    f"{region_line}")
        return

    if arguments.profile:
        for value in data['profiles']:
            if arguments.profile == value["name"]:
                region_line = f"region = {value['region']}\n" if 'region' in value else ""
                with open(arguments.profile_path, "w") as file:
                    file.write(f"# Current profile is {value['name']}\n"
                                f"[default]\n"
                                f"aws_access_key_id = {value['aws_access_key_id']}\n"
                                f"aws_secret_access_key = {value['aws_secret_access_key']}\n"
                                f"{region_line}")
                    print(f"The AWS profile with name {arguments.profile} has been successfully uploaded.\n")
                break
        else:
            print(f"The AWS profile with name {arguments.profile} is not found.\n")
        return

if __name__ == "__main__":
    main()
