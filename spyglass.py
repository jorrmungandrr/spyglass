#!/usr/bin/python

import os
import yaml
import platform
import argparse
from pathlib import Path


def get_database_path():
    database = None
    os_type = platform.system()

    if os_type == 'Linux':
        database = os.environ.get('HOME') + '/.local/share/spyglass-db.yaml'
    elif os_type == 'Windows':
        database = os.environ.get('APPDATA') + 'spyglass-db.yaml'
    else:
        print('OS not supported')
        exit()

    return database



def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--project', type=Path, required=False, help='Path to the project directory')
    parser.add_argument('-s', '--script', type=Path, required=False, help='Path to the script to run')
    parser.add_argument('-c', '--command', type=str, required=False, help='Command to run')
    parser.add_argument('-n', '--name', type=str, required=False, help='Name of the project')
    parser.add_argument('-e', '--editor', type=str, required=False, help='Name of the text editor to use')

    return parser.parse_args()


def handle_db(database, name, project):
    if not os.path.exists(database):
        with open(database, 'w') as f:
            yaml.dump({}, f)

    data = None
    with open(database, 'r') as f:
        data = yaml.safe_load(f)

    if name not in data:
        data[name] = project[name]
    else:
        print('Project already exists')

    with open(database, 'w') as f:
        yaml.dump(data, f)


def collect_project_data(args):
    project_path = args.project
    script = args.script
    name = args.name
    editor = args.editor

    return {name: {'path': str(project_path), 'script': str(project_path/script), 'editor': editor}}




if __name__ == '__main__':
    args = get_args()
    database = get_database_path()

    if not any(vars(args).values()):
        print('TODO : Make it actually do something')
    else:
        project = collect_project_data(args)
        handle_db(database, args.name, project)

