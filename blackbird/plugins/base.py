#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Various Base objects"""

import abc
import datetime
import math
import socket
import time

class JobBase(object):
    u"""Based ConcreteJob"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, options, queue, logger):
        self.options = options
        self.queue = queue
        self.logger = logger

    @abc.abstractmethod
    def looped_method(self):
        u"""Called by "Executer".
        This method implemented by derived class
        """
        raise NotImplementedError

class ItemBase(object):
    u"""Base class of the item to be enqueued.
    This class has row value(key, value...and more).
    When it is dequeue, it assemble appropriate format.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, key=None, value=None, host=None, clock=None):
        self.key = key
        self.value = value
        self.host = host
        self.clock = self.__set_timestamp(clock)

    @abc.abstractproperty
    def data(self):
        u"""Dequeued data."""
        raise NotImplementedError

    def _generate(self):
        u"""overrided in each modules."""

        self._data['key'] = self.key
        self._data['value'] = self.value
        self._data['host'] = self.host
        self._data['clock'] = self.clock

    def __set_timestamp(self, clock):
        u"""If "clock" is None, set the time now.
        This function is called self.__init__()
        """
        if clock == None:
            unix_timestamp = time.mktime(datetime.datetime.now().utctimetuple())
            timestamp = int(unix_timestamp)

            return timestamp

        else:
            return clock

class ValidatorBase(object):
    u"""
    Base class of each "plugins/hoge_module"'s Validator.
    options in config file validate.
    e.g: check the validity of the values as follows:
    host -> '127.0.0.1'(IPAddress),
    port -> '11211'(number of 0 - 65535)
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def spec(self):
        u"""
        This property is used when validate config file.
        It's also used when "configspec" object as ConfigObj instance.
        e.g: ConfigObj(infile=ValidatorBase.spec, _inspec=True)

        Thus, this property must be listed configobj's specfiles rules.
        e.g:
        [redis]
        host = ipaddress(default='127.0.0.1')
        port = port(0, 65535, default=6379)

        And, "configspec" as ConfigObj's argument must be
        filelike object(like StringIO or TemporaryFile)
        or a list of lines.

        Notes: 1. List of lines as COnfigObj's argument
        spec = (
            "[redis]",
            "host = string(default='127.0.0.1')",
            "port = integer(0, 6535, default=6379)"
        )

        spec = (
            "[redis]\n",
            "host = string(default='127.0.0.1')\n",
            "port = integer(0, 6535, default=6379)\n"
        )

        Both forms works fine above.

        Notes: 2. List of lines
        when writing to FileType like StringIO object.
        spec = (
            "[redis]\n"
            "host = string(default='127.0.0.1')\n"
            "port = integer(0, 65535, default=6379)\n"
        )

        spec = (
            "[redis]\n",
            "host = string(default='127.0.0.1')\n",
            "port = integer(0, 65535, default=6379)\n"
        )
        
        Both forms works fine above.
        """

        raise NotImplementedError('spec')

    def gethostname(self, addr=None):
        if addr:
            return socket.gethostbyaddr(addr)
        else:
            return socket.gethostname()

class Timer(object):
    """
    TImer Context mansger class.
    Usage:
        with Timer() as timer:
            YOUR_EXECUTE

        print timer.sec
        print timer.msec
    """

    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.sec = self.end - self.start
        self.sec = str(round(self.sec ,4))
        self.msec = self.sec * 1000
        self.msec = str(round(self.msec ,4))