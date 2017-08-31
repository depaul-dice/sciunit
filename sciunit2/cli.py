from __future__ import absolute_import

from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.command.create import CreateCommand
from sciunit2.command.open import OpenCommand

import sys
from getopt import getopt, GetoptError
from cStringIO import StringIO
import pkg_resources

__cmds__ = [CreateCommand, OpenCommand]


def short_usage(out):
    out.write("usage: sciunit [--version] [--help]\n"
              "       sciunit <command> [<args...>]\n")


def subcommand_usage(out, cmds):
    buf = StringIO()
    for cmd in cmds:
        for ln in cmd.usage:
            buf.write("  sciunit %-19s %s\n" % ln)
    out.write(buf.getvalue())


def main():
    try:
        _main(sys.argv[1:])
    except CommandLineError:
        short_usage(sys.stderr)
        sys.exit(2)
    except (CommandError, GetoptError) as exc:
        print >> sys.stderr, "sciunit: %s" % exc[0]
        short_usage(sys.stderr)
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
        for cls in __cmds__:
            if args[0] == cls.name:
                cmd = cls()
                try:
                    cmd.run(args[1:])
                except CommandLineError:
                    subcommand_usage(sys.stderr, [cmd])
                    sys.exit(2)
                except (CommandError, GetoptError) as exc:
                    print >> sys.stderr, "sciunit %s: %s" % (cls.name, exc[0])
                    _exit_given(exc)
                break
        else:
            raise GetoptError('subcommand %r unrecognized' % args[0])
    elif len(optlist) == 1:
        op, _ = optlist[0]
        if op == '--help':
            short_usage(sys.stdout)
            print
            subcommand_usage(sys.stdout, [cls() for cls in __cmds__])
        elif op == '--version':
            print pkg_resources.require("sciunit2")[0]
        else:  # unreachable
            pass
    else:
        raise CommandLineError
