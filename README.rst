.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

==========================
sciunit
==========================
-------------------------------------------------------------
deliver reproducibility in your research
-------------------------------------------------------------
:Author:    Zhihao Yuan <zhihao.yuan@depaul.edu>
:Version:   sciunit2 0.2
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
A *sciunit* is a lightweight and portable unit that contains captured,
repeatable program executions.

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

``sciunit open`` <name>|<token#>|<path to sciunit.zip>
          Open the sciunit under *~/sciunit/<name>* or designated by
          a *token#* obtained from ``sciunit copy``, or one in a
          zipped sciunit package by extracting it to a temporary
          directory.

``sciunit open -m`` <name>
          Rename the currently-opened sciunit to *<name>* and open it.

``sciunit exec`` <executable> [<args...>]
          Capture the execution of the given *executable* with
          the command line arguments *args*.  The newly-created
          execution is added to the
          currently-opened sciunit and assigned execution id "*eN*",
          where *N* is a monotonically-increasing decimal.
          The first execution created in a sciunit has execution id
          "*e1*".

          Note that the command line is launched using `execvp(3)`
          rather than interpreted by a shell.

``sciunit exec -i``
          Launch the current user's shell and capture the user's
          interactions with the shell.  This may involve executing
          multiple commands.  A new execution is created on exiting
          the shell.

``sciunit repeat`` <execution id> [<args...>]
          Repeat the execution of *execution id* from the
          currently-opened sciunit.  If *args* present, use them in
          place of the command line arguments that were present when the
          command was captured with the ``sciunit exec`` command.

``sciunit list``
          List the existing executions in the currently-opened sciunit.

``sciunit show`` [<execution id>]
          Show detailed information about a specific execution (or the
          most recent execution, if no argument present) in the
          currently-opened sciunit.

``sciunit rm`` <execution id>
          Remove an existing execution from the currently-opened
          sciunit.  A malformed execution id causes an error.
          Removing a nonexistent execution has no effect.

          Note: the execution is removed from the records, but its
          data remains and may be shared with other executions.

``sciunit push`` <codename> --setup <service>
          Create an article on a research object sharing *service*
          and attach the currently opened sciunit to the article.
          Assign different *codenames* to track multiple articles or
          multiple versions of an article created from a sciunit.
          The supported services include
          figshare_ (`fs`) and HydroShare_ (`hs`).

``sciunit push`` [<codename>]
          Update the last pushed article with the latest sciunit data
          if no argument present.  Otherwise, update the article
          referred to by *codename*.

``sciunit copy``
          Copy the currently-opened sciunit to
          `file.io <https://file.io/>`_ and obtain a token for
          remotely opening it.  The token is invalidated after being
          accessed or after one day, whichever happens first.

``sciunit copy`` <remote>|<name>
          Copy a sciunit to a *remote* server or *~/sciunit/<name>*.
          The supported remote protocols include Globus_.

``sciunit copy -n``
          Archive the currently-opened sciunit to
          *~/sciunit/<name>.zip*.

``sciunit gc``
          Reduce the currently-opened sciunit's disk usage by
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

SEE ALSO
=============

.. _HydroShare:

HydroShare: https://www.hydroshare.org/

.. _figshare:

figshare: https://figshare.com/

.. _Globus:

Globus: https://www.globus.org/
