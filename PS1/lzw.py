import argparse
import array
import random
import sys
import struct

from source import SourceEncoder, SourceDecoder
from bitstring import BitString

class LZWEncoder(SourceEncoder):

    def __init__(self, word_size=16):
        super(LZWEncoder, self).__init__()
        self.word_size = word_size
        self.dictionary = None
        self.initialize_dict()

    def initialize_dict(self):
        # Initialized dictionary.  Maps strings to indexes.
        self.dictionary = {chr(k) : k for k in range(256)}

    def encode(self, message):
        string = message.pop(0)
        code = []
        bitstring = BitString()
        while message:
            symbol = message.pop(0)
            if (string + symbol) in self.dictionary.keys():
                string = string + symbol
            else:
                code.append(self.dictionary[string])
                if len(self.dictionary) >= 2**16:
                    self.initialize_dict()
                self.dictionary[string+symbol] = len(self.dictionary)
                string = symbol
            if len(message) == 0:
                code.append(self.dictionary[string])

        bitstring.pack_numbers(code, 16)
        return bitstring

class LZWDecoder(SourceDecoder):

    def __init__(self, word_size=16):
        super(LZWDecoder, self).__init__()
        self.word_size = word_size
        self.dictionary = None
        self.initialize_dict()

    def initialize_dict(self):
        # Backwards dict for decoders.  Maps indexes to strings.
        self.dictionary = {k : chr(k) for k in range(256)}

    def decode(self, bits):
        numbers = bits.unpack_all_numbers(16)

        code = numbers.pop(0)
        string = self.dictionary[code]
        output = string

        while numbers:
            code = numbers.pop(0)

            if code not in self.dictionary.keys():
                entry = string + string[0]
            else:
                entry = self.dictionary[code]
            output += entry
            if len(self.dictionary) >= 2 ** 16:
                self.initialize_dict()
            self.dictionary[len(self.dictionary)] = string + entry[0]
            string = entry

        return output

if __name__ == "__main__":

    sender = LZWEncoder()
    receiver = LZWDecoder()
    # To use a dictionary with a maximum of 2**9 entries, uncomment
    # out the following lines:
#    sender = LZWEncoder(word_size=9)
#    receiver = LZWDecoder(word_size=9)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='filename to compress or decompress', default='test')
    parser.add_argument('-d', '--decompress', help='decompress file', action='store_true')

    args = parser.parse_args()

    if not args.decompress:
        # read in the file
        f = open(args.filename, 'rb')
        compressed = [chr(k) for k in array.array("B", f.read())]
        f.close()
        # encode and output
        x = sender.encode(compressed)
        new_filename = args.filename + '.encoded'
        x.write_to_file(new_filename)
        print("Saved encoded file as %s" % new_filename)

    else:
        b = BitString()
        b.read_in_file(args.filename)
        x = receiver.decode(b)
        new_filename = args.filename + '.decoded'
        with open(new_filename, "w") as f:
            f.write(x)
        print("Saved decoded file as %s" % new_filename)
