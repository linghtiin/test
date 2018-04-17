#include<iostream>

using namespace std ;

class clock
{
private:
    int hour,minute,second;
public:
    clock(int h,int m,int s);
    clock(clock &p);
    ~clock();
    void setTime(int h1,int m1,int s1);
    void showTime();
    int checkTime();
    void runTime();
};

clock::clock(int h,int m,int s)
{
    hour=h;
    minute=m;
    second=s;
}


void clock::setTime(int h1=0,int m1=0,int s1=0)
{
    int err=0;
    hour=h1;
    minute=m1;
    second=s1;

    err=checkTime();
    if(err>0)
        cout<<"Time's number is out space."<<endl;

}

void clock::showTime()
{
    cout<<"Time is :"<<endl;
    cout<<hour<<':'<<minute<<':'<<second<<endl;
}


int clock::checkTime()
{
    int err=0;

    if(hour<0||hour>24)
        err=err+200;
    else if(hour==24)
        err=err+100;

    if(minute<0||minute>60)
        err=err+20;
    else if(minute==60)
        err=err+10;

    if(second<0||second>60)
        err=err+2;
    else if(second==60)
        err=err+1;

    return err;
}



void clock::runTime()
{
    int err;
    second++;
    err=checkTime();
    if(err/10%10=1)
    {

    }
}


