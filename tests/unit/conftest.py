# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
import pytest
import saltext.heist.runners.heist as heist


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
