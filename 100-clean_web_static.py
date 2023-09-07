#!/usr/bin/python3
""" Cleans up outdated web_static archives and directories """

from fabric.api import *
import os
from datetime import datetime
import tarfile

env.hosts = ["100.25.119.2", "100.25.136.71"]
env.user = "ubuntu"


def do_clean(number=0):
    """
    Cleans up outdated web_static archives and directories.

    Args:
        number (int): The number of archives to keep, including the most recent

    Notes:
        If number is 0 or 1, only the most recent version of the archive kept
        If number is 2, the most recent and second most recent versions kept
    """
    number = int(number)
    if number < 2:
        number = 1
    number += 1
    number = str(number)
    with lcd("versions"):
        local("ls -1t | grep web_static_.*\.tgz | tail -n +" +
              number + " | xargs -I {} rm -- {}")
    with cd("/data/web_static/releases"):
        run("ls -1t | grep web_static_ | tail -n +" +
            number + " | xargs -I {} rm -rf -- {}")
