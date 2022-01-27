from __future__ import absolute_import

import os
import re
import subprocess
import sys
from subprocess import CalledProcessError

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext
from sciunit2.exceptions import CommandLineError, MalformedExecutionId
from sciunit2.util import quoted_format
from sciunit2.workspace import _mkdir_p
from sciunit2.workspace import at

from getopt import getopt


def find_env_path(log_file, pkg_home_dir):
    """Retrieve the environment path from the log file"""
    with open(log_file) as f:
        line = f.readline()
        found = False
        while line:
            if not found and not line.startswith('#'):
                splits = line.split(' ')
                if len(splits) >= 5:
                    python_path = splits[4]
                    found = True
                    continue
            if "site-packages" in line:
                path_portion = line.split(" ")[-1].strip()
                env_path = "/".join(path_portion.split("/")[:-2])
                env_path = pkg_home_dir + env_path
                if any(os.scandir(pkg_home_dir+path_portion)):
                    return env_path, python_path
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
    # Get the python version
    py_version = None
    for part in site_packages.split('/'):
        if "python" in part:
            py_version = part.split("python")[-1]
            break

    # Get the packages
    try:
        if site_packages:
            packages = [dir_ for dir_ in os.listdir(site_packages)
                        if ".dist-info" in dir_ or ".egg-info" in dir_]
            # if no dist-info or egg-info found,
            # then the python packages are in separate directories.
            pkg_list = []
            if not packages:
                packages = []
                package_paths = []
                # read package dirs
                for (dirpath, dirnames, filenames) in os.walk(site_packages):
                    for dirname in dirnames:
                        if dirname == '__pycache__':
                            continue
                        package_path = os.path.join(dirpath, dirname)
                        if any(os.scandir(package_path)):
                            package_paths.append(package_path)
                            packages.append(dirname)
                    break

                version_list = []
                # find the package versions from the __init__.py, version.py,
                # __version__.py, etc. files
                for package_path in package_paths:
                    for (dirpath, dirnames, filenames) in os.walk(package_path):
                        version_file = None
                        version = None
                        version_file_list = list(filter(lambda file: 'version' in file, filenames))
                        if version_file_list:
                            version_file = version_file_list[0]
                        else:
                            #  check for version detail in __init__.py
                            if '__init__.py' in filenames:
                                version_file = '__init__.py'
                        if version_file:
                            # extract version number from the file
                            with open(os.path.join(dirpath, version_file)) as f:
                                lines = f.readlines()
                                for line in lines:
                                    version_line_list = re.findall(r'^_*version_*\s*=', line)
                                    if version_line_list:
                                        version_split = line.split('=')
                                        if version_split and len(version_split) >= 2:
                                            version = version_split[1].strip()
                                            version = version.strip('"').strip('\'')
                                            version = str(version)
                                            # check if its a number
                                            if not version[:1].isdigit():
                                                version = None
                        version_list.append(version)
                        break
                pkg_list = zip(packages, version_list)
            else:
                for package in packages:
                    pkg_list.append(package_version(package))

            return py_version, pkg_list
    except Exception:
        return None

    return None


def package_version(package):
    """Split the package from the version"""
    pkg, ver = package.split("-")[:2]
    if "dist" in ver:
        ver = ".".join(ver.split(".")[:-1])
    return pkg, ver


def write_requirements_file(py_version, pkgs, filename="requirements.txt"):
    """Write the requirements.txt file"""
    with open(filename, "w") as f:
        f.write("# for python version: {0}\n".format(py_version))
        pkg_str = ''
        for pkg, ver in pkgs:
            version = ''
            if ver:
                version = '==' + ver
            f.write(pkg+version + '\n')
            pkg_str += pkg+version + ' '
    return pkg_str


# this class exports the dependencies of an execution
# and stores them in a requirements.txt file
class ExportCommand(AbstractCommand):
    name = 'export'

    # export can be called as:
    # sciunit export e1 [virtualenv]
    # where e1 is the mandatory execution id
    # if argument virtualenv is given, create
    # requirements.txt file and use it to instantiate
    # a new virtual environment in virtualenv,
    # install all Python dependencies in it.
    @property
    def usage(self):
        return [('export <execution id> [virtualenv]',
                 'Exports the dependencies of <execution id> into requirements.txt.\n'
                 'Optionally creates new virtualenv instance and '
                 'installs all dependencies in it.\n')]

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) < 1:
            raise CommandLineError
        eid = args[0]
        # check if eid is of the form en
        # i.e., a valid execution id format
        if not re.match(r'^e[1-9]\d*$', eid):
            raise MalformedExecutionId
        create_venv = False
        if len(args) == 2:
            create_venv = True

        # checkout execution
        with CheckoutContext(eid) as (pkg_dir, orig):
            # find environment path from log file
            log_file = "provenance.cde-root.1.log"
            log_file_path = pkg_dir + "/" + log_file
            pkg_home_dir = pkg_dir + "/cde-root"
            env_path, python_path = find_env_path(log_file_path, pkg_home_dir)
            if env_path is None:
                print('Aborting export! Environment path not found')
                return None
            # todo: probably combine this with find_env_path
            site_package_dir = get_dist_info_path(env_path)

            # find packages
            py_version, pkg_list = get_packages(site_package_dir)
            # write requirements file
            if pkg_list is not None:
                req_file = eid + "-requirements.txt"
                pkg_str = write_requirements_file(py_version, pkg_list, req_file)
                if create_venv:
                    # 1. install virtualenv using pip(assuming pip is installed)
                    try:
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                                               '--user', 'virtualenv'])
                    except CalledProcessError as err:
                        print(err.stderr)
                        print('Aborting export! Error installing virtualenv')
                        return None
                    # 2. create new environment using virtualenv and
                    # install all Python dependencies in it
                    env_name = 'sciunit_env'
                    retcode = 0
                    retcode ^= subprocess.check_call(['virtualenv', '-p', python_path, env_name])
                    retcode ^= subprocess.check_call('source ' + env_name + '/bin/activate',
                                                     shell=True, executable='/bin/bash')
                    if retcode == 0:
                        python_path = env_name + '/bin/python'
                        cmd = 'cat ' + req_file + ' | xargs -n 1 ' + python_path + ' -m pip install'
                        subprocess.call(cmd, shell=True, executable='/bin/bash')
                        print('Installed relevant Python packages.')
                    else:
                        print('Aborting export! Error installing dependencies')
                        return None
                    if retcode == 0:
                        print("New virtual environment '" + env_name + "' successfully " +
                              "created with the required dependencies.")
                    else:
                        print('Aborting export!')
                        return None
                    # 3. create new folder in cwd and bring all code+data
                    # in /home/<user> there
                    project_dir = at()
                    project_name = project_dir.split('/')[-1]
                    home_dir = project_dir + '/cde-package/cde-root/home/'
                    user_name = os.listdir(home_dir)[0]
                    user_dir = os.path.join(home_dir, user_name)
                    user_dir += '/*'
                    data_dir = project_name + '-' + eid
                    _mkdir_p(data_dir)
                    subprocess.call('cp -r ' + user_dir + ' ' + data_dir, shell=True)
                    print('You are all set. You can activate the new '
                          'virtual environment as follows:\n'
                          '\tsource ' + env_name + '/bin/activate')
                    print('Your code and data have been copied to the dir: '
                          + project_name + '\n')
                    print('To deactivate the environment, enter: deactivate')
            else:
                print('Export not successful!')
                return None

        return eid

    def note(self, eid):
        return quoted_format('Exported dependencies of {0} into {0}-requirements.txt \n', eid)
