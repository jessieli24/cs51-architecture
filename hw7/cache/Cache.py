#
# Cache.py - data structure representing a cache
#
# Jessie Li     CS 51, Fall 2024
#

from enum import Enum
from typing import List 

tagMaskDM: int = 0xfffffc00
setMaskDM: int = 0x000003f0

tagMask2S: int = 0xfffffe00
setMask2S: int = 0x000001f0

tagMask4S: int = 0xffffff00
setMask4S: int = 0x000000f0

tagMaskFA: int = 0xfffffff0
setMaskFA: int = 0x00000000

class CacheMode(Enum):
    DIRECT_MAPPED = 0
    TWO_WAY = 1
    FOUR_WAY = 2
    FULLY_ASSOCIATIVE = 3
    
    def __str__(self):
        return {
            CacheMode.DIRECT_MAPPED: "Direct-mapped",
            CacheMode.TWO_WAY: "2-way set associative",
            CacheMode.FOUR_WAY: "4-way set associative",
            CacheMode.FULLY_ASSOCIATIVE: "Fully associative"
        }[self]
    
class Cache:
    class Line:
        def __init__(self, index: int, nBlockBytes: int):
            self.index: int = index
            self.valid: bool = False
            self.tag: int = 0
            self.lastTouch = 0
            self.next = None
    
    def __init__(self, blockCapacity: int, nSetBits: int, nTagBits: int, nBlockBits: int, mode: CacheMode):
        self.nSetBits = nSetBits
        self.nTagBits = nTagBits
        self.nBlockBits = nBlockBits
        
        self.S = 2 ** nSetBits
        self.E = blockCapacity // self.S
        self.B = 2 ** nBlockBits
        
        self.tagMask = ~(0xffffffff >> nTagBits)
        self.blockMask = ~(0xffffffff << nBlockBits)
        self.setMask = ~(self.tagMask | self.blockMask)
        
        self.sets = self.newCache(self.S, self.E, self.B)
        
        self.nTouches = 0
        self.nHits = 0
        self.nMisses = 0
        
        # print(f'tagMask = 0x{(self.tagMask & 0xffffffff):08x}')
        # print(f'setMask = 0x{self.setMask:08x}')
        print('-----------------------------------------------')
        print(f'{mode}')
        
        nBlocks  = self.S * self.E
        print(f'{nBlocks} blocks, {self.B} bytes in block; {self.S} sets, {self.E} lines per set\n')
        # print('-----------------------------------------------')
        
    def newCache(self, nSets: int, nLinesPerSet: int, nBytesPerBlock):
        return [[Cache.Line(j, nBytesPerBlock) for j in range(nLinesPerSet)] for i in range(nSets)]
        
    def touch(self, type: str, address: str):
        self.nTouches += 1
        
        setIndex: int = (address & self.setMask) >> self.nBlockBits
        tag: int = (address & self.tagMask) >> (self.nBlockBits + self.nSetBits)
        
        # print(f'{type}{self.nTouches:07d}: addr {hex(address)}; looking for tag {hex(tag)} in set {hex(setIndex)}.\n')
        # print(f'State of set {hex(setIndex)}:')
        set: List[Cache.Line] = self.sets[setIndex]
        
        hit: bool = False
        updateLine: Cache.Line = None

        for i in range(self.E):
            line: Cache.Line = set[i]
            
            # print(f'line {hex(i)} V={1 if line.valid else 0} tag {hex(line.tag)} last_touch={line.lastTouch:07d}')
            
            if (line.valid and tag == line.tag):
                updateLine = line
                hit = True
                break
            elif (not hit and (updateLine is None or (line.lastTouch < updateLine.lastTouch))): 
                updateLine = line
                
        # print('\n')
        if (updateLine is None):
            print('Error: Failed to update cache.')
            return
        
        if (hit):
            # print(f'Found it in line {hex(updateLine.index)}. Hit! Updating last_touch to {self.nTouches}.')
            self.nHits += 1
        elif (not hit and updateLine.lastTouch == 0):
            # print(f'Miss! Found empty line {hex(updateLine.index)}; adding block there; setting last_touch to {self.nTouches}.')
            self.nMisses += 1
        else:
            # print(f'Miss! Evicting line {hex(updateLine.index)}; adding block there; setting last_touch to {self.nTouches}.')
            self.nMisses += 1
        
        updateLine.valid = True
        updateLine.tag = tag
        updateLine.lastTouch = self.nTouches
        
        # print('-----------------------------------------------')