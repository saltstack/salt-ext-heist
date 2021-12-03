# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
import os

import pytest
from saltext.heist import PACKAGE_ROOT
from saltfactories.utils import random_string


@pytest.fixture(scope="session")
def salt_factories_config():
    """
    Return a dictionary with the keyworkd arguments for FactoriesManager
    """
    return {
        "code_dir": str(PACKAGE_ROOT),
        "inject_coverage": "COVERAGE_PROCESS_START" in os.environ,
        "inject_sitecustomize": "COVERAGE_PROCESS_START" in os.environ,
        "start_timeout": 120 if os.environ.get("CI") else 60,
    }


@pytest.fixture(autouse=True)
def set_heist_config(tmp_path):
    """
    Create the heist config file.
    """
    heist_conf = tmp_path / "heist_config"
    heist_conf.touch(exist_ok=True)
    os.environ["HEIST_CONFIG"] = str(heist_conf)
    return heist_conf


@pytest.fixture(scope="package")
def master(salt_factories):
    return salt_factories.get_salt_master_daemon(random_string("master-"))


@pytest.fixture(scope="package")
def minion(master):
    return master.get_salt_minion_daemon(random_string("minion-"))
