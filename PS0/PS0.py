import argparse

from image import Image
from sound import Sound
from text import Text

# Function to count the number of bit errors in two lists.  You can
# assume that
# - Both lists are the same length
# - Every value in each list is either 0.0 or 1.0
#
# This function should return the number of bit errors in the two
# lists.
def count_bit_errors(list1, list2):
    count = 0
    for index in range(len(list1)):
        if list1[index] != list2[index]:
            count += 1
    return count

parser = argparse.ArgumentParser()
parser.add_argument("type", choices=["sound", "image", "text"])
parser.add_argument("data")
parser.add_argument("-d", action="store_true")
parser.add_argument("-n", type=float, default=.001)
args = parser.parse_args()

if args.type == "sound":
    system = Sound(args.n)
    system.set_data(args.data)

elif args.type == "image":
    system = Image(args.n)
    system.set_data(args.data)

else: # text
    system = Text(args.n)
    system.set_data(args.data)
    pass

# Digital representation
if args.d:
    data = system.get_digital_data()
    noisy_data = system.transmit(data)
    noisy_data = system.digitize(noisy_data)
    system.output_digital(noisy_data)
    bit_errors = count_bit_errors(data, noisy_data)
    if bit_errors is not None:
        print("%d bit errors" % bit_errors)
# Analog representation
else:
    data = system.get_analog_data()
    noisy_data = system.transmit(data)
    system.output_analog(noisy_data)
