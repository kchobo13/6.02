#!/usr/bin/python

import warnings

from collections import defaultdict

'''
Generic classes for source encoders and decoders.
'''

class SourceEncoder:

    def __init__(self):
        self.source_probabilities = {}

    # Set the source probabilities either by calculating them from the
    # source directly (src_string), by calculating them from a list of
    # characters (src_list), or from a previously-created dictionary
    # of probabilities (src_probs).
    def set_source_probabilities(self, src_string=None, src_probs=None, src_list=None):
        self.source_probabilities = {}
        if src_string is not None:
            self.set_probabilities_from_iterable(src_string)
        elif src_probs is not None:
            self.source_probabilities = src_probs
        elif src_list is not None:
            self.set_probabilities_from_iterable(src_list)
        else:
            warnings.warn("Tried to set source with unknown source type")
            self.source_set = False

    def set_probabilities_from_iterable(self, string):
        # Get a mapping of symbols -> number of occurrences in the string
        symbol_frequencies = defaultdict(int)
        for symbol in string:
            symbol_frequencies[symbol] += 1

        # Change frequencies to probabilities
        for symbol in symbol_frequencies:
            self.source_probabilities[symbol] = symbol_frequencies[symbol]/float(len(string))

    def encode(self, message):
        raise NotImplementedError


class SourceDecoder:

    def __init__(self):
        self.source_probabilities = {}
        self.source_set = False

    def decode(self, encoded_bits):
        raise NotImplementedError

