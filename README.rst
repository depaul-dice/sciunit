.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

==========================
sciunit
==========================
:Author:    Zhihao Yuan <zhihao.yuan@depaul.edu>
:Manual section: 1

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l


SYNOPSIS
==========

``sciunit`` [--version] [--help]
``sciunit`` <command> [<args>]

DESCRIPTION
============

``Sciunit`` is a command line utility to create, manage, and verify
*sciunit* packages.  A *sciunit* package is a lightweight unit to
represent executions of programs.


OPTIONS
========

General Options
--------------------

--version             show program's version number and exit
-h, --help            show help message and exit


Commands
-----------------

``sciunit`` create <project name>
          Create a new project under *~/sciunit/<project name>*
          and use it as the current project.  If the project already
          exists, exit with an error.

``sciunit`` open <project name>|<path to zipped sciunit>
          Set the current project to *~/sciunit/<project name>* if
          the directory exists.  Otherwise, the argument should be
          a path to a sciunit package.  Decompress it to a temporary
          directory and use it as the current project.

``sciunit`` exec <executable> [<args>]
          Package an execution of for the given *executable* with
          the command line arguments *args* without involving a
          shell.  *Executable* and *args* are expended with limited
          features.  The newly created execution is assigned
          execution id "*eN*", where *N* is a monotone increasing
          decimal.
          The first execution created in a project has execution id
          "*e1*".

``sciunit`` sh
          Launch the current user's shell, and create an execution
          given the user's interactions with the shell, which may
          involve multiply commands.  The execution is created after
          the user exits the shell.

``sciunit`` list
          List the existing executions in the current project.

``sciunit`` rm <execution id>
          Remove an existing execution from the current project.  A
          malformed execution id causes an error.  Removing a
          nonexistent execution has no effect.

          Note: the execution is removed from the records, but its
          data preserves.

``sciunit`` repeat <execution id> [<args>]
          Checkout the corresponding execution form the current
          project and repeat it.  If *args* presents, use it in place
          of the packaged arguments.

``sciunit`` draft [<service>|update]
          Prepare a publication with the project content.  If the
          *service* argument is not supplied, a list of services
          will be prompted.  The supported services include
          Figshare and Hydroshare.
          If the argument is a keyword "update", update the last
          draft with the latest sciunit data.

``sciunit`` push [<remote>]
          Synchronize a project at a remote server.  The default
          remote server of the current project can be configured
          in *~/sciunit/<project name>/config*.  The remote server
          where this project successfully pushes to will be recorded
          as the default remote server.  The supported remote
          protocols include Globus.

``sciunit`` verify [<execution id>] [<api>]
          Repeat a given execution using sciunit API and verify the
          results.  If *execution id* is not supplied, verify all
          executions in the current project.

``sciunit`` gc
          Shrink the project directory by garbage collecting the
          unreferenced data.


SEE ALSO
=============
