#!/usr/bin/python3
"""
This module provides a function to creat a .tgz archive from web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create a .tgz archive from the web_static folder.

    Returns:
        str: The path to the created archive if successful, None otherwise.
    """
    try:
        now = datetime.now()
        date_time_str = now.strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_name = "web_static_" + date_time_str + ".tgz"
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None
