/***************************************************************
 * Name:      Class.h
 * Purpose:   Language Maker Classes
 * Author:    Linghtiin (wrqal666@gmail.com)
 * Created:   2018-03-30
 * Copyright: Linghtiin ()
 * License:
 **************************************************************/

#ifndef CLASS_H_INCLUDED
#define CLASS_H_INCLUDED

class LanguageSource;

namespace LanguageMaker {

enum type_Phoneme {
    Noun,
    Verb;
};

struct Phoneme{

char name[6];
int sound[4][2];
int motion[4];
enum type_Phoneme Type;

};






class Spell{
public:
    char* getword();
    int* getsound();



};




}


#endif // CLASS_H_INCLUDED
