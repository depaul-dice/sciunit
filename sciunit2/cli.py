from __future__ import absolute_import

from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.command.create import CreateCommand
from sciunit2.command.open import OpenCommand

import sys
from getopt import getopt, GetoptError


def short_usage():
    print >> sys.stderr, ("usage: sciunit [--version] [--help]\n"
                          "       sciunit <command> [<args...>]")


def main():
    try:
        _main(sys.argv[1:])
    except CommandLineError:
        short_usage()
        sys.exit(2)
    except (CommandError, GetoptError) as exc:
        print >> sys.stderr, "sciunit: %s" % exc[0]
        short_usage()
        _exit_given(exc)
    except EnvironmentError as exc:
        if hasattr(exc, 'filename') and exc.filename is not None:
            print >> sys.stderr, "sciunit: %s: %s" % (exc.filename,
                                                      exc.strerror)
        else:  # pragma: no cover
            print >> sys.stderr, "sciunit: %s" % exc.strerror
        sys.exit(1)


def _exit_given(exc):
    sys.exit(1 if isinstance(exc, CommandError) else 2)


def _main(args):
    optlist, args = getopt(args, '', ['help', 'version'])
    if not optlist and args:
        for cls in [CreateCommand, OpenCommand]:
            if args[0] == cls.name:
                cmd = cls()
                try:
                    cmd.run(args[1:])
                except CommandLineError:
                    for ln in cmd.usage:
                        print >> sys.stderr, "  sciunit %-19s %s" % ln
                    sys.exit(2)
                except (CommandError, GetoptError) as exc:
                    print >> sys.stderr, "sciunit %s: %s" % (cls.name, exc[0])
                    _exit_given(exc)
                break
        else:
            raise GetoptError('subcommand %r unrecognized' % args[0])
    elif len(optlist) == 1:
        pass
    else:
        raise CommandLineError()
