import argparse
import numpy as np
import pyperclip as pyclip
from codecs import encode, decode
from lib import *
from prs import *
from PIL import Image

def manage_file(filename, row_data: bytearray, mode, encoding):
    """
    reads file/writes to file. Returns nothing or data depending on situation
    
    filename - if %CLIP% writes to clipboard, otherwise requires filename
    row_data - data to be written to the file, empty on r mode 
    modes    - 'r' read, returns data from file, 
               'w' write, returns nothing
    encoding - encoding
    """
    if filename != "%CLIP%":
        match mode:
            case 'r':
                pure_data = bytearray()
                with open(data_src, 'r', encoding = encoding) as raw_data:
                    for line in raw_data.readlines():
                        pure_data += bytearray(encode(line, encoding))
                return pure_data
            case 'w':
                with open(data_dest, 'w+', encoding=encoding) as dfile:
                    dfile.write(decode(row_data, encoding))
            case _: 
                raise ValueError
    else:
        match mode:
            case 'r':
                return encode(pyclip.paste(),encoding)
            case 'w':
                pyclip.copy(decode(row_data,encoding))
            case _:
                raise ValueError
    
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
    
    # with open(data_dest, 'w+', encoding=encoding) as dfile:
        # dfile.write(decode(dump, encoding))
   
    manage_file(data_dest, dump, 'w', encoding)
    
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
    # pure_data = bytearray()
    # with open(data_src, 'r', encoding = encoding) as raw_data:
        # for line in raw_data.readlines():
            # pure_data += bytearray(encode(line, encoding))
    pure_data = manage_file(data_src, "", 'r',encoding)
    
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
    parser.add_argument('-d', help="data file for message encoding/decoding I/O. Use %CLIP% to use data from clipboard/copy to clipboard", required=True)
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