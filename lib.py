import numpy as np

def LSB_inject_to_R(src : np.array, data : bytearray, verbose : bool = False):
    '''
    Injects data to src.
    Returns modified src (numpy arrayed image pixels)
    '''
    
    if not isinstance(src, np.ndarray):
        raise TypeError('passed non-numpy array '+str(type(src)))
    elif not isinstance(src[1], np.ndarray):
        raise TypeError('passed non-numpy array (sub)')
    if not isinstance(data, bytearray):
        raise TypeError('data must be bytearray')
    if len(src[0][0]) != 3:
        raise TypeError('passed src array data is not pixels')
    if(len(src)*len(src[1]) < len(data)*8):
        raise ValueError("Image is too small to hide data") 
    
    if data[-1] != 1:
        data.append(1)
    
    row_size = len(src[1])  # row's length
    
    insp = 0 # insertion point
   
    for dp in data:
        
        # from highest digit (0b10000000 if 8 bit for instance)
        for i in range(((dp.bit_length()+7)//8)*8):  
            src[insp//row_size][insp%row_size][0] &= 0xfe # setting 0 bit to 0
            src[insp//row_size][insp%row_size][0] |= (dp & 1) # setting zero bit to wanted value
            
            dp >>= 1
            insp+=1
    
    if verbose:
        print("data encoded")
        #print(data)
    
    return src

def LSB_get_data(src : np.array, verbose : bool = False):
    '''
    returns injected to src via LSB data
    reads until \0
    '''
    if not isinstance(src, np.ndarray):
        raise TypeError('passed non-numpy array '+str(type(src)))
    elif not isinstance(src[1], np.ndarray):
        raise TypeError('passed non-numpy array (sub)')
    if len(src[0][0]) != 3:
        raise TypeError('passed src array data is not pixels')
        
    row_size = len(src[1])  # row's length
    
    data = bytearray()
    ctr = 0
    var = 0
    
    while True:
        
        try:
            var |= ((src[ctr//row_size][ctr%row_size][0] & 1) << ctr%8)
        except Exception as ex:
            print(str(ex),'at', ctr,'decoding itration')
            break
            
        if ctr%8 == 7:
            data.append(var)
            var = 0
        
        ctr+=1
        if var == 1 and ctr%8 == 7 and ctr > 8: # 64 - one wide unicode
            break
        '''
        if ctr > 200000:
            # the payload is too big.
            break
        '''
    return data