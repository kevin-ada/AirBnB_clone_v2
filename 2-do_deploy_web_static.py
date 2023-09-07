#!/usr/bin/python3
"""
Distributes an archive to web servers using Fabric.
"""

from fabric.api import run, put, env
from os.path import exists

# Set the host IP addresses for web-01 and web-02
env.hosts = ['100.25.119.2', '100.25.136.71']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        folder_name = archive_name.split(".")[0]

        put(archive_path, "/tmp/")

        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))

        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_name, folder_name))

        run("rm /tmp/{}".format(archive_name))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(folder_name))

        return True
    except Exception:
        return False
