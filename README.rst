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
represent an execution of a program.


OPTIONS
========

General Options
--------------------

--version             Show program's version number and exit
-h, --help            Show help message and exit


Commands
-----------------

``sciunit`` init
          Initialize the current working directory to a *sciunit*
          project directory.  The project directory will contain a
          *.sciunit* directory.  If the current working directory
          has already been initialized, do nothing.

``sciunit`` create <executable> [<args>]
          Package an execution of for the given *executable* with
          the command line arguments *args* without involving a
          shell.  *Executable* and *args* are expended with limited
          features.  The newly created package is assigned package
          id "*pN*", where *N* is a monotone increasing decimal.
          The first package created in a project has package id "p1".

``sciunit`` sh
          Launch the current user's shell, and create a package given
          the user's interactions with the shell, which may contain
          executing multiply commands.  The package is created after
          the user exits the shell.

``sciunit`` list
          List the existing packages in the current project.

``sciunit`` rm <package id>
          Remove an existing package from the current project.  A
          malformed package id causes an error.  Removing a
          nonexistent package has no effect.

          Note: the package is removed from the records, but its data
          preserves.

``sciunit`` repeat <package id>|<path to zipped package>
          If *package id* is well-formed, checkout the corresponding
          package form the current project and repeat its execution.
          Otherwise, the argument is a path to a zipped package.
          Unzip the package and repeat its execution.

``sciunit`` draft [<service>]
          Prepare a publication with the project content.  If the
          *service* argument is not supplied, a list of services
          will be prompted.  The supported services include
          Figshare and Hydroshare.

``sciunit`` push [<remote>]
          Synchronize a project at a remote server.  The default
          remote server of the current project can be configured
          in *.sciunit/config*.  The remote server where this
          project successfully pushes to will be recorded as the
          default remote server.  The supported remote protocols
          include Globus.

``sciunit`` gc
          Shrink the project directory by garbage collecting the
          unreferenced data.


SEE ALSO
=============
