import os
import ctypes
from hdt_py.triple import Triple
from hdt_py.iterator_triple_string import IteratorTripleString
import multiprocessing
import sys
from hdt_py.utils import timing
from logging import Logger

class HDT(object):
    '''Represent an HDT file and allow to query it.'''

    @timing
    def __init__(self, hdtFilePath: str, logger: Logger, lib_path: str=None):
        if not os.path.isfile(hdtFilePath):
            raise FileNotFoundError(hdtFilePath + " has not been found!")
        if lib_path is None:
            lib_path = '/usr/local/src/hdt-cpp/libhdt/.libs/libhdt.so'
        if not os.path.isfile(lib_path):
            raise FileNotFoundError(lib_path + " has not been found!")
        self.lib = ctypes.cdll.LoadLibrary(lib_path)
        self.hdt = self.lib.HDT_new(bytes(hdtFilePath, encoding="utf8"))
        self.logger = logger
        if self.logger is not None:
            self.logger.name = self.__class__.__name__

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.lib.HDT_delete(self.hdt)

    def search(self, s: str, p: str, o: str):
        '''Search for specified triples in HDT file.

        For example, if s="http://dbpedia.org/resource/Paris" and p=o="", then all triples starting with Paris will be produced.
        '''
        with IteratorTripleString(self.hdt, s, p, o, self.lib) as it:
            while it.hasNext():
                arr = it.next()
                try:
                    yield Triple(arr)                
                except UnicodeDecodeError:
                    if self.logger is not None:
                        self.logger.info(f"UnicodeDecodeError: {arr}")
    
    def search_pattern(self, triple_pattern: str):
        '''Search for specified triples in HDT file.

        For example, if "http://dbpedia.org/resource/Paris ? ?", then all triples starting with Paris will be produced.
        '''
        splited = triple_pattern.split(" ")
        if len(splited) < 3:
            raise Exception("Your pattern must be like 'ex:A_Subject ? ex:An_Object'")
        s = splited[0]
        p = splited[1]
        o = " ".join(splited[2:])
        with IteratorTripleString(self.hdt, s, p, o, self.lib) as it:
            while it.hasNext():
                arr = it.next()
                try:
                    yield Triple(arr)                
                except UnicodeDecodeError:
                    if self.logger is not None:
                        self.logger.info(f"UnicodeDecodeError: {arr}")

    def get_predicates(self):
        '''Return the set of predicates contained in the HDT file.'''
        get_pred = self.lib.HDT_getPredicates
        get_pred.argtypes = [ctypes.c_int]
        get_pred.restype = ctypes.py_object
        return {p.decode('utf-8') for p in get_pred(self.hdt)}
