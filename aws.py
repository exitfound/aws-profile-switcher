import argparse
import json
import sys
import os.path
from shutil import copy2
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
parser.add_argument('-o', '--original', nargs='?', const=expanduser("~")+"/.aws/credentials.original", help="Save the original AWS credential file")
parser.add_argument('-l', '--list', action='store_true', help="Display all existing AWS profiles")

arguments = parser.parse_args()
json_profiles = arguments.json_path
profiles_exist = os.path.exists(json_profiles)

def original_save():
    try:
        copy2(credential_file_path, arguments.original)
    except:
        raise SystemExit(f"The file {credential_file_path} does not exist or has already been saved.")

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
        data_generate={}
        data_generate['profiles'] = []

    elif arguments.append_profile:
        with open(profiles_file_name, "r") as append:
            data_generate = json.load(append)

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
            quit=input("\nEnter Y/N to continue: ")
            if quit.lower() == 'n':
                break_from_cycle = True
                break
            if quit.lower() == 'y':
                break
        if break_from_cycle is True:
            break

    with open(profiles_file_name,'w') as file:
        json.dump(data_generate,file,indent=4)
    sys.exit()

if profiles_exist != True:
    print("The file on the path", json_profiles, "was not found. Generate or add it manually!")
    sys.exit()

open_profiles = open(json_profiles, "r")
read_data = open_profiles.read()
data = json.loads(read_data)

if arguments.delete_profile:
    is_deleted = False
    for element in data['profiles']:
        if element['name'] == arguments.delete_profile:
            data['profiles'].remove(element)
            print("The AWS profile with name", arguments.delete_profile, "has been successfully deleted.")
            is_deleted = True
            break

    with open(json_profiles, 'w') as file:
        file.write(json.dumps(data, indent=4))

    if is_deleted == False:
        print("The AWS profile with name", arguments.delete_profile, "is not found.")
    sys.exit()

if arguments.list:
    for list in data['profiles']:
        print(f"[{list['name']}]\naws_access_key = {list['aws_access_key']}\naws_secret_key = {list['aws_secret_key']}\n")
    sys.exit()

for value in data['profiles']:
    if arguments.profile == value["name"]:
        with open(arguments.profile_path, "w") as file:
            file.write(f"# Current profile is {value['name']}\n[default]\naws_access_key = {value['aws_access_key']}\naws_secret_key = {value['aws_secret_key']}\n")
            print("The AWS profile with name", arguments.profile, "has been successfully uploaded.\n")
        break

else:
    print("The AWS profile with name", arguments.profile, "is not found.\n")
