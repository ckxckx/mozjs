# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Combined with build/autoconf/config.status.m4, ConfigStatus is an almost
# drop-in replacement for autoconf 2.13's config.status, with features
# borrowed from autoconf > 2.5, and additional features.

from __future__ import absolute_import, print_function

import logging
import os
import subprocess
import sys
import time

from argparse import ArgumentParser

from mach.logging import LoggingManager
from mozbuild.backend.configenvironment import ConfigEnvironment
from mozbuild.base import MachCommandConditions
from mozbuild.frontend.emitter import TreeMetadataEmitter
from mozbuild.frontend.reader import BuildReader
from mozbuild.mozinfo import write_mozinfo
from itertools import chain

from mozbuild.backend import (
    backends,
    get_backend_class,
)


log_manager = LoggingManager()


ANDROID_IDE_ADVERTISEMENT = '''
=============
ADVERTISEMENT

You are building Firefox for Android. After your build completes, you can open
the top source directory in IntelliJ or Android Studio directly and build using
Gradle.  See the documentation at

https://developer.mozilla.org/en-US/docs/Simple_Firefox_for_Android_build

PLEASE BE AWARE THAT GRADLE AND INTELLIJ/ANDROID STUDIO SUPPORT IS EXPERIMENTAL.
You should verify any changes using |mach build|.
=============
'''.strip()

VISUAL_STUDIO_ADVERTISEMENT = '''
===============================
Visual Studio Support Available

You are building Firefox on Windows. You can generate Visual Studio
files by running:

   mach build-backend --backend=VisualStudio

===============================
'''.strip()


def config_status(topobjdir='.', topsrcdir='.', defines=None,
                  non_global_defines=None, substs=None, source=None,
                  mozconfig=None, args=sys.argv[1:]):
    '''Main function, providing config.status functionality.

    Contrary to config.status, it doesn't use CONFIG_FILES or CONFIG_HEADERS
    variables.

    Without the -n option, this program acts as config.status and considers
    the current directory as the top object directory, even when config.status
    is in a different directory. It will, however, treat the directory
    containing config.status as the top object directory with the -n option.

    The options to this function are passed when creating the
    ConfigEnvironment. These lists, as well as the actual wrapper script
    around this function, are meant to be generated by configure.
    See build/autoconf/config.status.m4.
    '''

    if 'CONFIG_FILES' in os.environ:
        raise Exception('Using the CONFIG_FILES environment variable is not '
            'supported.')
    if 'CONFIG_HEADERS' in os.environ:
        raise Exception('Using the CONFIG_HEADERS environment variable is not '
            'supported.')

    if not os.path.isabs(topsrcdir):
        raise Exception('topsrcdir must be defined as an absolute directory: '
            '%s' % topsrcdir)

    default_backends = ['RecursiveMake']
    default_backends = (substs or {}).get('BUILD_BACKENDS', ['RecursiveMake'])

    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='display verbose output')
    parser.add_argument('-n', dest='not_topobjdir', action='store_true',
                        help='do not consider current directory as top object directory')
    parser.add_argument('-d', '--diff', action='store_true',
                        help='print diffs of changed files.')
    parser.add_argument('-b', '--backend', nargs='+', choices=sorted(backends),
                        default=default_backends,
                        help='what backend to build (default: %s).' %
                        ' '.join(default_backends))
    parser.add_argument('--dry-run', action='store_true',
                        help='do everything except writing files out.')
    options = parser.parse_args(args)

    # Without -n, the current directory is meant to be the top object directory
    if not options.not_topobjdir:
        topobjdir = os.path.abspath('.')

    env = ConfigEnvironment(topsrcdir, topobjdir, defines=defines,
            non_global_defines=non_global_defines, substs=substs,
            source=source, mozconfig=mozconfig)

    # mozinfo.json only needs written if configure changes and configure always
    # passes this environment variable.
    if 'WRITE_MOZINFO' in os.environ:
        write_mozinfo(os.path.join(topobjdir, 'mozinfo.json'), env, os.environ)

    cpu_start = time.clock()
    time_start = time.time()

    # Make appropriate backend instances, defaulting to RecursiveMakeBackend,
    # or what is in BUILD_BACKENDS.
    selected_backends = [get_backend_class(b)(env) for b in options.backend]

    if options.dry_run:
        for b in selected_backends:
            b.dry_run = True

    reader = BuildReader(env)
    emitter = TreeMetadataEmitter(env)
    # This won't actually do anything because of the magic of generators.
    definitions = emitter.emit(reader.read_topsrcdir())

    log_level = logging.DEBUG if options.verbose else logging.INFO
    log_manager.add_terminal_logging(level=log_level)
    log_manager.enable_unstructured()

    print('Reticulating splines...', file=sys.stderr)
    if len(selected_backends) > 1:
        definitions = list(definitions)

    for the_backend in selected_backends:
        the_backend.consume(definitions)

    execution_time = 0.0
    for obj in chain((reader, emitter), selected_backends):
        summary = obj.summary()
        print(summary, file=sys.stderr)
        execution_time += summary.execution_time
        if hasattr(obj, 'gyp_summary'):
            summary = obj.gyp_summary()
            print(summary, file=sys.stderr)

    cpu_time = time.clock() - cpu_start
    wall_time = time.time() - time_start
    efficiency = cpu_time / wall_time if wall_time else 100
    untracked = wall_time - execution_time

    print(
        'Total wall time: {:.2f}s; CPU time: {:.2f}s; Efficiency: '
        '{:.0%}; Untracked: {:.2f}s'.format(
            wall_time, cpu_time, efficiency, untracked),
        file=sys.stderr
    )

    if options.diff:
        for the_backend in selected_backends:
            for path, diff in sorted(the_backend.file_diffs.items()):
                print('\n'.join(diff))

    # Advertise Visual Studio if appropriate.
    if os.name == 'nt' and 'VisualStudio' not in options.backend:
        print(VISUAL_STUDIO_ADVERTISEMENT)

    # Advertise Android Studio if it is appropriate.
    if MachCommandConditions.is_android(env):
        print(ANDROID_IDE_ADVERTISEMENT)
