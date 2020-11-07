#!/usr/bin/env python
import os
import argparse

files_and_content = [('settings.py', """import os

BASEDIR = os.path.dirname(__file__)

SECTIONS = []
GLOBALS = []

DB = {
    'engine': 'sqlite',
    'name': '/sqlite.db',
}

TOKEN = ''
PROXY = {}
"""),
                     ('botmanager.py', """import os
from bot_framework.shell.loader import handle_shell_input

import sys


def main():
    os.environ.setdefault('BOT_SETTING_MODULE', 'settings')
    handle_shell_input(*sys.argv[1:])


if __name__ == '__main__':
    main()
""")]


def create_project(project_name):
    full_pn = os.path.join(os.getcwd(), project_name)
    if os.path.exists(full_pn):
        return 'A folder with that name already exist'
    else:
        os.mkdir(full_pn)
        for fal in files_and_content:
            with open(os.path.join(full_pn, fal[0]), 'w') as fs:
                fs.write(fal[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Project name')
    print(parser.parse_args())