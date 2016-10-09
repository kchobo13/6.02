import numpy, sys

from channel import ChannelEncoder, ChannelDecoder

'''
A linear block encoder is just one type of channel encoder; we'll look
at another in PS3.
'''
class BlockEncoder(ChannelEncoder):

    def __init__(self):
        super(BlockEncoder, self).__init__()

    '''
    Here, you should implement the linear encoder.  This requires
    the following steps:

    1. Calculate the G matrix
    2. Break the message into k-length blocks
    3. Use G to determine the codewords for each block
    4. Concatenate the codewords into a single array and return it

    The input, bits, will be a numpy array of integers (each integer
    is 0 or 1).
    '''
    def encode(self, A, bits):
        #Calculate the G matrix
        k = len(A)
        identity = numpy.identity(k, int)
        G = numpy.concatenate((identity,A), axis=1)

        #Break the message into k-length blocks
        bits_array = bits.reshape((int(len(bits)/k),k))


        #Use g to determine the codewords for each blocks
        encoded_bits = []
        for k_bit in bits_array:
            encoded_bits = numpy.concatenate((encoded_bits, numpy.mod(k_bit.dot(G),2)))

        #change all floats to int in array
        encoded_bits = encoded_bits.astype(int)
        return encoded_bits

class SyndromeDecoder(ChannelDecoder):

    def __init__(self):
        super(ChannelDecoder, self).__init__()

    '''
    Here you should implement the syndrome decoder.  This requires the
    following steps:

    1. Calculate the H matrix
    2. Use H to set up the syndrome table
    3. Break the message into n-length codewords
    4. For each codeword, calculate the error bits
    5. If the error bits are nonzero, use the syndrome table to correct the error.
    6. Return the corrected bitstring

    Please set up the syndrome table before you perform the decoding
    (feel free to set up a different function to do this).  This will
    result in a more organized design, and also a more efficient
    decoding procedure (because you won't be recalculating the
    syndrome table for each codeword).
    '''
    def decode(self, A, bits):
        #Calculate the H matrix
        k = len(A.T)
        identity = numpy.identity(k, int)
        H = numpy.concatenate((A.T, identity), axis=1)
        syndrome_iden = numpy.identity(len(H.T), int)

        #syndrome table
        table = {}
        for i in range(len(syndrome_iden)):
            s = numpy.mod(H.dot(syndrome_iden[i].T),2)
            string = ''
            for j in s:
                string = string + str(j)
            table[string] = syndrome_iden[i]

        #Break the message into n-length blocks
        decoded = []
        bits_array = bits.reshape((int(len(bits)/len(H.T)),len(H.T)))

        for code in bits_array:
            s = numpy.mod(H.dot(code.T),2)
            if 1 in s:
                string = ''
                for j in s:
                    string = string + str(j)

                error = table[string]
                code = numpy.mod(code+error,2)
            decoded = numpy.concatenate((decoded, code[:k+1]))
        return decoded.astype(int)
