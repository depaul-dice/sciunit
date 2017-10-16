Sciunit
----------

**sciunit** is a command-line tool that answers the call for a
reusable research object that containerizes and stores applications
simply and efficiently, facilitates sharing and collaboration, and
eases the task of executing, understanding, and building on shared
work.

Installing
=============

*[ Note* This section introduces the binary distributions of sciunit.
*--end note ]*

Requires: pip>=8.1.1, glibc>=2.17, python2.7 with headers and compiler

Platform: amd64-pc-linux-gnu

Ensure that `~/.local/bin` is in your ``PATH`` environment variable,
and then, run

::

    pip install --user sciunit2

Add ``--upgrade`` to the command line arguments to upgrade an existing
sciunit installation.

Verify the installation with

::

    sciunit --version

In the following per-distro instructions, if you see a command-line
in the form of

::

    export PATH=~/.local/bin:$PATH

, it merely means that you will need the aforementioned binary path
in ``PATH`` before proceeding; normally you should adjust it according
to your login shell and write it to a shell configuration such as
`~/.profile`.

Ubuntu 16.04
~~~~~~~~~~~~~
::

    sudo apt update
    sudo apt install python-dev python-pip
    pip install --user sciunit2

Ubuntu 14.04
~~~~~~~~~~~~~
::

    sudo apt update
    sudo apt install python-dev python-pip
    pip install --user -U pip
    export PATH=~/.local/bin:$PATH
    pip install --user sciunit2


Arch Linux
~~~~~~~~~~~~~
::

    sudo pacman -S python2-pip
    export PATH=~/.local/bin:$PATH
    pip2 install --user sciunit2

Fedora 26
~~~~~~~~~~~~~
::

    sudo dnf install python2-pip python2-devel gcc redhat-rpm-config
    pip install --user sciunit2

CentOS 7
~~~~~~~~~~~~~
::

    sudo yum install -y epel-release
    sudo yum install python2-pip python-devel gcc
    pip install --user sciunit2

RHEL 7
~~~~~~~~~~~~~
::

    sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    sudo yum install python2-pip python-devel gcc
    pip install --user sciunit2

Debian 9
~~~~~~~~~~~~~
::

    sudo apt update
    sudo apt install python-dev python-pip
    export PATH=~/.local/bin:$PATH
    pip install --user sciunit2

Debian 8
~~~~~~~~~~~~~
::

    sudo apt update
    sudo apt install python-dev python-pip
    pip install --user -U pip
    export PATH=~/.local/bin:$PATH
    pip install --user sciunit2

OpenSUSE 42
~~~~~~~~~~~~~

Note that OpenSUSE defaults user-binary path to `~/bin` rather than
`~/.local/bin`, so you may want to symlink one to the other.

::

    sudo zypper install python-pip python-devel gcc
    pip install --user -U pip
    export PATH=~/.local/bin:$PATH
    pip install --user sciunit2

Using
===========

Checkout our `tutorial <https://sciunit.run/docs/>`_ and manpage.
The manpage is available as

::

    man sciunit

after a successful installation.
