#!/usr/bin/python3
"""Deploys an archive to web servers using Fabric."""

from fabric.api import *
import os

# Set the host IP addresses for web-01 and web-02
env.hosts = ['100.25.119.2', '100.25.136.71']
env.user = "ubuntu"

def do_deploy(archive_path):
    """
    Deploys an archive to web servers and updates the web_static content.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory
        res = put(archive_path, "/tmp")

        # Check if upload was successful
        if not res.succeeded:
            return False

        # Extract the archive to a new directory
        basename = archive_path.split("/")[-1]
        name = basename[:-4] if basename.endswith(".tgz") else basename
        newdir = "/data/web_static/releases/" + name
        run("mkdir -p " + newdir)
        run("tar -xzf /tmp/" + basename + " -C " + newdir)

        # Clean up temporary files and update web_static content
        run("rm /tmp/" + basename)
        run("mv " + newdir + "/web_static/* " + newdir)
        run("rm -rf " + newdir + "/web_static")
        run("rm -rf /data/web_static/current")
        run("ln -s " + newdir + " /data/web_static/current")

        return True
    except Exception:
        return False
