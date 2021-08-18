# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
"""
    Unit tests for the salt.runners.heist module
"""
from unittest.mock import call
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import saltext.salt_ext_heist.runners.heist as heist

pytest.importorskip("pop", reason="Test requires pop to be installed")
pytest.importorskip("heist", reason="Test requires heist to be installed")


@pytest.fixture
def configure_loader_modules():
    return {
        heist: {"__context__": {}},
        #        hub: {"__context__": {}},
    }


@pytest.fixture()
def pop_hub():
    """
    Test the hub using the heist project
    """
    return heist.create_hub(
        "heist",
        subs=["acct", "artifact", "rend", "roster", "service", "tunnel"],
        sub_dirs=["heist", "service"],
        confs=["heist", "acct"],
    )


@pytest.mark.parametrize("sub", ["config", "heist"])
def test_subs(sub, pop_hub):
    assert hasattr(pop_hub, sub)


@pytest.mark.parametrize("sub_dir", ["heist", "service"])
def test_sub_dirs(sub_dir, pop_hub):
    assert hasattr(pop_hub, sub_dir)


@pytest.mark.parametrize("conf", ["heist", "acct"])
def test_confs(conf, pop_hub):
    hasattr(pop_hub.OPT, conf)


def test_heist_deploy(pop_hub):
    """
    test heist deploy runner
    """
    mock_run = Mock(return_value=True)
    patch_platform = patch("salt.utils.platform.is_windows", return_value=False)
    patch_heist_hub = patch.object(heist, "create_hub", return_value=pop_hub)
    patch_init = patch.object(pop_hub.heist.init, "run_remotes", mock_run)
    patch_loop = patch.object(pop_hub.pop.loop, "start", return_value=True)

    with patch_platform, patch_heist_hub, patch_init, patch_loop:
        heist.deploy("salt.minion", sub="salt")
        assert mock_run.call_args_list == [
            call(
                "salt.minion",
                artifact_version="",
                roster=None,
                roster_data=None,
                roster_file="",
            )
        ]


def test_heist_deploy_args(pop_hub):
    """
    test heist deploy runner when an
    args (roster_file) is passed.
    """
    mock_run = Mock(return_value=True)
    roster_file = "/tmp/testrosterfile"
    patch_platform = patch("salt.utils.platform.is_windows", return_value=False)
    patch_heist_hub = patch.object(heist, "create_hub", return_value=pop_hub)
    patch_init = patch.object(pop_hub.heist.init, "run_remotes", mock_run)
    patch_loop = patch.object(pop_hub.pop.loop, "start", return_value=True)

    with patch_platform, patch_heist_hub, patch_init, patch_loop:
        heist.deploy("salt.minion", roster_file=roster_file, sub="salt")
        assert mock_run.call_args_list == [
            call(
                "salt.minion",
                artifact_version="",
                roster=None,
                roster_data=None,
                roster_file=roster_file,
            )
        ]
