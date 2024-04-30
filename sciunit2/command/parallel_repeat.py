from __future__ import absolute_import

from sciunit2.command import AbstractCommand
from sciunit2.command.context import CheckoutContext, CheckoutContext_Parallel
from sciunit2.exceptions import CommandLineError, MalformedExecutionId
import sciunit2.core
import re
from getopt import getopt
import sys
import subprocess
import shlex
import os

class ParallelRepeatCommand(AbstractCommand):
    name = 'parallel_repeat'
    @staticmethod
    def __to_rev(id_):
        return 'e%d' % id_

    @staticmethod
    def __to_id_range(revrange):
        r = re.match(r'^e([1-9]\d*)-e([1-9]\d*)?$', revrange)
        if not r:
            raise MalformedExecutionId
        return tuple(int(x) if x is not None else x for x in r.groups())
    

    @property
    def usage(self):
        return [('parallel_repeat <execution id1>-<execution id2> [<args...>]',
                 "Repeat the execution of <execution id1> to <execution id2>")]
    
    def is_gnu_parallel_installed(self):
        try:
            subprocess.run(['parallel', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError as e:
            return False

    def run(self, args):
        optlist, args = getopt(args, '')
        if len(args) == 0:
            raise CommandLineError

        if not self.is_gnu_parallel_installed():
            print("GNU Parallel is not installed on the machine")
            sys.exit(1)

        
        start,end = self.__to_id_range(args[0])
        pkgdirs = ''
        origs = ''
        for curr in range(start, end+1):
            with CheckoutContext_Parallel(self.__to_rev(curr)) as (pkgdir, orig):
                pkgdirs += '\'' + pkgdir + '\' '
                origs += '\'' +  str(orig).replace("'", '"') + '\' '


        
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parallel_script.py')

        # command = f'parallel --link python {script_path} ::: {pkgdirs} ::: \'["python3", "test.py", "1"]\' \'["python3", "test.py", "2"]\' \'["python3", "test.py", "3"]\''
       
        command = f'parallel --link python {script_path} ::: {pkgdirs} ::: {origs}'

        subprocess.run(command, shell=True, executable='/bin/bash')


        # TODO: Delete all the new directories created
        sys.exit(0)
