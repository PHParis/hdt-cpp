import os
import ctypes
from hdt_py.triple import Triple
from hdt_py.iterator_triple_string import IteratorTripleString
import multiprocessing
import sys
from hdt_py.utils import timing


class HDT(object):
    '''Represent an HDT file and allow to query it.'''

    @timing
    def __init__(self, hdtFilePath, lib_path=None):
        if not os.path.isfile(hdtFilePath):
            raise FileNotFoundError(hdtFilePath + " has not been found!")
        if lib_path is None:
            lib_path = '/usr/local/src/hdt-cpp/libhdt/.libs/libhdt.so'
        if not os.path.isfile(lib_path):
            raise FileNotFoundError(lib_path + " has not been found!")
        self.lib = ctypes.cdll.LoadLibrary(lib_path)
        self.hdt = self.lib.HDT_new(bytes(hdtFilePath, encoding="utf8"))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.lib.HDT_delete(self.hdt)

    def search(self, s, p, o):
        '''Search for specified triples in HDT file.

        For example, if s="http://dbpedia.org/resource/Paris" and p=o="", then all triples starting with will be produced.
        '''
        with IteratorTripleString(self.hdt, s, p, o, self.lib) as it:
            while it.hasNext():
                yield Triple(it.next())

    def get_predicates(self):
        '''Return the set of predicates contained in the HDT file.'''
        get_pred = self.lib.HDT_getPredicates
        get_pred.argtypes = [ctypes.c_int]
        get_pred.restype = ctypes.py_object
        return {p.decode('utf-8') for p in get_pred(self.hdt)}
