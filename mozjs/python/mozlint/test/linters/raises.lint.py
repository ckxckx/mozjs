# -*- Mode: python; indent-tabs-mode: nil; tab-width: 40 -*-
# vim: set filetype=python:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mozlint.errors import LintException


def lint(files, **lintargs):
    raise LintException("Oh no something bad happened!")


LINTER = {
    'name': "RaisesLinter",
    'description': "Raises an exception",
    'type': 'external',
    'payload': lint,
}
