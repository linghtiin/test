/*
    单片机实现计算器功能；
    使用LCD602；
    矩阵键盘；
    可实现加减多位加减乘除；

 */

#include <STC89C5xRC.H>
#include "lcd.h"


#define N 80


unsigned char key;
unsigned char t[N]; //显示缓存
unsigned char l,e,sta;


//错误处理函数
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


//全局LCD处理
void lcd_mo()
{

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

//显示刷新函数
void lcd_scan()
{
    w_com(0x01);

    if(sta>78)    //LCD数据溢出
        err_mo(5);
    else if(sta>54) //
        w_com(0x07);
    else if(sta>40) //
        w_com(0x06);
    else if(sta>14) //
        w_com(0x07);

    for(i=0;i<N;++)
        w_data(t[i]);
}

void main(void)
{
    init();

    unsigned char i;
    for(i=0;i<=N;i++)
        t[i]=0x20;


    l=0,e=0,sta=0;
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
                    t[sta]='+';
                    break;
                case(8):
                    t[sta]='-';
                    break;
                case(12):
                    t[sta]='*';
                    break;
                case(16):
                    t[sta]='/';
                    break;
            }

            delayms(10);
            l=0;
            key=0;
            sta+=1;

        }
        //清零的分支
        else if(key==13)
        {
            unsigned char i;
            for(i=0;i<=N;i++)
                t[i]=0x20;

            w_com(0x01);

            sta=0;
            l=0;
            e=0;
            key=0;
        }
        //等于的分支
        else if(key==15)
        {
            float daan,t_daan,tt_daan;
            char f1=0,f2=0;
            if(l==0||e!=0)
            {
                //输出错误
                if(l==0)
                    e=1;
                err_mo(e);
            }

            daan=0;
            t_daan=0;
            tt_daan=0;
            for(i=0;i<sta;i++)
            {
                switch(t[i])
                {
                    case('1'):
                        tt_daan*=10;
                        tt_daan+=1;
                        break;
                    case('2'):
                        tt_daan*=10;
                        tt_daan+=2;
                        break;
                    case('3'):
                        tt_daan*=10;
                        tt_daan+=3;
                        break;
                    case('4'):
                        tt_daan*=10;
                        tt_daan+=4;
                        break;
                    case('5'):
                        tt_daan*=10;
                        tt_daan+=5;
                        break;
                    case('6'):
                        tt_daan*=10;
                        tt_daan+=6;
                        break;
                    case('7'):
                        tt_daan*=10;
                        tt_daan+=7;
                        break;
                    case('8'):
                        tt_daan*=10;
                        tt_daan+=8;
                        break;
                    case('9'):
                        tt_daan*=10;
                        tt_daan+=9;
                        break;
                    case('+'):
                        if(f2==0)
                            daan=tt_daan;
                        f2=1;
                        if(f1)

                        break;
                    case('-'):
                        if(f==0)
                        {
                            daan=tt_daan;
                            break;
                        }
                        daan-=t_daan;
                        f=2;
                        break;
                    case('*'):
                        if(f1==0)
                        {
                            daan=t_daan;
                            break;
                        }
                        daan*=t_daan;
                        f=3;
                        break;
                    case('/'):
                        if(f==0)
                        {
                            daan=t_daan;
                            break;
                        }
                        if(t_daan==0)
                            err_mo(3);
                        daan/=t_daan;
                        f=4;
                        break;
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

            //数字增加显示
            if(key>8)
                key=key-2;
            else if(key>4)
                key=key-1;

            t[sta]=0x30+key;


            key=0;
            sta+=1;
            l+=1;

        }


        lcd_scan();
    }


}































