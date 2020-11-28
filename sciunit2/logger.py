import logging
import sciunit2.workspace
from sciunit2.exceptions import CommandLineError, CommandError
import os

logger = logging.getLogger('sciunit')
hdlr = logging.FileHandler(os.path.expanduser('~/sciunit/sciunit.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def runlog(level, command, message, file):
    try:
        if level == 'warning':
            logger.warning("{0} {1} {2} {3}".format(sciunit2.workspace.at(), command, message, file))
        elif level == 'error':
            logger.error("{0} {1} {2} {3}".format(sciunit2.workspace.at(), command, message, file))
        else:
            logger.info("{0} {1} {2} {3}".format(sciunit2.workspace.at(), command, message, file))
    except CommandError:
        runlogat(level, command, message, file)


def runlogat(level, command, message, file):
    if level == 'warning':
        logger.warning("{0} {1} {2}".format(command, message, file))
    elif level == 'error':
        logger.error("{0} {1} {2}".format(command, message, file))
    else:
        logger.info("{0} {1} {2}".format(command, message, file))
