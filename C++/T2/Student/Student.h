#ifndef STUDENT_H_INCLUDED
#define STUDENT_H_INCLUDED

#include <iostream>
#include <cstring>

enum subject
{
    Math,
    English,
    Politics,
};
//typedef enum subject sub;



class persent
{
private:

protected:
	char name[20];
	int age;

public:
    static int number;
    persent();
    persent(char* na,int ag);
    present(persent &p);
    ~persent();

	char* GetName(){return name;}
	int GetAge(){return age;}

	void SetName(char* na){strcpy(name,na);}
	void SetAge(int ag){age=ag;}
	void disp();

};


class student:public persent
{
private:
	float math;
	float english;
	float politics;
public:
    static int number;
	student();
	student(char* na,int ag,float s1,float s2,float s3);
	student(student &stu);
	~student();

	float GetScore(enum subject sub);

	void SetScore(enum subject sub,float s);
	void disp();
};


int init();

#endif // STUDENT_H_INCLUDED
