'''
Module to test the memory on the devise. This is done to check tht a memory error is less or more likely to occur based on an input size.
Created on Apr 18, 2019

@author: 
'''
#! /usr/bin/python
import ctypes
import sys

#the size to evaluate 
size = int(sys.argv[1])

'''
Class to carry out the memory test
'''
class MemoryTest(ctypes.Structure):
    _fields_ = [  ('chars' , ctypes.c_char*size * 1024*1024 ) ]
    
    #run the test
    try:
        test = MemoryTest()
        print(('success => {0:>4}MB was allocated'.format(size) ))
    except:
        print(('failure => {0:>4}MB can not be allocated'.format(size) ))