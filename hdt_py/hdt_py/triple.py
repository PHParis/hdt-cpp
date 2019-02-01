# coding=utf-8
class Triple(object):
    '''A triple contained in an HDT file.'''

    def __init__(self, array):
        self.s = array[0].decode('utf-8')
        self.p = array[1].decode('utf-8')
        self.o = array[2].decode('utf-8')

    def __str__(self):
        return self.s + " " + self.p + " " + self.o

    def __call__(self):
        return self.__str__()

    def __repr__(self):
        return "Triple(%s, %s, %s)" % (self.s, self.p, self.o)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Triple):
            return ((self.s == other.s) and (self.p == other.p) and (self.o == other.o))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))
