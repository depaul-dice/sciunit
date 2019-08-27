from __future__ import absolute_import

import abc
from abc import abstractmethod, abstractproperty


class NotAuthorized(Exception):
    @property
    def message(self):
        return str(self[0])


class NotFound(Exception):
    @property
    def message(self):
        return str(self[0])


class AbstractWizard:
    __metaclass__ = abc.ABCMeta

    @abstractmethod
    def ask(self, msg, *args):
        raise NotImplementedError

    @abstractmethod
    def prompt(self, msg, *args):
        raise NotImplementedError

    @abstractmethod
    def info(self, msg, *args):
        raise NotImplementedError

    @abstractmethod
    def progress(self, msg, nbytes):
        raise NotImplementedError


class AbstractService:
    __metaclass__ = abc.ABCMeta

    name = NotImplemented

    @abstractmethod
    def __init__(self, tokenp, wizard):
        raise NotImplementedError

    @abstractmethod
    def setup(self, article):
        raise NotImplementedError

    @abstractmethod
    def push(self, article, fn):
        raise NotImplementedError
