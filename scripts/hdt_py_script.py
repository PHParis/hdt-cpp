# coding=utf-8
from hdt_py import HDT
import traceback

if __name__ == "__main__":
    hdt_file = "/data/dataset.hdt"
    # hdt_file = "/mnt/d/dev/hdt/dataset.hdt"
    # with HDT(hdt_file, "/mnt/d/dev/Python/hdt_py/libs/libhdt.so") as f:
    with HDT(hdt_file) as f:
        for triple in f.search("http://dbpedia.org/resource/Paris", "", ""):
            try:
                print(str(triple).encode('utf-8'))
            except UnicodeEncodeError:# as e:
                print(traceback.format_exc())#print(e)
