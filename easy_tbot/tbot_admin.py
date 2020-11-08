#!/usr/bin/env python
import os
import argparse

files_and_content = [('settings.py', """import os

BASEDIR = os.path.dirname(__file__)
TOKEN = ''

SECTIONS = []
GLOBALS = []

DB = 'sqlite:///sqlite.db'

TEMPLATES = {
    'DIR':os.path.join(BASEDIR, 'templates'),
    'AUTOESCAPE': ['txt', 'xml', 'html']
}

PROXY = {}
DEBUG = True
"""),
                     ('botmanager.py', """import os
import sys


def main():
    os.environ.setdefault('BOT_SETTING_MODULE', 'settings')
    from easy_tbot.shell.loader import handle_shell_input
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
        os.mkdir(os.path.join(full_pn, 'templates'))
        for fal in files_and_content:
            with open(os.path.join(full_pn, fal[0]), 'w') as fs:
                fs.write(fal[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Project name')
    args = parser.parse_args()
    if 'name' in vars(args):
        create_project(args.name)
