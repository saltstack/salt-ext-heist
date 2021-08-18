# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
"""
Define the required entry-points functions in order for Salt to know
what and from where it should load this extension's loaders
"""
from . import PACKAGE_ROOT


def get_runner_dirs():
    """
    Return a list of paths from where salt should load runner modules
    """
    return [str(PACKAGE_ROOT / "runners")]
