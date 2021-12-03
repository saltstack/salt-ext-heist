# Copyright 2021 VMware, Inc.
# SPDX-License: Apache-2
"""
Heist runner for deploying and managing artifacts
"""
import asyncio
import logging

try:
    import pop.hub

    HAS_REQS = True
except ImportError:
    HAS_REQS = False


import salt.utils.platform

log = logging.getLogger(__name__)

__virtualname__ = "heist"


def __virtual__():
    if HAS_REQS:
        return __virtualname__
    return (
        False,
        "The heist module could not be imported. Requires the pop and heist module",
    )


def create_hub(project, subs=None, sub_dirs=None, confs=None):
    """
    Create a hub with specified pop project ready to go and completely loaded
    """
    if "{}.hub".format(project) not in __context__:
        log.debug("Creating the POP hub")
        hub = pop.hub.Hub()

        log.debug("Initializing the loop")
        hub.pop.loop.create()

        log.debug("Loading subs onto hub")
        hub.pop.sub.add(dyne_name=project)
        if subs:
            for sub in subs:
                hub.pop.sub.add(dyne_name=sub)

        if sub_dirs:
            for sub_dir in sub_dirs:
                hub.pop.sub.load_subdirs(getattr(hub, sub_dir), recurse=True)

        if confs:
            hub.pop.sub.add(dyne_name="config")
            hub.pop.config.load(confs, project, parse_cli=False, logs=False)

        __context__["{}.hub".format(project)] = hub

    return __context__["{}.hub".format(project)]


def heist_hub(sub=None):
    """
    Create the pop hub for heist
    """
    subs = ["acct", "artifact", "rend", "roster", "service", "tunnel"]
    if sub:
        subs.append(sub)
    sub_dirs = ["heist", "service"]
    confs = ["heist", "acct"]
    hub = create_hub("heist", subs=subs, sub_dirs=sub_dirs, confs=confs)
    return hub


def deploy(
    manager,
    artifact_version=None,
    roster_file=None,
    roster=None,
    roster_data=None,
    sub=None,
    **kwargs
):
    """
    Deploy the heist artifact
    :depends: heist, heist_salt, pop, asyncio

    **Arguments**

    manager

        The name of the heist manager or artifact to deploy to the target.

    artifact_version

        The version of the artifact to use.

    roster_file

        Path to the roster file heist will use

    roster

        The type of heist roster to use. For example: flat, scan, fernet, clustershell

    roster_data

        Pass json data to be used for the roster data

    sub

        Additional subs to load onto the hub

    CLI Example:

    .. code-block:: bash

        salt-run heist.deploy salt.minion

        salt-run heist.deploy salt.minion roster_file=/tmp/roster_file
    """
    hub = heist_hub(sub)
    hub.heist.init.env()
    if not salt.utils.platform.is_windows():
        try:
            hub.pop.loop.start(
                hub.heist.init.run_remotes(
                    manager,
                    artifact_version=artifact_version or hub.OPT.heist.artifact_version,
                    roster_file=roster_file or hub.OPT.heist.roster_file,
                    roster=roster or hub.OPT.heist.roster,
                    roster_data=roster_data or hub.OPT.heist.roster_data,
                    **kwargs
                ),
                sigint=hub.heist.init.clean,
                sigterm=hub.heist.init.clean,
            )
        except asyncio.CancelledError:
            hub.log.debug("Cancelled remaining running asyncio tasks")
        finally:
            hub.pop.Loop.close()
    else:
        hub.pop.loop.create()
        try:
            hub.pop.Loop.run_until_complete(
                hub.heist.init.run_remotes(
                    manager,
                    artifact_version=artifact_version or hub.OPT.heist.artifact_version,
                    roster_file=roster_file or hub.OPT.heist.roster_file,
                    roster=roster or hub.OPT.heist.roster,
                    roster_data=roster_data or hub.OPT.heist.roster_data,
                    **kwargs
                )
            )
        except KeyboardInterrupt:
            hub.log.debug("Caught keyboard interrupt")
        finally:
            hub.pop.Loop.run_until_complete(hub.heist.init.clean())
            hub.pop.Loop.close()
