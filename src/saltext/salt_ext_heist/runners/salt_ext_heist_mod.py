"""
Salt runner module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "salt_ext_heist"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The salt-ext-heist runner module is not implemented yet")
    return __virtualname__
