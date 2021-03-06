#!/usr/bin/env python2
"""Command to build a DXR instance from one or more source trees"""

from optparse import OptionParser
import os.path
from os.path import isdir
from sys import exit, stderr

from dxr.build import build_instance


def main():
    parser = OptionParser(
        usage='usage: %prog [options] [folder containing dxr.config | config '
              'file]',
        description='If no args are given, defaults to looking for a config '
                    'file called dxr.config in the current working directory.')
    parser.add_option('-f', '--file', dest='config_file',
                      help='A DXR config file. [Deprecated. Use the first '
                           'positional arg instead.]')
    parser.add_option('-t', '--tree', dest='tree',
                      help='An INI section title in the config file, '
                           'specifying a source tree to build. (Default: all '
                           'trees.)')
    parser.add_option('-j', '--jobs', dest='jobs',
                      type='int',
                      default=None,
                      help='Number of parallel processes to use, (Default: the'
                           ' value of nb_jobs in the config file)')
    parser.add_option('-v', '--verbose', dest='verbose',
                      action='store_true', default=False,
                      help='Display the build logs during the build instead of'
                           ' only on error.')
    options, args = parser.parse_args()
    if len(args) > 1:
        parser.print_usage()

    if args:
        # Handle deprecated --file arg:
        if options.config_file:
            print >> stderr, ('Warning: overriding the --file or -f flag with '
                              'the first positional argument.')
        options.config_file = (os.path.join(args[0], 'dxr.config') if
                               isdir(args[0]) else args[0])
    elif not options.config_file:
        # Assume dxr.config in the cwd:
        options.config_file = 'dxr.config'

    return build_instance(options.config_file,
                          nb_jobs=options.jobs,
                          tree=options.tree,
                          verbose=options.verbose)


if __name__ == '__main__':
    main()
