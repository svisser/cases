# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from metacomm.combinatorics.all_pairs2 import all_pairs2 as allpairs
from itertools import izip, izip_longest
import random
import json


class Case(object):
    def __repr__(self):
        return json.dumps({key: value for key, value in self.__dict__.iteritems() \
                           if value is not None})


class Cases(object):

    def __init__(self):
        self._CasesClass = Case

    def get_one(self, cls=None, **kwargs):
        """Returns a one case."""
        case = cls() if cls else self._CasesClass()
        for attr, value in kwargs.iteritems():
            setattr(case, attr, value)
        return case

    def get_each_choice(self, cls=None, **kwargs):
        """Returns a generator that generates positive cases by
        "each choice" algorithm.
        """
        defaults = {attr: kwargs[attr][0] for attr in kwargs}
        for set_of_values in izip_longest(*kwargs.values()):
            case = cls() if cls else self._CasesClass()
            for attr, value in izip(kwargs.keys(), set_of_values):
                if value is None:
                    value = defaults[attr]
                setattr(case, attr, value)
            yield case

    def get_pairwise(self, cls=None, **kwargs):
        """Returns a generator that generates positive cases by
        "pairwise" algorithm.
        """
        for set_of_values in allpairs(kwargs.values()):
            case = cls() if cls else self._CasesClass()
            for attr, value in izip(kwargs.keys(), set_of_values):
                setattr(case, attr, value)
            yield case

    def get_negative(self, cls=None, **kwargs):
        """Returns a generator that generates negative cases by
        "each negative value in separate case" algorithm.
        """
        for attr, set_of_values in kwargs.iteritems():
            defaults = {key: kwargs[key][-1]["default"] for key in kwargs}
            defaults.pop(attr)
            for value in set_of_values[:-1]:
                case = cls() if cls else self._CasesClass()
                setattr(case, attr, value)
                for key in defaults:
                    setattr(case, key, defaults[key])
                yield case

    def get_mix_gen(self, sample):
        """Returns function that returns sequence of characters of a
        given length from a given sample
        """
        def mix(length):
            result = "".join(random.choice(sample) for _ in xrange(length)).strip()
            if len(result) == length:
                return result
            return mix(length)
        return mix