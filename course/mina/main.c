/*
    单片机实现计算器功能；
    使用LCD602；
    矩阵键盘；
    可实现加减多位加减乘除；

 */

#include <STC89C5xRC.H>
#include "lcd.h"


#define N 5


unsigned char key;
unsigned char t[N]; //其十位用于错误检测
float n[N];
float daan;
unsigned char l,f,e,sta;

void err_mo(uchar e)
{
    uchar i,err[]="error";
    w_data(0x01);
    for(i=0;i<5;i++)
        w_data(err[i]);
    w_data(0x14);
    w_data(0x14);
    w_data(0x30+e);

    while(key!=13)
        keyscan();
    w_data(0x01);
}

void lcd_mo()
{
        //全局LCD处理
        if(sta>78)    //LCD数据溢出
            err_mo(5);
        else if(sta>54) //
            w_com(0x07);
        else if(sta>40) //
            w_com(0x06);
        else if(sta>14) //
            w_com(0x07);

}

void keyscan() // 矩阵键盘 完成版
{
	keyline=0x0f;
	if(keyline!=0x0f)
	{
		delayms(10);
		if(keyline!=0x0f)
		{
			keyline=0x0f;
			switch(keyline)
			{
				case(0X07): key=1;break;
				case(0X0b): key=2;break;
				case(0X0d): key=3;break;
				case(0X0e): key=4;break;
			}
			keyline=0xf0;
			switch(keyline)
			{
				case(0X70):	key=key;break;
				case(0Xb0):	key=key+4;break;
				case(0Xd0): key=key+8;break;
				case(0Xe0):	key=key+12;break;
			}
			while(keyline!=0xf0)
				delayms(10);
		}
	}

}



void main(void)
{

    init();
    l=0,f=0,e=0,sta=0;
    while(1)
    {
        keyscan();

        //加减乘除的分支
        if(key%4==0)
        {
            if(l==0)
                e=1;
            switch(key)
            {
                case(4):
                    t[f]=1;
                    f++;
                    l=0;
                    w_data('+');
                    break;
                case(8):
                    t[f]=2;
                    f++;
                    l=0;
                    w_data('-');
                    break;
                case(12):
                    t[f]=3;
                    f++;
                    l=0;
                    w_data('*');
                    break;
                case(16):
                    t[f]=4;
                    f++;
                    l=0;
                    w_data('/');
                    break;
            }

            delayms(10);

            key=0;
            sta+=1;

        }
        //清零的分支
        else if(key==13)
        {
            unsigned char i;
            for(i=0;i<=f;i++)
            {
                n[i]=0;
                t[i]=0;
            }

            w_com(0x01);

            f=0;
            l=0;
            e=0;
            sta=0;
            key=0;
        }
        //等于的分支
        else if(key==15)
        {
            unsigned char i,we[10]={0};
            double t;
            if(l==0||e!=0)
            {
                //输出错误
                if(l==0)
                    e=1;
                err_mo(e);
            }

            daan=n[0];
            for(i=0;i<f;i++)
            {
                switch(t[i])
                {
                    case(1):
                        daan+=n[i+1];
                        break;
                    case(2):
                        daan-=n[i+1];
                        break;
                    case(3):
                        daan*=n[i+1];
                        break;
                    case(4):
                        if(daan==0||n[i+1]==0)
                            err_mo(4);
                        else
                            daan/=n[i+1];
                        break;
                    default:
                        err_mo(3);
                }
            }

            //得出答案，现在显示
            w_data('=');
//            daan=daan*100;
            for(l=0;daan>1;l++)
            {
                t=daan/1;
                t=t%10;
                we[l]=0x30+t;
                daan=daan/10;
            }
            sta+=l;
            lcd_mo();
            for(;l>=0;l--)
                w_data(we[l]);




        }
        //数字的分支
        else if(key!=0)
        {
            if(key==14)
                key=0;
            if(l>8)
                e=2;
            n[f]*=10;
            n[f]+=key;

            //数字增加显示
            if(key>8)
                w_data(0x30+key-2);
            else if(key>4)
                w_data(0x30+key-1);
            else
                w_data(0x30+key);



            key=0;
            sta+=1;
            l+=1;

        }
    }


}































