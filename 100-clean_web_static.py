#!/usr/bin/python3
""" Cleans up outdated web_static archives and directories """

from fabric.api import *

env.hosts = ["100.25.119.2", "100.25.136.71"]
env.user = "ubuntu"


def do_clean(number=0):
    """
    Cleans up outdated web_static archives and directories.

    Args:
        number (int): The number of archives to keep, including the most recent.

    Notes:
        If number is 0 or 1, only the most recent version of the archive is kept.
        If number is 2, the most recent and second most recent versions are kept, and so on.
    """
    number = int(number)
    if number < 1:
        number = 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm {{}}".format(number))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number))
