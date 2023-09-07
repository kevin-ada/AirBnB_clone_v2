#!/usr/bin/python3
""" Deploys an archive to web servers"""

from fabric.api import *
from os.path import isfile

env.hosts = ["100.25.119.2", "100.25.136.71"]
env.user = "ubuntu"


def do_pack():
    """ Generates a .tgz archive from web_static folder """
    time_format = '%Y%m%d%H%M%S'
    archive_path = 'versions/web_static_{}.tgz'.format(
        local('date +"{}"'.format(time_format), capture=True))
    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static'.format(archive_path))
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """ Deploys an archive to web servers """
    if not isfile(archive_path):
        return False

    folder_name = archive_path.split('/')[-1][:-4]

    put(archive_path, "/tmp")
    run("mkdir -p /data/web_static/releases/{}".format(folder_name))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
        .format(archive_path.split('/')[-1], folder_name))
    run("rm /tmp/{}".format(archive_path.split('/')[-1]))
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
        .format(folder_name, folder_name))
    run("rm -rf /data/web_static/releases/{}/web_static".format(folder_name))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(folder_name))
    return True


def deploy():
    """ Deploys an archive to web servers """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
