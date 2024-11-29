#
# main.py - simulates a direct-mapped, two-way, four-way, and fully associative cache
#
# usage: python main.py -m [0-3] -f [filename]
#
# Jessie Li     CS 51, Fall 2024
#

import sys
import argparse
import time

from Cache import Cache, CacheMode

def main(filename: str, mode: CacheMode.DIRECT_MAPPED):
    cache: Cache = None
    
    match (mode):
        case CacheMode.DIRECT_MAPPED:
            cache = Cache(blockCapacity = 64, nSetBits = 6, nTagBits = 22, nBlockBits = 4, mode = CacheMode.DIRECT_MAPPED)
        
        case CacheMode.TWO_WAY:
            cache = Cache(blockCapacity = 64, nSetBits = 5, nTagBits = 23, nBlockBits = 4, mode = CacheMode.TWO_WAY)
            
        case CacheMode.FOUR_WAY:
            cache = Cache(blockCapacity = 64, nSetBits = 4, nTagBits = 24, nBlockBits = 4, mode = CacheMode.FOUR_WAY)
            
        case CacheMode.FULLY_ASSOCIATIVE:
            cache = Cache(blockCapacity = 64, nSetBits = 0, nTagBits = 28, nBlockBits = 4, mode = CacheMode.FULLY_ASSOCIATIVE)
        
        case _:
            print('Error: Unknown mode.')
            return
    
    # read file - from io_example.py (provided in the assignment)
    if (filename == '-'):
        in_file = sys.stdin
    else:
        try: 
            with open(filename, "r"):
                in_file = open(filename, "r")
        except IOError:
            print("Error: Could not open \"" + filename + "\" in read mode")
            return
    
    startTime = time.time()
    line = in_file.readline()
    while line:
        stripped_line = line.strip()
        
        # should I exit?
        if ( stripped_line == "exit" ):
            if (filename != '-'):
                in_file.close()
            return

        # split line on spaces
        args = stripped_line.split(" ")
        
        c = args[0] # D or I
        n = int(args[1], 16) # address, unsigned int (at least 32 bits)
        cache.touch(c, n)
            
        line = in_file.readline()
    
    endTime = time.time()
    in_file.close()  
    
    # print('-----------------------------------------------')
    print(f'Hits: {cache.nHits}, Misses: {cache.nMisses}, Touches: {cache.nTouches}')
    print(f'Time: {endTime - startTime:.6f} seconds')
    print('-----------------------------------------------')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-m", "--mode", 
        help="""Mode:
        0 - Direct-mapped
        1 - Two-way
        2 - Four-way
        3 - Fully associative""",
        type=int,
        default=0
    )
    
    parser.add_argument(
        "-f", "--file", 
        help='Trace file containing a list of byte-by-byte memory accesses: a [D] or [I] followed by the address in hex.'
    )
    
    args = parser.parse_args()
    
    if (args.file is None):
        print('No trace file provided.')
        print('Usage: python main.py -m mode -f filename')
        sys.exit(1)
        
    try:
        mode = CacheMode(args.mode)
    except ValueError:
        print("Error: Invalid cache mode.")
    
    main(args.file, mode)