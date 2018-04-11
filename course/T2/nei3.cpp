/**     时钟类程序
 *
 *
 *
 *
 *
 */
#include<iostream>

using namespace std ;

class Clock
{
private:
    int hour,minute,second;
public:
    int setTime(int h1,int m1,int s1);
    void showTime();
    int checkTime();
    int runTime();
};

int Clock::setTime(int h1=0,int m1=0,int s1=0)
{
    int err=0;
    hour=h1;
    minute=m1;
    second=s1;

    err=checkTime();
    if(err>0)
        return -1;

}

void Clock::showTime()
{
    cout<<"Time is :"<<endl;
    cout<<hour<<':'<<minute<<':'<<second<<endl;
}


int Clock::checkTime()
{

    if(hour<0||hour>24)
        return 200;
    else if(hour==24)
        return 100;

    if(minute<0||minute>60)
        return 20;
    else if(minute==60)
        return 10;

    if(second<0||second>60)
        return 2;
    else if(second==60)
        return 1;

    return 0;
}



int Clock::runTime()
{
    int err,rnum=0;
    second++;
    err=checkTime();
    if(err==1)
    {
        second=0;
        minute++;
        rnum=1;
    }
    err=checkTime();
    if(err/10==1)
    {
        minute=0;
        hour++;
        rnum=rnum+10;
    }
    err=checkTime();
    if(err/100==1)
    {
        hour=0;
        rnum=rnum+100;
    }
    return rnum;
}


int main()
{
    Clock c1;
    int i=200000;
    if(c1.setTime(12,23,11)<0)
        cout<<"时间设置错误."<<endl;

    while(i--)
    {

        if(c1.runTime()!=0)
            c1.showTime();
    }

    return 0;
}
