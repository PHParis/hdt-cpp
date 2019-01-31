#include <iostream>
#include <HDTManager.hpp>
#include <string>
// #include <python3.5/Python.h>
#include <python3.4/Python.h>

using namespace hdt;

extern "C"
{
    HDT* HDT_new(const char* hdtFilePath){ return HDTManager::mapHDT(hdtFilePath); }

    IteratorTripleString* Iterator_new(HDT* hdt, const char* s, const char* p, const char* o){ 
        return hdt->search(s,p,o); 
    }

    PyObject* HDT_getPredicates(HDT* hdt)
    {
        IteratorUCharString *itPred = hdt->getDictionary()->getPredicates();
        PyObject* result = PyList_New(0);
        while(itPred->hasNext()) {
            unsigned char *pred = itPred->next(); 
            std::string sPred(reinterpret_cast<char*>(pred));
            PyList_Append(result, PyBytes_FromString(sPred.c_str()));
        }
        return result;
    }

    bool Iterator_hasNext(IteratorTripleString* it){return it->hasNext();}

    PyObject* Iterator_next(IteratorTripleString* it){
        TripleString *triple = it->next();
        std::string subj = triple->getSubject();
        std::string pred = triple->getPredicate();
        std::string obj = triple->getObject();
        PyObject* result = PyList_New(0);
        PyList_Append(result, PyBytes_FromString(subj.c_str()));
        PyList_Append(result, PyBytes_FromString(pred.c_str()));
        PyList_Append(result, PyBytes_FromString(obj.c_str()));
        return result;
    }

    void Iterator_delete(IteratorTripleString* it){delete it;}

    void HDT_delete(HDT* hdt){delete hdt;}

} 
