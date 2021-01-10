import sys
import argparse
import math
import struct

# This is needed to allow argparse to automatically parse hex ints from user input
def autobase_int(x):
    return int(x, 0)

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Convert fixed point numbers to floating point")
    parser.add_argument('-b', '--bits', action='store', type=int, default=32,
                        help="The number of bits of the fixed point number. Must be multiple of 8 times a power of 2, max 64")
    parser.add_argument('-f', '--frac', action='store', type=int, default=16,
                        help="The number of bits representing the fractional part of the fixed point number.  Default 16")
    parser.add_argument('-s', '--signed', action='store_true', default=False, help='Used signed integers')
    parser.add_argument('number', action='store',type=autobase_int, help='The number to convert, using standard base notation')
    return parser.parse_args(argv)

def main(argv):
    # Strip out the script name before parsing the arguments
    arg_vals = parse_args(argv[1:])
    # Grab the fixed point parameters
    given = arg_vals.number
    num_bits=arg_vals.bits
    num_frac=arg_vals.frac

    print(f'Given Val: {given:#0{num_bits//4+2}x}')
    print(f'Given Val(dec): {given:d}')
    print(f'Floating pt: {given/2**num_frac:f}')

if __name__ == "__main__":
    main(sys.argv)
