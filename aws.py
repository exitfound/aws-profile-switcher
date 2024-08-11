import argparse
import json
from shutil import copy2
from os.path import exists
from os.path import expanduser

credential_file_path = (expanduser("~") + "/.aws/credentials")
profile_file_path = (expanduser("~") + "/.aws/profiles.json")

parser = argparse.ArgumentParser(description='Help for this script:')
parser.add_argument('-p', '--profile', type=str, default="default", help="Input an existing profile AWS")
parser.add_argument('-a', '--profile_path', type=str, default=credential_file_path, help="Input path to your AWS credential file")
parser.add_argument('-j', '--json_path', type=str, default=profile_file_path, help="Input path to the AWS profiles generated file in JSON format.")
parser.add_argument('-g', '--generate', nargs='?', const=profile_file_path, help="Generate a JSON file for the application to run")
parser.add_argument('-e', '--append_profile', nargs='?', const=profile_file_path, help="Append a new profile to JSON file")
parser.add_argument('-d', '--delete_profile', type=str, help="Remove an existing profile from a JSON file")
parser.add_argument('-o', '--original', nargs='?', const=credential_file_path + ".original", help="Save the original AWS credential file")
parser.add_argument('-l', '--list', action='store_true', help="Display all existing AWS profiles")

arguments = parser.parse_args()
json_profiles = arguments.json_path
profiles_exist = exists(json_profiles)

def original_save():
    try:
        open(credential_file_path, 'r')
        copy2(credential_file_path, arguments.original)

    except FileNotFoundError as error:
        print(f"The requested file was not found: \n\n {error}")

def profile_create(profiles_file_name, data_generate):
    while True:
        aws_name = input("Enter the profile name: ")
        aws_access = input("Enter the access key: ")
        aws_secret = input("Enter the secret key: ")
        data_generate['profiles'].append({
            "name": aws_name,
            "aws_access_key": aws_access,
            "aws_secret_key": aws_secret
        })

        break_from_cycle = False

        while True:
            repeat=input("\nEnter Y/N to continue: ")
            if repeat.lower() == 'n':
                break_from_cycle = True
                break
            if repeat.lower() == 'y':
                break
        if break_from_cycle is True:
            break

    with open(profiles_file_name, 'w') as data:
        json.dump(data_generate, data, indent=4)

def main():

    if arguments.original:
        original_save()
        return

    elif arguments.generate:
        data_generate = {'profiles': []}
        profiles_file_name = arguments.generate
        profile_create(profiles_file_name, data_generate)
        return

    elif arguments.append_profile:
        profiles_file_name = arguments.append_profile
        with open(profiles_file_name, "r") as append:
            data_generate = json.load(append)
        profile_create(profiles_file_name, data_generate)
        return

    elif not profiles_exist:
        print("The file on the path", json_profiles, "was not found. Generate or add it manually!")
        return

    open_profiles = open(json_profiles, "r")
    read_data = open_profiles.read()
    data = json.loads(read_data)

    if arguments.delete_profile:
        for value in data['profiles']:
            if value['name'] == arguments.delete_profile:
                data['profiles'].remove(value)
                print("The AWS profile with name", arguments.delete_profile, "has been successfully deleted.")
                break
        else:
            print("The AWS profile with name", arguments.delete_profile, "is not found.")

        with open(json_profiles, 'w') as file:
            file.write(json.dumps(data, indent=4))

    elif arguments.list:
        for value in data['profiles']:
            print(f"[{value['name']}]\naws_access_key = {value['aws_access_key']}\naws_secret_key = {value['aws_secret_key']}\n")

    elif arguments.profile:
        for value in data['profiles']:
            if arguments.profile == value["name"]:
                with open(arguments.profile_path, "w") as file:
                    file.write(f"# Current profile is {value['name']}\n[default]\naws_access_key = {value['aws_access_key']}\naws_secret_key = {value['aws_secret_key']}\n")
                    print("The AWS profile with name", arguments.profile, "has been successfully uploaded.\n")
                break

        else:
            print("The AWS profile with name", arguments.profile, "is not found.\n")

if __name__ == "__main__":
    main()
