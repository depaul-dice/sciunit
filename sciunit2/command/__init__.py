from __future__ import absolute_import

import abc
from abc import abstractmethod, abstractproperty


class AbstractCommand:
    __metaclass__ = abc.ABCMeta

    name = NotImplemented

    @abstractproperty
    def usage(self):
        raise NotImplementedError

    @abstractmethod
    def run(self, args):
        raise NotImplementedError

    def note(self, user_data):
        raise NotImplementedError
