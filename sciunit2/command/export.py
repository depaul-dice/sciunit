from __future__ import absolute_import

import os
import re

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext
from sciunit2.exceptions import CommandLineError, MalformedExecutionId
from sciunit2.util import quoted_format

from getopt import getopt


def find_env_path(log_file):
    """Retrieve the environment path from the log file"""
    with open(log_file) as f:
        line = f.readline()
        while line:
            if "site-packages" in line:
                path_portion = line.split(" ")[-1]
                env_path = "/".join(path_portion.split("/")[:-2])
                return env_path
            line = f.readline()
        return None


def get_dist_info_path(env_path):
    """Retrieve the site-package directory"""
    for dir_ in os.listdir(env_path):
        path = os.path.join(env_path, dir_)
        if "python" in dir_ and os.path.isdir(path):
            python_path = path

            for sub_dir in os.listdir(python_path):
                if "site-packages" in sub_dir:
                    # Found the environment
                    return os.path.join(python_path, sub_dir)


def get_packages(site_packages):
    """Retrieve a list of virtualenv packages from the site-packages directory"""
    # # Get the python version
    # py_version = None
    # for part in site_packages.split('/'):
    #     if "python" in part:
    #         py_version = part.split("python")[-1]
    #         print("version: " + py_version)
    #         break

    # Get the packages
    try:
        if site_packages:
            packages = [dir_ for dir_ in os.listdir(site_packages)
                        if ".dist-info" in dir_ or ".egg-info" in dir_]
            pgk_list = []
            for package in packages:
                pgk_list.append(package_version(package))

            return pgk_list
    except Exception:
        return None

    return None


def package_version(package):
    """Split the package from the version"""
    pkg, ver = package.split("-")[:2]
    if "dist" in ver:
        ver = ".".join(ver.split(".")[:-1])
    return pkg, ver


def write_requirements_file(pkgs, filename="requirements.txt"):
    """Write the requirements.txt file"""
    with open(filename, "w") as f:
        for pkg, v in pkgs:
            f.write(pkg + "==" + v + "\n")


# this class exports the dependencies of an execution
# and stores them in a requirements.txt file
class ExportCommand(AbstractCommand):
    name = 'export'

    @property
    def usage(self):
        return [('export <execution id>',
                 'Exports the dependencies of <execution id> into requirements.txt')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) != 1:
            raise CommandLineError
        eid = args[0]
        # check if eid is of the form en
        # i.e., a valid execution id format
        if not re.match(r'^e[1-9]\d*$', eid):
            raise MalformedExecutionId

        # checkout execution
        with CheckoutContext(eid) as (pkg_dir, orig):
            # find environment path from log file
            log_file = "provenance.cde-root.1.log"
            log_file_path = pkg_dir + "/" + log_file
            env_path = find_env_path(log_file_path)
            if env_path is not None:
                env_path = pkg_dir + "/cde-root" + env_path
            site_package_dir = get_dist_info_path(env_path)

            # find packages
            pkg_list = get_packages(site_package_dir)
            # write requirements file
            if pkg_list is not None:
                write_requirements_file(pkg_list, eid+"-requirements.txt")
            else:
                return None

        return eid

    def note(self, eid):
        return quoted_format('Exported dependencies of {0} into requirements.txt \n', eid)
