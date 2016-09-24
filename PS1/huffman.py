import heapq, operator, random, sys

from collections import defaultdict

from source import SourceEncoder, SourceDecoder
from bitstring import BitString

class HuffmanTree:

    # Huffman Trees always have a probability.  For internal nodes,
    # symbol will be None, and left and right children will be
    # defined.  For leaf nodes, symbol will *not* be None, but the
    # children will be.
    def __init__(self, symbol, probability):
        self.left_child = None
        self.right_child = None
        self.probability = probability
        self.symbol = symbol

    # "less than" method, for sorting trees
    def __lt__(self, other):
        return self.probability < other.probability

    @staticmethod
    def build_codebook(probabilities):

        # Degenerate case: only one symbol to encode
        if len(probabilities) == 1:
            return {list(probabilities.keys())[0] : "0"}

        # Convert the list of symbols into a min-heap that sorts
        # HuffmanTrees instead of (symbol, probability) tuples
        min_heap = []
        for symbol in probabilities:
            h = HuffmanTree(symbol, probabilities[symbol])
            min_heap.append(h)
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            # Take the two smallest elements out
            a = heapq.heappop(min_heap)
            b = heapq.heappop(min_heap)

            # Create a new Huffman tree out of the two smallest elements
            c = HuffmanTree(None, a.probability + b.probability)
            c.left_child = a
            c.right_child = b
            heapq.heappush(min_heap, c)

        # Return the codebook
        return min_heap[0].codebook()

    def codebook(self, current_bitstring=""):
        # If we're at a leaf, return our symbol
        if self.left_child == None:
            book = {}
            book[self.symbol] = current_bitstring
        # Else, walk down the tree.  Zeros on the left, ones on the right
        else:
            book = self.left_child.codebook(current_bitstring + "0")
            book1 = self.right_child.codebook(current_bitstring + "1")
            book.update(book1) # Merge the two dictionaries into one book
        return book

class HuffmanEncoder(SourceEncoder):

    def __init__(self):
        super(HuffmanEncoder, self).__init__()
        self.decoder = None
        self.codebook = None

    # Set the source
    def set_source_probabilities(self, src_string=None, src_probs=None, src_list=None):
        super(HuffmanEncoder, self).set_source_probabilities(src_string=src_string, src_probs=src_probs, src_list=src_list)
        self.transmit_probabilities()
        self.codebook = HuffmanTree.build_codebook(self.source_probabilities)

    # Transmit the probabilities to the receiver
    def transmit_probabilities(self):
        self.decoder.receive_probabilities(self.source_probabilities)

    # Encode some data based on the previously-set source
    def encode(self, data):
        b = BitString()
        for c in data:
            b.pack_bitstring(self.codebook[c])
        return b

class HuffmanDecoder(SourceDecoder):

    def __init__(self):
        super(HuffmanDecoder, self).__init__()
        self.codebook = None

    # Get the source probabilities from the transmitter and create the tree
    def receive_probabilities(self, probabilities):
        self.source_probabilities = probabilities
        codebook = HuffmanTree.build_codebook(self.source_probabilities)
        self.reverse_codebook = {codebook[c] : c for c in codebook}

    # Decode an encoded string based on the existing tree
    def decode(self, b):
        encoded_bits = b.unpack_bitstring(len(b))
        output = ""
        j = ""
        for i in encoded_bits:
            j += str(i)
            if j in self.reverse_codebook:
                output += self.reverse_codebook[j]
                j = ""
        return output
