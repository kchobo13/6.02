import sys

import image

from huffman import HuffmanEncoder, HuffmanDecoder

'''
This file runs the Huffman experiments for the first task.
'''

if __name__ == "__main__":


    filename = "PS1_fax_image.png"

    encoder = HuffmanEncoder()
    decoder = HuffmanDecoder()
    encoder.decoder = decoder

    # 1. Individual bits
    bits = image.get_bits_from_bitmap(filename)
    num_bits = len(bits)
    print("Encoding 1: Individual bits")
    print("   %d bits" % num_bits)


    # 2. Fixed-length runs
    runs = image.get_run_lengths(filename, fixed_length=True)
    if len(runs) % 2 != 0:
        runs.append(0)
    num_bits = len(runs) * 8
    print("Encoding 2: Fixed-length runs")
    print("   %d runs" % len(runs))
    print("   %d bits" % num_bits)


    # 3. Huffman-encoded runs
    encoder.set_source_probabilities(src_list=runs)
    s = encoder.encode(runs)
    print("Encoding 3: Huffman-encoded runs\n   %d bits" % len(s))

    # Get the probability of each run length
    run_probs = image.get_run_probabilities(runs)
    print("   Top 10 run lengths [probability]:")
    for i in range(10):
        print("      %d [%2.2f]" % (run_probs[i][0], run_probs[i][1]))


    # 4. Huffman-encoded runs, separate colors
    white_runs = [runs[i] for i in range(len(runs)) if i % 2 == 0]
    black_runs = [runs[i] for i in range(len(runs)) if i % 2 == 1]
    encoder.set_source_probabilities(src_list=white_runs)
    white_string = encoder.encode(white_runs)
    encoder.set_source_probabilities(src_list=black_runs)
    black_string = encoder.encode(black_runs)
    print("Encoding 4: Huffman-encoded runs by color\n   %d bits" % (len(white_string) + len(black_string)))


    # Get the probabilities of the run lengths
    white_run_probs = image.get_run_probabilities(white_runs)
    print("   Top 10 white run lengths [probability]:")
    for i in range(10):
        print("      %d [%2.2f]" % (white_run_probs[i][0], white_run_probs[i][1]))
    black_run_probs = image.get_run_probabilities(black_runs)
    print("   Top 10 black run lengths [probability]:")
    for i in range(10):
        print("      %d [%2.2f]" % (black_run_probs[i][0], black_run_probs[i][1]))


    # 5. Huffman-encoded runs, allow pairs
    paired_runs = [(runs[i], runs[i+1]) for i in range(0, len(runs), 2)]
    encoder.set_source_probabilities(src_list=paired_runs)
    s = encoder.encode(paired_runs)
    print("Encoding 5: Huffman-encoded run pairs\n   %d bits" % len(s))


    # Get the probabilities
    run_probs = image.get_run_probabilities(paired_runs)
    print("   Top 10 run lengths [probability]:")
    for i in range(10):
        print("      %s [%2.2f]" % (run_probs[i][0], run_probs[i][1]))


    # 6. Huffman-encoded blocks
    blocks = image.get_image_blocks(filename)
    encoder.set_source_probabilities(src_list=blocks)
    s = encoder.encode(blocks)
    print("Encoding 6: Huffman-encoded 4x4 image blocks\n   %d bits" % len(s))

    # Get the probabilities
    run_probs = image.get_run_probabilities(blocks)
    print("   Top 10 4x4 blocks [probability]:")
    for i in range(10):
        print("      %s [%2.2f]" % (hex(run_probs[i][0])[:-1], run_probs[i][1]))


    # 7. Run-length encoding on a different image
    runs_v = image.get_run_lengths("PS1_voyager.png", fixed_length=True)
    if len(runs) % 2 != 0:
        runs_v.append(0)

    # For any run lengths that don't exist, we'll assume a probability
    # of zero.
    encoder.set_source_probabilities(src_list=runs)
    p = encoder.source_probabilities
    for i in range(0, 256):
        if i not in p:
            p[i] = 0.0
    encoder.set_source_probabilities(src_probs=p)

    s = encoder.encode(runs_v)
    print("Final experiment: Huffman-encoded runs on a different image")
    print("   Using probabilities calculated from previous image: %d bits" % len(s))

    encoder.set_source_probabilities(src_list=runs_v)
    s = encoder.encode(runs_v)
    print("   Using probabilities calculated from source image: %d bits" % len(s))
