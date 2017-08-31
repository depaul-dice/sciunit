from __future__ import absolute_import

import abc
from abc import abstractmethod, abstractproperty


class AbstractCommand:
    __metaclass__ = abc.ABCMeta

    name = NotImplemented

    @abstractproperty
    def usage(self):
        pass  # pragma: no cover

    @abstractmethod
    def run(self, args):
        pass  # pragma: no cover
