# Build Instructions

## Overview

The Sciunit management suite, _sciunit2_, is a software package written in
Python 2.7 and shipped along with multiple binary executables that target
Linux.  _Sciunit2_ builds these executables automatically as a part of a
standard Python project build process.  If all end-users' machines are equipped
with suitable toolchains, we can ship a Python source distribution to PyPI and
users can simply _pip_-install it.  However, this situation is unlikely.  The
official _sciunit2_ build produces Python Wheel (`.whl`) packages, compiled
with the _devtoolset-4_ toolchain on CentOS 7.  The packages don't qualify for
the `manylinux1_x86_64` ABI but are branded as such.  For performance and
security concerns, the official build does not target CentOS 6.  Therefore, if
you are still on an old CentOS/RHEL-based distro, you will need to build
_sciunit2_ manually.

## Flow

The following instructions use Red Hat Enterprise Linux Server release 6.5
(Santiago) as an example and explain the differences between RHEL and CentOS
6/7.

### Step 1: Install [Devtoolset-4](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-4/)

First, enable the SCL repository.  Look at the output of

    sudo yum repolist all

and find a repository with the string "rhscl" in its name.  In my case, its
called "rhui-REGION-rhel-server-rhscl"; in your case, it might be
"rhel-server-rhscl-6-rpms."  Assume it's the latter, execute

    sudo yum-config-manager --enable rhel-server-rhscl-6-rpms

to enable it.  If you are not able to identify the SCL repo, go to

  https://access.redhat.com/solutions/472793

and get a feeling about how messy the RHEL product line is, then give them a
call.

If you are on CentOS, then it's as simple as

    sudo yum install -y centos-release-scl

After enabling the SCL repository, do

    sudo yum install -y devtoolset-4-gcc-c++

### Step 2: Install CMake 3

First, enable the EPEL repository:

    sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

On CentOS, it's

    sudo yum install epel-release

Now install cmake3 and link it to cmake:

    sudo yum install -y cmake3
    sudo ln -s /usr/bin/cmake3 /usr/bin/cmake

### Step 3: Install Python's [virtualenv](https://virtualenv.pypa.io/en/stable/)

    sudo yum install -y python27-python-virtualenv

On CentOS 7 and RHEL 7, where Python defaults to 2.7, just do

    sudo yum install -y python-virtualenv

### Step 4: Get _sciunit2_ source code

If you don't have Git, then

    sudo yum install -y git

Go to a directory, get our code, and `cd` into it

    git clone https://bitbucket.org/geotrust/sciunit2
    cd sciunit2

### Step 5: Activate SCL environment

    scl enable devtoolset-4 python27 bash

Again, if you are on CentOS 7 or RHEL 7, just

    scl enable devtoolset-4 bash

### Step 6: Start a virtualenv

    virtualenv venv
    . venv/bin/activate

And don't forget to upgrade the environment

    pip install -U pip setuptools wheel

### Step 7: Build

    python setup.py bdist_wheel

This takes time, but not longer than what our continuous integration system
does to every one of the commits we pushed to the master branch, so feel free
to

    git pull

and build a new version at any time.

The build will be placed under the *dist* directory:

    $ ls dist/
    sciunit2-0.2.post4.dev128624984-py2-none-any.whl

By default it's unbranded.  You can specify a platform tag with the
`--plat-name` option, or read more materials before doing
that[^pep425][^pep513].

That's it.  Time to try out your Sciunit suite by _pip_-installing the package!

  [^pep425]: https://www.python.org/dev/peps/pep-0425/
  [^pep513]: https://www.python.org/dev/peps/pep-0513/
