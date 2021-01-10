import sys
import argparse
import math
import struct

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Convert floating point to fixed point numbers")
    parser.add_argument('-b', '--bits', action='store', type=int, default=32,
                        help="The number of bits of the fixed point number. Must be multiple of 8 times a power of 2, max 64")
    parser.add_argument('-f', '--frac', action='store', type=int, default=16,
                        help="The number of bits representing the fractional part of the fixed point number.  Default 16")
    parser.add_argument('-r', '--show_range', action='store_true', help='Display the valid range of the fixed point number')
    parser.add_argument('-p', '--show_precision', action='store_true', help='Display the precision of the fixed point number')
    parser.add_argument('number', action='store',type=float, help='The number to convert')
    parser.add_argument('-s', '--signed', action='store_true', default=False, help='Used signed integers')
    return parser.parse_args(argv)

def main(argv):
    arg_vals = parse_args(argv[1:])
    given = arg_vals.number
    num_bits=arg_vals.bits
    num_frac=arg_vals.frac
    struct_format='I'
    if num_bits == 8:
        if arg_vals.signed:
            struct_format='b'
        else:
            struct_format='B'
    elif num_bits == 16:
        if arg_vals.signed:
            struct_format='h'
        else:
            struct_format='H'
    elif num_bits == 32:
        if arg_vals.signed:
            struct_format='i'
        else:
            struct_format='I'
    elif num_bits == 64:
        if arg_vals.signed:
            struct_format='l'
        else:
            struct_format='L'
    else:
        print("Invalid bit length")
        sys.exit(1)

    if arg_vals.show_range:
        minval= struct.pack(struct_format,
                            0 if not arg_vals.signed else int.from_bytes((b'\x80' + (b'\x00'*(num_bits//8-1))),
                                                                        byteorder='big', signed=True))
        maxval= struct.pack(struct_format,
                            int.from_bytes(b'\xff'*(num_bits//8), byteorder='big', signed=False) if not arg_vals.signed
                            else int.from_bytes(b'\x7f' + (b'\xff'*((num_bits//8)-1)), byteorder='big', signed=True))
        minval=struct.unpack(struct_format, minval)[0]
        maxval=struct.unpack(struct_format, maxval)[0]
        minval = minval/(2**num_frac)
        maxval = maxval/(2**num_frac)
        print(f'Representation range: [{minval:f}, {maxval:f}]')

    if arg_vals.show_precision:
        print(f'Precision: +/- {1/(2**num_frac):f}')

    try:
        fxdpt = struct.pack(struct_format, int(given * 2**num_frac))
    except:
        print(f"Error: {given:f} causes overflow with given fixed point parameters")
        sys.exit(2)

    print(f'Given Val: {given:f}')
    print(f'Fixed point: {struct.unpack(struct_format.upper(),fxdpt)[0]:#0{num_bits//4 + 2:d}x}')
    actualFloat=struct.unpack(struct_format, fxdpt)[0]/(2**num_frac)
    print(f'Actual Val: {actualFloat:f}')
    if given != 0:
        print(f'Representation Error: {(actualFloat - given)/given:%}')
    else:
        print("Cannot calculate error for value of 0")

if __name__ == "__main__":
    main(sys.argv)
