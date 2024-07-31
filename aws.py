import argparse
import json
from shutil import copy2
import sys
import os.path
from os.path import expanduser

cred_path = (expanduser("~") + "/.aws/credentials")
prof_path = (expanduser("~") + "/.aws/profiles.json")

parser = argparse.ArgumentParser(description='Help for this script:')
parser.add_argument('-p', '--profile', type=str, help="Input an existing profile AWS")
parser.add_argument('-a', '--profile_path', type=str, default=cred_path,
                    help="Input path to your AWS credential file")
parser.add_argument('-j', '--json_path', type=str, default=prof_path,
                    help="Input path to the AWS profiles generated file in JSON format.")
parser.add_argument('-g', '--generate', nargs='?', const=prof_path,
                    help="Generate a JSON file for the application to run")
parser.add_argument('-e', '--append_profile', nargs='?', const=prof_path,
                    help="Append a new profile to JSON file")
parser.add_argument('-d', '--delete_profile', type=str, help="Removing an existing profile from a JSON file")
parser.add_argument('-o', '--original', nargs='?', const=cred_path + ".original",
                    help="Saving the original AWS credential file")
parser.add_argument('-l', '--list', action='store_true', help="Displaying all existing AWS profiles")

arguments = parser.parse_args()
json_profiles = arguments.json_path
profiles_exist = os.path.exists(json_profiles)


def original_save():
    try:
        copy2(cred_path, arguments.original)
    except:
        raise SystemExit(f"The file {cred_path} does not exist or has already been saved.")


if arguments.original:
    original_save()
    sys.exit()

profiles_file_name = ""

if arguments.generate:
    profiles_file_name = arguments.generate

elif arguments.append_profile:
    profiles_file_name = arguments.append_profile

if arguments.generate or arguments.append_profile:
    if arguments.generate:
        data_generate = {'profiles': []}

    elif arguments.append_profile:
        with open(profiles_file_name, "r") as append:
            data_generate = json.load(append)

    while True:
        data_generate['profiles'].append({"name": input("Enter the profile name: "),
                                          "aws_access_key": input("Enter the access key: "),
                                          "aws_secret_key": input("Enter the secret key: ")})

        if input("\nEnter Y/N to continue: ").lower() == 'n': break

    with open(profiles_file_name, 'w') as file:
        json.dump(data_generate, file, indent=4)
    sys.exit()

if not profiles_exist:
    print("The file on the path", json_profiles, "was not found. Generate or add it manually!")
    sys.exit()

open_profiles = open(json_profiles, "r")
read_data = open_profiles.read()
data = json.loads(read_data)

if arguments.delete_profile:
    for element in data['profiles']:
        if arguments.delete_profile in element['name']:
            data['profiles'].remove(element)
            print("The AWS profile with name", arguments.delete_profile, "has been successfully deleted.")
            break
    else:
        print("The AWS profile with name", arguments.delete_profile, "is not found.")

    with open(json_profiles, 'w') as file:
        file.write(json.dumps(data, indent=4))
    sys.exit()

if arguments.list:
    for v in data['profiles']:  # Can't use list
        print(f"[{v['name']}]\naws_access_key = {v['aws_access_key']}\naws_secret_key = {v['aws_secret_key']}\n")
    sys.exit()

for value in data['profiles']:
    if value["name"] in arguments.profile:
        with open(arguments.profile_path, "w") as file:
            file.write(f"# Current profile is {value['name']}\n[default]\naws_access_key = {value['aws_access_key']}"
                       f"\naws_secret_key = {value['aws_secret_key']}\n")
            print("The AWS profile with name", arguments.profile, "has been successfully uploaded.\n")
            break

else:
    print("The AWS profile with name", arguments.profile, "is not found.\n")
