from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.exceptions import CommandLineError, MalformedExecutionId
from sciunit2.util import quoted
from sciunit2 import timestamp
import sciunit2.workspace
import re

from getopt import getopt


class RmCommand(AbstractCommand):
    name = 'rm'

    @property
    def usage(self):
        return [('rm <execution id>', 'Remove an execution from the sciunit'),
                ('rm eN-[M]', 'Remove executions ranging from eN to eM')]

    @staticmethod
    def __to_rev(id_):
        return 'e%d' % id_

    @staticmethod
    def __to_get_current_missing(ids):
        list_ids = []
        for i in ids:
            list_ids.append(int(i.replace('e', '')))
        list_ids.sort()
        return [x for x in range(list_ids[0], list_ids[-1] + 1) if x not in list_ids]

    @staticmethod
    def __to_id_range(revrange):
        r = re.match(r'^e([1-9]\d*)-([1-9]\d*)?$', revrange)
        if not r:
            raise MalformedExecutionId
        return tuple(int(x) if x is not None else x for x in r.groups())

    def run(self, args):
        ids = []
        optlist, args = getopt(args, '')
        if len(args) != 1:
            raise CommandLineError
        emgr, repo = sciunit2.workspace.current()
        with emgr.exclusive():
            # try:
            #     for rev in emgr.deletemany(args[0]):
            #         repo.unlink(rev)
            #
            # except MalformedExecutionId:
            #     emgr.delete(args[0])
            #     repo.unlink(args[0])
            try:
                if args[0].endswith('-'):
                    arg = args[0] + str(emgr.get_last_id())

                else:
                    arg = args[0]

                for rev, d in emgr.list():
                    ids.append(rev)

                id_bound = self.__to_id_range(arg)

                for i in id_bound:
                    ids.append('e' + str(i))

                ids = self.__to_get_current_missing(ids)
                for i in ids:
                    repo.unlink(self.__to_rev(i))

                emgr.deletemany(arg)
                # TODO: see if deletemany could return bounds
                bounds = self.__to_id_range(arg)

                for _id in range(bounds[0], bounds[1]+1):
                    repo.unlink(self.__to_rev(_id))

            except MalformedExecutionId:
                emgr.delete(arg)
                repo.unlink(arg)
