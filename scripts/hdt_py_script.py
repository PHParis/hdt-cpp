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
                print(triple)
            except UnicodeEncodeError:  # as e:
                print(traceback.format_exc())  # print(e)
# BUG when displaying Île de France only on docker
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/area "1.054E8"^^<http://www.w3.org/2001/XMLSchema#double>
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/area "1.054E8"^^<http://www.w3.org/2001/XMLSchema#double>
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/country http://dbpedia.org/resource/France
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/country http://dbpedia.org/resource/France
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/inseeCode "75056"
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/inseeCode "75056"
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/mayor http://dbpedia.org/resource/Anne_Hidalgo
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/mayor http://dbpedia.org/resource/Anne_Hidalgo
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/populationTotal "2229621"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/populationTotal "2229621"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/postalCode "75001-75020, 75116"
# http://dbpedia.org/resource/Paris http://dbpedia.org/ontology/postalCode "75001-75020, 75116"
# Traceback (most recent call last):
#   File "hdt_py_script.py", line 10, in <module>
#     for triple in f.search("http://dbpedia.org/resource/Paris", "", ""):
#   File "/usr/local/lib/python3.4/dist-packages/hdt_py/hdt_document.py", line 37, in search
#     yield Triple(it.next())
#   File "/usr/local/lib/python3.4/dist-packages/hdt_py/triple.py", line 9, in __init__
#     print(self.s + " " + self.p + " " + self.o)
# UnicodeEncodeError: 'ascii' codec can't encode character '\xce' in position 97: ordinal not in range(128)

# Using MinGW to compile on Windows
# D:\dev\cpp\hdt-cpp>sh autogen.sh
# configure.ac:16: warning: macro `AM_PROG_AR' not found in library
# aclocal-1.11: installing `m4/libtool.m4' from `/mingw/share/aclocal/libtool.m4'
# aclocal-1.11: installing `m4/ltoptions.m4' from `/mingw/share/aclocal/ltoptions.m4'
# aclocal-1.11: installing `m4/ltsugar.m4' from `/mingw/share/aclocal/ltsugar.m4'
# aclocal-1.11: installing `m4/ltversion.m4' from `/mingw/share/aclocal/ltversion.m4'
# aclocal-1.11: installing `m4/lt~obsolete.m4' from `/mingw/share/aclocal/lt~obsolete.m4'
# configure.ac:16: warning: macro `AM_PROG_AR' not found in library
# libtoolize: putting auxiliary files in AC_CONFIG_AUX_DIR, `build'.
# libtoolize: copying file `build/ltmain.sh'
# libtoolize: putting macros in AC_CONFIG_MACRO_DIR, `m4'.
# libtoolize: copying file `m4/libtool.m4'
# libtoolize: copying file `m4/ltoptions.m4'
# libtoolize: copying file `m4/ltsugar.m4'
# libtoolize: copying file `m4/ltversion.m4'
# libtoolize: copying file `m4/lt~obsolete.m4'
# configure.ac:16: warning: macro `AM_PROG_AR' not found in library
# configure.ac:10: error: possibly undefined macro: AC_SUBST
#       If this token and others are legitimate, please use m4_pattern_allow.
#       See the Autoconf documentation.
# configure.ac:16: error: possibly undefined macro: AM_PROG_AR
# configure.ac:48: error: possibly undefined macro: AC_DEFINE
# autoreconf-2.68: /mingw/bin/autoconf-2.68 failed with exit status: 1