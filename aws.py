import argparse
import json
import shutil
import os.path
from os.path import expanduser

parser = argparse.ArgumentParser(description='Help for this script:')
parser.add_argument('-p', '--profile', type=str, default="default", help="Input an existing profile AWS")
parser.add_argument('-a', '--profile_path', type=str, default=expanduser("~")+"/.aws/credentials", help="Input path to your AWS credential file")
parser.add_argument('-j', '--json_path', type=str, default=expanduser("~")+"/.aws/profiles.json", help="Input path to the AWS profiles generated file in JSON format.")
parser.add_argument('-g', '--generate', nargs='?', const=expanduser("~")+"/.aws/profiles.json", help="Generate a JSON file for the application to run")
parser.add_argument('-d', '--generate_append', nargs='?', const=expanduser("~")+"/.aws/profiles.json", help="Generate a JSON file for the application to run")
parser.add_argument('-o', '--original', nargs='?', const=expanduser("~")+"/.aws/credentials.original", help="Saving the original AWS credential file")
parser.add_argument('-l', '--list', action='store_true', help="Displaying all existing AWS profiles")
arguments = parser.parse_args()

originalProfiles = (expanduser("~")+"/.aws/credentials")
jsonProfiles = arguments.json_path
profilesExist = os.path.exists(jsonProfiles)

if arguments.original:
    try:
        shutil.copy2(originalProfiles, arguments.original)
    except FileNotFoundError:
        print(f"{originalProfiles} already saved or does not exist.")
    exit(0)

profiles_file_name = ""

if arguments.generate:
    profiles_file_name = arguments.generate

elif arguments.generate_append:
    profiles_file_name = arguments.generate_append

if arguments.generate or arguments.generate_append:
    if arguments.generate:
        dataGenerate={}
        dataGenerate['profiles'] = []

    elif arguments.generate_append:
        with open(profiles_file_name, "r") as append:
            dataGenerate = json.load(append)

    while True:
        aws_name = input("Enter the profile name: ")
        aws_access = input("Enter the access key: ")
        aws_secret = input("Enter the secret key: ")
        dataGenerate['profiles'].append({
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

    print(profiles_file_name)
    with open(profiles_file_name,'w') as file:
        json.dump(dataGenerate,file,indent=4)
    exit(0)

if profilesExist != True:
    print("The file on the path", jsonProfiles, "was not found. Generate or add it manually!")
    exit(0)

openProfiles = open(jsonProfiles, "r")
readData = openProfiles.read()
data = json.loads(readData)

if arguments.list:
    for list in data['profiles']:
        print(f"[{list['name']}]\naws_access_key = {list['aws_access_key']}\naws_secret_key = {list['aws_secret_key']}\n")
    exit(0)

for value in data['profiles']:
    if arguments.profile == value["name"]:
        with open(arguments.profile_path, "w") as file:
            file.write(f"# Current profile is {value['name']}\n[default]\naws_access_key = {value['aws_access_key']}\naws_secret_key = {value['aws_secret_key']}\n")
            print("The AWS profile with name", arguments.profile, "has been successfully uploaded.\n")
        break

else:
    print("The AWS profile with name", arguments.profile, "is not found.\n")
