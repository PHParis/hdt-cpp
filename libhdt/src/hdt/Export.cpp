#include <iostream>
#include <HDTManager.hpp>
#include <string>
#include <python3.7m/Python.h>

using namespace hdt;

extern "C"
{
    HDT* HDT_new(const char* hdtFilePath){ return HDTManager::mapHDT(hdtFilePath); }
    
    HDT* HDT_newIndexed(const char* hdtFilePath){ return HDTManager::mapIndexedHDT(hdtFilePath); }

    IteratorTripleString* Iterator_new(HDT* hdt, const char* s, const char* p, const char* o){ 
        return hdt->search(s,p,o); 
    }

    IteratorUCharString* HDT_getPredicates(HDT* hdt)
    {
        IteratorUCharString *itPred = hdt->getDictionary()->getPredicates();
        return itPred;
        // PyObject* result = PyList_New(0);
        // while(itPred->hasNext()) {
        //     unsigned char *pred = itPred->next(); 
        //     std::string sPred(reinterpret_cast<char*>(pred));
        //     PyList_Append(result, PyBytes_FromString(sPred.c_str()));
        // }
        // return result;
    }
    
    bool IteratorUCharString_hasNext(IteratorUCharString* itPred){return itPred->hasNext();}
    void IteratorUCharString_delete(IteratorUCharString* itPred){delete itPred;}
    char const* IteratorUCharString_next(IteratorUCharString* itPred){
        unsigned char *pred = itPred->next();
        std::string sPred(reinterpret_cast<char*>(pred));
        return sPred.c_str();
        // std::string subj = triple->getSubject();
        // std::string pred = triple->getPredicate();
        // std::string obj = triple->getObject();
        // PyObject* result = PyList_New(0);
        // PyList_Append(result, PyBytes_FromString(subj.c_str()));
        // PyList_Append(result, PyBytes_FromString(pred.c_str()));
        // PyList_Append(result, PyBytes_FromString(obj.c_str()));
        // return result;
    }

    IteratorUCharString* HDT_getSubjects(HDT* hdt)
    {
        IteratorUCharString *itPred = hdt->getDictionary()->getSubjects();
        return itPred;
        // PyObject* result = PyList_New(0);
        // while(itPred->hasNext()) {
        //     unsigned char *pred = itPred->next(); 
        //     std::string sPred(reinterpret_cast<char*>(pred));
        //     PyList_Append(result, PyBytes_FromString(sPred.c_str()));
        // }
        // return result;
    }

    IteratorUCharString* HDT_getObjects(HDT* hdt)
    {
        IteratorUCharString *itPred = hdt->getDictionary()->getObjects();
        return itPred;
        // PyObject* result = PyList_New(0);
        // while(itPred->hasNext()) {
        //     unsigned char *pred = itPred->next(); 
        //     std::string sPred(reinterpret_cast<char*>(pred));
        //     PyList_Append(result, PyBytes_FromString(sPred.c_str()));
        // }
        // return result;
    }

    IteratorUCharString* HDT_getShared(HDT* hdt)
    {
        IteratorUCharString *itPred = hdt->getDictionary()->getShared();
        return itPred;
        // PyObject* result = PyList_New(0);
        // while(itPred->hasNext()) {
        //     unsigned char *pred = itPred->next(); 
        //     std::string sPred(reinterpret_cast<char*>(pred));
        //     PyList_Append(result, PyBytes_FromString(sPred.c_str()));
        // }
        // return result;
    }

    size_t HDT_getNsubjects(HDT* hdt)
    {
        return hdt->getDictionary()->getNsubjects();
    }
    size_t HDT_getNpredicates(HDT* hdt)
    {
        return hdt->getDictionary()->getNpredicates();
    }
    size_t HDT_getNobjects(HDT* hdt)
    {
        return hdt->getDictionary()->getNobjects();
    }
    size_t HDT_getNobjectsLiterals(HDT* hdt)
    {
        return hdt->getDictionary()->getNobjectsLiterals();
    }
    size_t HDT_getNshared(HDT* hdt)
    {
        return hdt->getDictionary()->getNshared();
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
