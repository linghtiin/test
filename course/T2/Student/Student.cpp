#include "Student.h"

using namespace std;

//////////////////////////////////////////////
//      初始化
//////////////////////////////////////////////
int init()
{


    return 0;
}
//////////////////////////////////////////////
//      Present函数
//////////////////////////////////////////////

persent::persent()
{
    number++;
}

persent::persent(char* na, int ag)
{
    strcpy(name,na);
    age=ag;

    number++;
}

persent::~persent()
{
    number--;
}

/** @brief disp
  *
  */
void persent::disp()
{
    cout<<"Persent`s index:"<<endl;
    cout<<"name="<<name<<endl;
    cout<<"age="<<age<<endl;
}

////////////////////////////////////////////////////////////////
//      Student函数
////////////////////////////////////////////////////////////////

student::student()
{
    number++;
}

student::student(char* na, int ag, float s1, float s2, float s3)
{
    strcpy(name,na);
    age=ag;

    math=s1;
    english=s2;
    politics=s3;

    number++;
}

student::student(student& stu)
{
    number++;
}

student::~student()
{
    number--;
}

/** @brief GetScore
  * @param sub 科目名称
  */
float student::GetScore(enum subject sub)
{
    float t_score=0;
    switch (sub)
    {
    case  Math :
        t_score = math;
        break;
    case  English :
        t_score = english;
        break;
    case  Politics :
        t_score = politics;
        break;
    default:
        cout<<"waring: Can`t find sub."<<endl;
        t_score = -1;
        break;
    }
    return t_score;
}


/** @brief SetScore
  *
  * @param sub 科目名称
  * @param s   成绩
  */
void student::SetScore(enum subject sub, float s)
{
    switch (sub)
    {
    case Math :
        math = s;
        break;
    case English :
        english = s;
        break;
    case Politics :
        politics = s;
        break;
    default:
        cout<<"waring: Can`t find sub."<<endl;
        break;
    }

}

/** @brief disp
  *
  * @todo: document this function
  */
void student::disp()
{
    cout<<"Student`s index:"<<endl;
    cout<<"name="<<name<<endl;
    cout<<"age="<<age<<endl;
    cout<<"math="<<math<<endl;
    cout<<"english="<<english<<endl;
    cout<<"politics="<<politics<<endl;
}

//  test函数
int persent::number=0;
int student::number=0;

int main()
{
    init();
    char tName[20];
    int tAge;
    float tMath,tEnglish,tPolitics;
    cin>>tName;
    strcpy(tName,"本方");
    persent ones(tName,17);
    student s[16];
    ones.disp();

    for (int i=0;i<16;i++)
    {

        cin>>tName>>tAge;
        cin>>tMath>>tEnglish>>tPolitics;
        s[i].SetName(tName);
        s[i].SetAge(tAge);
        s[i].SetScore(Math,tMath);
        s[i].SetScore(English,tEnglish);
        s[i].SetScore(Politics,tPolitics);
        s[i].disp();
    }
    return 0;
}
