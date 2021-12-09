# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
"""
    Unit tests for the salt.runners.heist_salt module
"""
from unittest.mock import call
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import saltext.heist.runners.heist as heist
import saltext.heist.runners.heist_salt as heist_salt

pytest.importorskip("pop", reason="Test requires pop to be installed")
pytest.importorskip("heist", reason="Test requires heist to be installed")


@pytest.fixture
def configure_loader_modules():
    return {
        heist: {"__context__": {}},
        heist_salt: {"__salt__": {"heist.deploy": heist.deploy}},
    }


def test_heist_salt_deploy(pop_hub):
    """
    test heist salt deploy runner
    """
    mock_run = Mock(return_value=True)
    patch_platform = patch("salt.utils.platform.is_windows", return_value=False)
    patch_heist_hub = patch.object(heist, "create_hub", return_value=pop_hub)
    patch_init = patch.object(pop_hub.heist.init, "run_remotes", mock_run)
    patch_loop = patch.object(pop_hub.pop.loop, "start", return_value=True)

    with patch_platform, patch_heist_hub, patch_init, patch_loop:
        heist_salt.deploy()
        assert mock_run.call_args_list == [
            call(
                "salt.minion",
                artifact_version="",
                roster=None,
                roster_data=None,
                roster_file="/etc/heist/roster",
            )
        ]


def test_heist_salt_deploy_args(pop_hub):
    """
    test heist_salt deploy runner when an
    args (roster_file) is passed.
    """
    mock_run = Mock(return_value=True)
    roster_file = "/tmp/testrosterfile"
    patch_platform = patch("salt.utils.platform.is_windows", return_value=False)
    patch_heist_hub = patch.object(heist, "create_hub", return_value=pop_hub)
    patch_init = patch.object(pop_hub.heist.init, "run_remotes", mock_run)
    patch_loop = patch.object(pop_hub.pop.loop, "start", return_value=True)

    with patch_platform, patch_heist_hub, patch_init, patch_loop:
        heist_salt.deploy(roster_file=roster_file)
        assert mock_run.call_args_list == [
            call(
                "salt.minion",
                artifact_version="",
                roster=None,
                roster_data=None,
                roster_file=roster_file,
            )
        ]
