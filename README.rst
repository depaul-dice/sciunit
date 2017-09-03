.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

==========================
sciunit
==========================
-------------------------------------------------------------
deiliver reproducibility in your research
-------------------------------------------------------------
:Author:    Zhihao Yuan <zhihao.yuan@depaul.edu>
:Version:   sciunit2 0.1
:Manual section: 1
:Copyright: Copyright 2017, DePaul University
:Licence:   FreeBSD License (BSD-2-Clause)

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l


SYNOPSIS
==========

``sciunit`` [--version] [--help]

``sciunit`` <command> [<args...>]

DESCRIPTION
============

A command line utility to create, manage, and share *sciunits*.
A *sciunit* is a lightweight and portable unit to represent
executions of programs.

OPTIONS
========

General Options
--------------------

``--version``         show program's version number and exit

``-h, --help``        show help message and exit


Commands
-----------------

``sciunit create`` <name>
          Create a new sciunit under *~/sciunit/<name>* and open it.
          If the directory already exists, exit with an error.

``sciunit open`` <name>|<path to zipped sciunit>
          Open the sciunit under *~/sciunit/<name>* if the directory
          exists.  Otherwise, the argument should be a path to a zipped
          sciunit package.  Decompress it to a temporary directory and
          open it.

``sciunit exec`` <executable> [<args...>]
          Capture the execution of the given *executable* with
          the command line arguments *args* without involving a
          shell.  The newly created execution is added to the
          currently opened sciunit and assigned execution id "*eN*",
          where *N* is a monotonically-increasing decimal.
          The first execution created in a sciunit has execution id
          "*e1*".

``sciunit exec -i``
          Launch the current user's shell and capture the user's
          interactions with the shell.  This may involve executing
          multiply commands.  A new execution is created on exiting
          the shell.

``sciunit repeat`` <execution id> [<args...>]
          Repeat the execution of *execution id* form the currently
          opened sciunit.  If *args* present, use them in place
          of the command line arguments that was being capture with
          the ``sciunit exec`` command.

``sciunit list``
          List the existing executions in the currently opened sciunit.

``sciunit rm`` <execution id>
          Remove an existing execution from the currently opened
          sciunit.  A malformed execution id causes an error.
          Removing a nonexistent execution has no effect.

          Note: the execution is removed from the records, but its
          data preserves and may be shared with other executions.

``sciunit stage`` [<service>]
          Stage the currently opened sciunit for sharing on *service*.
          If the *service* argument is not supplied, a list of services
          will be prompted.  The supported services include
          Figshare and Hydroshare.

``sciunit stage -u``
          Update the last staged content with the latest sciunit data.

``sciunit copy`` <remote>|<name>
          Copy a sciunit to a *remote* server or *~/sciunit/<name>*.
          The supported remote protocols include Globus.

``sciunit gc``
          Reduce the currently opened sciunit's disk usage by
          garbage-collecting the unreferenced execution data.

``sciunit alias`` <newcmd> <sub...>
          Add a new entry under the ``[alias]`` section in the
          user-wide config file *~/sciunit/config*.  The setting
          enables ``sciunit`` *<newcmd> [<args...>]* to be
          reinterpreted as ``sciunit`` *<sub...> [<args...>]*.

``sciunit ignore`` <path>
          Add a new entry under the ``[ignore]`` section in the
          unit-specific config file *~/sciunit/<name>/config*.
          If the *path* ends with ``/``, exclude any paths prefixed
          with *path* when capturing; otherwise, exclude just *path*.

