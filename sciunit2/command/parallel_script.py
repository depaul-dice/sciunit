import sys
import json
#from sciunit2.command import AbstractCommand
#from sciunit2.command.context import CheckoutContext
#from sciunit2.exceptions import CommandLineError
import sciunit2.core
if len(sys.argv) != 3:
    print("Usage: python my_script.py pkgdir arg_list repeat_args")
    sys.exit(1)

pkgdir = sys.argv[1]
arg_list = json.loads(sys.argv[2])

sciunit2.core.repeat(pkgdir, arg_list,[])