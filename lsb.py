import argparse
import numpy as np
from codecs import encode, decode
from lib import *
from prs import *
from PIL import Image

def extract(image_name, data_dest, verbose=False, encoding=None, prs=False):
    if encoding is None:
        encoding='utf8'
    
    with Image.open(image_name) as img:
        pix = np.array(img)
    
    dump = LSB_get_data(pix, verbose)

    if prs:
        global prs_table
        prs_table = np.transpose(prs_table)
        dump = join_bytearray(dump, prs_table)
    
    with open(data_dest, 'w+', encoding=encoding) as dfile:
        dfile.write(decode(dump, encoding))
    
    if verbose:
        print("Extracting completed.")

def hide(image_name, data_src, verbose=False, encoding=None, output_image_name=None, prs=False):
    if output_image_name is None:
        output_image_name = image_name.split('.')[0] + "_stenographed.bmp"
    if encoding is None:
        encoding = "utf8"
    
    #read image
    with Image.open(image_name) as img:
        pix = np.array(img)
    
    #read data
    pure_data = bytearray()
    with open("data.txt", 'r', encoding = encoding) as raw_data:
        for line in raw_data.readlines():
            pure_data += bytearray(encode(line, encoding))
    
    if prs:
        pure_data = join_bytearray(pure_data, prs_table)

    #hide data
    res = LSB_inject_to_R(pix, pure_data, verbose)
    rimg = Image.fromarray(res)

    rimg.save(output_image_name)
    
    if verbose:
        print("Hiding completed.")


def main():
    parser = argparse.ArgumentParser(
        prog="LSB steganographer(R only)",
        usage="python lsb.py -en -s dest.bmp -d data.txt -o stenographed.bmp",
        description="Hides some data in image (1 bit per pixel)"
    )
    # file encoding
    parser.add_argument("-enc", help="i/o file encoding")
    parser.set_defaults(enc="utf8")
    # mode
    modes_group = parser.add_mutually_exclusive_group(required=True)
    modes_group.add_argument("-en", help="encode mode (default)", action="store_true")
    modes_group.add_argument("-de", help="decode mode", action="store_true")
    # files
    parser.add_argument('-s', help="source image", required=True)
    parser.add_argument('-d', help="data file for encoding/decoding I/O", required=True)
    parser.add_argument('-o', help="output file(for images with message). If not mentioned, stored in (soure image name)_stenographed")
    #verbose
    parser.add_argument('-v', help="verbose", action="store_true")
    
    # data modification
    group = parser.add_argument_group('data concealment')
    # pseudo-random substitution
    group.add_argument('-prs', help="pseudo-random substitution(currently fixed)", action="store_true")

    args = parser.parse_args()

    # -o and -de exclusion
    if args.o is not None and args.de is True:
        parser.error("-de and -o are mutually exclusive")

    if args.de:
        extract(args.s, args.d, args.v, args.enc, prs=args.prs)
    elif args.en:
        hide(args.s, args.d, args.v, args.enc, args.o, prs=args.prs)
    else:
        raise ValueError("Unexpected behaviour. You should choose -de or -en to make it work as intended")
    pass


def extract_test(image_name, data_dest, verbose=False, encoding=None, prs=False):
    if encoding is None:
        encoding='utf8'
    
    with Image.open(image_name) as img:
        pix = np.array(img)
    
    dump = LSB_get_data(pix, verbose)

    if prs:
        np.transpose(prs_table)
        dump = join_bytearray(dump, prs_table)
    #print(dump)
    with open(data_dest, 'w+', encoding=encoding) as dfile:
        dfile.write(dump.decode(encoding))
    
    if verbose:
        print("Extracting completed.")

if __name__ == "__main__":
    #extract_test("source_stenographed.bmp", "decod.txt", False, None, prs=True)
    #print(p)
    main()