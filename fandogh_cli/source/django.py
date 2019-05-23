import fnmatch
import os
import sys
import click

from fandogh_cli.utils import format_text, TextStyle


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def wsgi_name_hint():
    cwd = os.getcwd()
    candidates = find_files(os.getcwd(), '*wsgi*.py')
    candidates = map(lambda candidate: candidate[len(cwd) + 1:-3], candidates)
    candidates = map(lambda candidate: candidate.replace(os.sep, '.'), candidates)
    click.echo('Possible wsgi modules are:')
    for candidate in candidates:
        click.echo(' - {}'.format(candidate))


def requirements_hint():
    req_path = os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.isfile(req_path):
        return
    click.echo(
        format_text(
            'Please consider to add a requirements.txt file contains all the dependencies your project has and try again.',
            TextStyle.FAIL), err=True)
    sys.exit(401)
