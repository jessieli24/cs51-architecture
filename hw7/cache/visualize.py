#
# visualize.py - visualizes hit rates for direct-mapped, two-way, four-way, and fully associative
#
# usage: python visualize.py -f [filename]
#
# Jessie Li     CS 51, Fall 2024
#

import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys

from Cache import Cache, CacheMode

def main(filename: str): 
    cacheDM = Cache(blockCapacity = 64, nSetBits = 6, nTagBits = 22, nBlockBits = 4, mode = CacheMode.DIRECT_MAPPED)
    cache2S = Cache(blockCapacity = 64, nSetBits = 5, nTagBits = 23, nBlockBits = 4, mode = CacheMode.TWO_WAY)
    cache4S = Cache(blockCapacity = 64, nSetBits = 4, nTagBits = 24, nBlockBits = 4, mode = CacheMode.FOUR_WAY)
    cacheFA = Cache(blockCapacity = 64, nSetBits = 0, nTagBits = 28, nBlockBits = 4, mode = CacheMode.FULLY_ASSOCIATIVE)
    
    if (filename == '-'):
        in_file = sys.stdin
    else:
        try: 
            with open(filename, "r"):
                in_file = open(filename, "r")
        except IOError:
            print("Error: Could not open \"" + filename + "\" in read mode")
            return

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
        
        cacheDM.touch(c, n)
        cache2S.touch(c, n)
        cache4S.touch(c, n)
        cacheFA.touch(c, n)
        
        line = in_file.readline()
    
    nSetBits = np.array([cacheDM.nSetBits, cache2S.nSetBits, cache4S.nSetBits, cacheFA.nSetBits])
    nHits = np.array([cacheDM.nHits, cache2S.nHits, cache4S.nHits, cacheFA.nHits]) / cacheDM.nTouches
    
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.plot(nSetBits, nHits, '-o')
    plt.xlabel('Number of Set Bits (2^s Sets)')
    plt.ylabel('Hit Rate')
    plt.title('Hit Rate v. Set Bits')
    plt.savefig('results/results.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-f", "--file", 
        help='Trace file containing a list of byte-by-byte memory accesses: a [D] or [I] followed by the address in hex.'
    )
    
    args = parser.parse_args()
    
    if (args.file is None):
        print('No trace file provided.')
        print('Usage: python main.py -m mode -f filename')
        sys.exit(1)
        
    main(args.file)