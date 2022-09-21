# pseudo-random susbtitution
import numpy as np
from copy import copy
from random import shuffle

prs_table = [
 [0, 0, 0, 0, 0, 1, 0, 0],    
 [0, 0, 1, 0, 0, 0, 0, 0],     
 [0, 0, 0, 0, 0, 0, 1, 0],     
 [1, 0, 0, 0, 0, 0, 0, 0],     
 [0, 0, 0, 0, 0, 0, 0, 1], 
 [0, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 0, 0, 0]]

'''
Highest digit is on the highest index for easy work with matrixes
'''

def matrix_to_mask(p):
    '''
    transforms logical matrix to array of single-bit(!) integers
    [[0, 0, 0, 0, 0, 1, 0, 0],    [8
     [0, 0, 1, 0, 0, 0, 0, 0],     32
     [0, 0, 0, 0, 0, 0, 1, 0],     2
     [1, 0, 0, 0, 0, 0, 0, 0],     64
     [0, 0, 0, 0, 0, 0, 0, 1], ->  128
     [0, 1, 0, 0, 0, 0, 0, 0],     1
     [0, 0, 0, 1, 0, 0, 0, 0],     4
     [0, 0, 0, 0, 1, 0, 0, 0]]     16]
    
    p - logical matrix
    '''
    res = []
    p = np.rot90(p,3)
    for i in p:
        res.append(array_to_integer(i))
    return res

def array_to_integer(arr, b=False):
    '''
    converts array of bits to an integer
    [0,0,0,0,0,1,1,1] -> 7
    
    arr - array of bits
    '''
    if b:
        return np.packbits(arr, bitorder='big')[0]
    else:
        return np.packbits(arr, bitorder='little')[0]
        

def join(arr, matr):
    '''
    sums an integer with aray of integers (matrix conjunction)
    71, [4, 32, 2, 128, 1, 64, 16, 8] -> 172
    0b01000111, [0b100, 0b100000, 0b10, 0b10000000, 0b1, 0b1000000, 0b10000, 0b1000] -> 0b10101100
    
    arr - integer
    matr - logical matrix(array of integers)
    '''
    res = 0
    mask = 1 << (len(matr)-1)
    
    for i in range(len(matr)):
        if arr & matr[i]:
            res |= mask
        mask >>= 1
    return res
    pass

'''
join alias
'''
def join_single(db, p):
    '''
    join function alias
    allows to pass raw matrixes without additional preparations.
    
    db - data block
    p  - logic matrix
    '''
    pt = copy(p)
    pt = matrix_to_mask(pt)
    if isinstance(db, type([])) or isinstance(db,np.ndarray):
        db = array_to_integer(db,True)
    return join(db, pt)

def join_bytearray(data:bytearray,p):
    '''
    encodes binary data array
    '''
    pt = copy(p)
    pt = matrix_to_mask(pt)
    result = bytearray()
    
    for i in range(len(data)):
        result += join(data[i], pt).to_bytes(1, 'big')
    return result