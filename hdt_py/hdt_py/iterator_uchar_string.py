import ctypes


class IteratorUCharString(object):
    def __init__(self, hdt, func, lib):
        self.lib = lib

        self.it = func(hdt) # func = self.lib.HDT_getPredicates

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.lib.IteratorUCharString_delete(self.it)

    def hasNext(self) -> bool:
        has_next = self.lib.IteratorUCharString_hasNext
        has_next.argtypes = [ctypes.c_int]
        has_next.restype = ctypes.c_bool
        return has_next(self.it)

    def next(self) -> str:
        get_next = self.lib.IteratorUCharString_next
        get_next.argtypes = [ctypes.c_int]
        get_next.restype = ctypes.c_char_p
        return get_next(self.it)
