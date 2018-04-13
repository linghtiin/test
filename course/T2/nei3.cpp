/**     时钟类程序
 *
 *
 *
 *
 *
 */
#include<iostream>

using namespace std ;



/** 时钟类
 *  具有设置时间,显示时间等基本功能.
 *
 *
 *
 *
 */

class Clock
{
private:
    int hour,minute,second;
    int checkTime();
public:
    int setTime(int h1,int m1,int s1);
    void showTime();
    int runTime();
};

/** \brief 时间设置函数
 *          不支持数值自动进位.
 * \param h1 小时
 * \param m1 分钟
 * \param s1 秒
 * \return 0 正常返回;-1 数值越界;
 *
 */

int Clock::setTime(int h1=0,int m1=0,int s1=0)
{
    int err=0;
    hour=h1;
    minute=m1;
    second=s1;

    err=checkTime();
    if(err>0)
        return -1;
    return 0;
}

/** \brief 时间显示函数
 *          格式: "Time is :" \n h:m:s
 *
 *
 *
 */

void Clock::showTime()
{
    cout<<"Time is :"<<endl;
    cout<<hour<<':'<<minute<<':'<<second<<endl;
}

/** \brief 时间检查函数
 *          检查时间数值是否进位,越界;h,m,s依次检查.
 *
 *  该函数检查时间数值是否进位,越界;依h,m,s顺序逐个检查,返回值以 数值*10^(检查的次序) 实现.
 *  例:  return-100 h进位; return-20 m越界;
 * \return 0 正常返回;1 满足进位;2 数值越界;
 *
 */

int Clock::checkTime()
{
    if(second<0||second>60)
        return 2;
    else if(second==60)
        return 1;

    if(minute<0||minute>60)
        return 20;
    else if(minute==60)
        return 10;

    if(hour<0||hour>24)
        return 200;
    else if(hour==24)
        return 100;

    return 0;
}


/** \brief 时钟运行函数
 *          以秒为单位增加时间数值,自动进位,返回进位事件.
 *
 * \return 0 正常返回;1 数值进位;
 *
 */

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
