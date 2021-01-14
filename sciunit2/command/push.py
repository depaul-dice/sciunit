from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError, CommandError
from sciunit2.sharing import NotAuthorized, NotFound
from sciunit2.sharing.terminal import TerminalWizard
from sciunit2.sharing.hydroshare import HydroShare
import sciunit2.sharing.article
import sciunit2.credentials
import sciunit2.workspace
import sciunit2.logger

from getopt import gnu_getopt


class PushCommand(AbstractCommand):
    name = 'push'

    __srv = {'hs': HydroShare, HydroShare.name: HydroShare}

    @property
    def usage(self):
        return [('push <codename> --setup ' + '|'.join(self.__srv.keys()),
                 'Push the sciunit to a web service by creating an article '
                 'and save it as <codename> for later use'),
                ('push [<codename>] [--file <filename>]',
                 'Update an article with the latest sciunit data')]

    def run(self, args):
        optlist, args = gnu_getopt(args, '', ['setup=', 'file='])
        setup = '--setup' in dict(optlist)
        if setup and not args or len(args) > 1 or len(optlist) > 1:
            sciunit2.logger.runlog("ERROR", "push",
                                   "CommandLineError: unexpected arguments", __file__)
            raise CommandLineError

        emgr, repo = sciunit2.workspace.current()
        if args:
            article = sciunit2.sharing.article.of(repo.location, args[0])
        else:
            article = sciunit2.sharing.article.most_recent(repo.location)
        if setup:
            srvname = optlist[0][1].lower()
        else:
            try:
                srvname = article.service
            except NotFound as exc:
                sciunit2.logger.runlog(
                    "error", "push", "CommandError: NotFound", __file__)
                raise CommandError(exc)

        try:
            srvcls = self.__srv[srvname]
        except KeyError:
            sciunit2.logger.runlog("ERROR", "push",
                                   "CommandError: unrecognized service %r" % srvname, __file__)
            raise CommandError('unrecognized service %r' % srvname)
        else:
            srv = srvcls(sciunit2.credentials.for_(srvcls.name),
                         TerminalWizard())

        with emgr.shared():
            try:
                if setup:
                    article.service = srvcls.name
                    srv.setup(article)
                if setup or not optlist:
                    fn = sciunit2.archiver.make(repo.location)
                else:  # file
                    fn = optlist[0][1]
                srv.push(article, fn)
                sciunit2.sharing.article.save_recent(repo.location, article)
            except (NotAuthorized, NotFound) as exc:
                sciunit2.logger.runlog("ERROR", "push",
                                       "CommandError: error with article", __file__)
                raise CommandError(exc)

        datatuple = (article, sciunit2.workspace.at())
        return datatuple

    def note(self, data):
        return "pushed sciunit {0} to sharing service {1} with id {2}\n".\
            format(data[1], data[0].service, data[0].id)
