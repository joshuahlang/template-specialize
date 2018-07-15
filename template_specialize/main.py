# Copyright (C) 2017-2018 Craig Hobbs
#
# Licensed under the MIT License
# https://github.com/craigahobbs/template-specialize/blob/master/LICENSE

import argparse
from itertools import chain
import os

try:
    from jinja2 import Template, StrictUndefined
except ImportError:
    pass

from . import __version__ as VERSION
from .environment import Environment


STATUS_UNKNOWN_ENVIRONMENT = 10


def main():

    # Command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('src_path', metavar='SRC', nargs='?',
                        help='the source template file or directory')
    parser.add_argument('dst_path', metavar='DST', nargs='?',
                        help='the destination file or directory')
    parser.add_argument('-c', dest='environment_files', metavar='FILE', action='append',
                        help='the environment files')
    parser.add_argument('-e', dest='environment', metavar='ENV',
                        help='the environment name - return status {0} if unknown environment'.format(STATUS_UNKNOWN_ENVIRONMENT))
    parser.add_argument('--key', action='append', dest='keys', metavar='KEY', default=[],
                        help='add a template key. Must be paired with a template value.')
    parser.add_argument('--value', action='append', dest='values', metavar='VALUE', default=[],
                        help='add a template value. Must be paired with a template key.')
    parser.add_argument('-v', '--version', action='store_true',
                        help='show version number and quit')
    args = parser.parse_args()
    if args.version:
        parser.exit(VERSION)
    if not args.src_path or not args.dst_path:
        parser.error('missing source file/directory and/or destination file/directory')
    if len(args.keys) != len(args.values):
        parser.error('mismatched keys/values')

    # Parse the environment files
    environments = {}
    if args.environment_files:
        for environment_file in args.environment_files:
            with open(environment_file, 'r', encoding='utf-8') as f_environment:
                Environment.parse(f_environment, filename=environment_file, environments=environments)

    # Build the template variables dict
    if args.environment:
        if args.environment not in environments:
            parser.exit(status=STATUS_UNKNOWN_ENVIRONMENT, message='unknown environment "{0}"\n'.format(args.environment))
            extra_variables = [(Environment.parse_key(key), Environment.parse_value(value)) for key, value in zip(args.keys, args.values)]
        template_variables = Environment.asdict(environments, args.environment, extra_values=extra_variables)
    else:
        template_variables = dict(zip(args.keys, args.values))

    # Create the source and destination template file paths
    if os.path.isfile(args.src_path):
        src_files = [args.src_path]
        if args.dst_path.endswith(os.sep):
            dst_files = [os.path.join(args.dst_path, os.path.basename(args.src_path))]
        else:
            dst_files = [args.dst_path]
    else:
        src_files = list(chain.from_iterable((os.path.join(root, file_) for file_ in files) for root, _, files in os.walk(args.src_path)))
        dst_files = [os.path.join(args.dst_path, os.path.relpath(file_, args.src_path)) for file_ in src_files]

    # Process the template files
    for src_file, dst_file in zip(src_files, dst_files):
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        with open(src_file, 'r', encoding='utf-8') as f_from:
            Template(f_from.read(), undefined=StrictUndefined).stream(**template_variables).dump(dst_file, encoding='utf-8')
