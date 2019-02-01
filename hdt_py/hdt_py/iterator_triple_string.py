import ctypes


class IteratorTripleString(object):
    def __init__(self, hdt, s, p, o, lib):
        self.lib = lib

        self.it = self.lib.Iterator_new(hdt, bytes(s, encoding="utf8"), bytes(
            p, encoding="utf8"), bytes(o, encoding="utf8"))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.lib.Iterator_delete(self.it)

    def hasNext(self):
        has_next = self.lib.Iterator_hasNext
        has_next.argtypes = [ctypes.c_int]
        has_next.restype = ctypes.c_bool
        return has_next(self.it)

    def next(self):
        get_next = self.lib.Iterator_next
        get_next.argtypes = [ctypes.c_int]
        get_next.restype = ctypes.py_object
        return get_next(self.it)
