import json
from json.decoder import JSONDecodeError
import os
from os.path import join
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import yaml
from config import *


def _violation(s):
    print("VIOLATION:", s)


def check_against_schema(file, schema):
    print("-"*5, f"Checking {file}", "-"*5)
    # 1. load to dict
    with open(file, 'r') as f:
        try:
            file_dict = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            _violation("[{}]: {}".format(e.__class__.__name__, e))
            return True
    # 2. validate against schema
    try:
        validate(file_dict, schema)
    except ValidationError as e:
        _violation("[{}]: {}".format(e.__class__.__name__, e.message))
        return True
    return False


if __name__ == "__main__":
    # get the type of files we want to check
    file_type = sys.argv[1]
    if file_type == "adapter":
        files = [f for f in sys.argv[2:] if f.startswith(REPO_FOLDER)]
    elif file_type == "architecture":
        files = [f for f in sys.argv[2:] if f.startswith(ARCHITECTURE_FOLDER)]
    elif file_type == "task":
        files = [f for f in sys.argv[2:] if f.startswith(TASK_FOLDER)]
    elif file_type == "subtask":
        files = [f for f in sys.argv[2:] if f.startswith(SUBTASK_FOLDER)]
    else:
        sys.exit("Invalid entry type '{}'".format(file_type))
    # load schema
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(join(dir_path, 'schemas', '{}.schema.json'.format(file_type)), 'r') as f:
        schema = json.load(f)
    # check files
    for file in files:
        has_error = check_against_schema(file, schema)
        if has_error:
            sys.exit(f"FAILED: {file}!")
        else:
            print(f"PASSED: {file}.")
            print("")
