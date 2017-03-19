#include "lcd.h"



void delayms (uint xms)
{
    uchar i,j;
    for(i=xms;i>0;i--)
        for(j=120;j>0;j--);
}


void w_com(uchar com)
{
    en=0;
    rs=0;
    rw=0;

    data=com;
    delayms(1);

    en=1;
    delayms(10);
    en=0;
}

void w_data(uchar dat)
{
    en=0;
    rs=1;
    rw=0;

    data=dat;
    delayms(1);

    en=1;
    delayms(10);
    en=0;
}



void init()
{
    w_com(0x38);
    w_com(0x0f);
    w_com(0x06);
    w_com(0x01);
    w_com(0x80);
}
