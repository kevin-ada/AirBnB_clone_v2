#!/usr/bin/python3
""" Deploys a web_static archive to web servers """

from fabric.api import put, run, env, local
import os
from datetime import datetime
import tarfile

env.hosts = ["100.25.119.2", "100.25.136.71"]
env.user = "ubuntu"


def do_pack():
    """
    Creates a web_static archive.

    Returns:
        Path to the created archive if successful, None otherwise.
    """
    savedir = "versions/"
    filename = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    with tarfile.open(savedir + filename, "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))
    if os.path.exists(savedir + filename):
        return savedir + filename
    else:
        return None


def do_deploy(archive_path):
    """
    Deploys a web_static archive to the web servers.

    Args:
        archive_path (str): Path to the web_static archive.

    Returns:
        True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    results = []

    res = put(archive_path, "/tmp")
    results.append(res.succeeded)

    basename = os.path.basename(archive_path)
    if basename[-4:] == ".tgz":
        name = basename[:-4]
    newdir = "/data/web_static/releases/" + name
    run("mkdir -p " + newdir)
    run("tar -xzf /tmp/" + basename + " -C " + newdir)

    run("rm /tmp/" + basename)
    run("mv " + newdir + "/web_static/* " + newdir)
    run("rm -rf " + newdir + "/web_static")
    run("rm -rf /data/web_static/current")
    run("ln -s " + newdir + " /data/web_static/current")

    return True


def deploy():
    """
    Deploys a web_static archive to the web servers.

    Calls the do_pack function to create a web_static archive,
    then deploys the archive using do_deploy.

    Returns:
        True if deployment is successful, False otherwise.
    """
    tar = do_pack()
    if not tar:
        return False
    return do_deploy(tar)
