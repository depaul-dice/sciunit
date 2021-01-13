import logging
import sciunit2.workspace
from sciunit2.exceptions import CommandError
import os

logger = logging.getLogger('sciunit')
hdlr = logging.FileHandler(os.path.expanduser('~/sciunit/sciunit.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def getpath(file):
    if "sciunit2/" in file:
        return file[file.find("sciunit2/"):]
    else:
        return file[file.find("tests/"):]  # for testing


def runlog(level, command, message, file):
    file = getpath(file)
    try:
        if level == 'WARNING':
            logger.warning("{0} {1} {2} {3}".format(
                sciunit2.workspace.at(1), command, message, file))
        elif level == 'ERROR':
            logger.error("{0} {1} {2} {3}".format(
                sciunit2.workspace.at(1), command, message, file))
        elif level == 'INFO':
            logger.info("{0} {1} {2} {3}".format(
                sciunit2.workspace.at(1), command, message, file))
        return 0
    except CommandError: #if sciunit not open
        return runlogat(level, command, message, file)


def runlogat(level, command, message, file):
    if level == 'WARNING':
        logger.warning("{0} {1} {2}".format(command, message, file))
    elif level == 'ERROR':
        logger.error("{0} {1} {2}".format(command, message, file))
    elif level == 'INFO':
        logger.info("{0} {1} {2}".format(command, message, file))
    return 1
