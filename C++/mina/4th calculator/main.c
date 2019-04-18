/*
    单片机实现计算器功能；
    使用LCD602；
    矩阵键盘；
    可实现加减多位加减乘除；

 */

#include <STC89C5xRC.H>
#include "lcd.h"
#include <math.h>


#define N 40


unsigned char key;
unsigned char t[N]; //显示缓存
unsigned char l,e,sta;


//错误处理函数
void err_mo(uchar e)
{
    w_data(0x01);
    w_data('e');
    w_data('r');
    w_data('r');
    w_data('o');
    w_data('r');
    w_data(0x14);
    w_data(0x14);
    w_data(0x30+e);

    while(key!=13)
        keyscan();
    w_data(0x01);
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
    uchar i;
    w_com(0x01);

    if(sta>38)    //LCD数据溢出
    {
        err_mo(5);
        return;
    }


    if(sta>14) //
        w_com(0x07);

    for(i=0;i<N;i++)
        w_data(t[i]);
		delayms(80);
}

void main(void)
{
    init();

    for(l=0;l<=N;l++)
        t[l]=0x20;


    l=0,e=0,sta=0;
    while(1)
    {
        keyscan();
        main_loop:


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
            for(l=0;l<=N;l++)
                t[l]=0x20;

            w_com(0x01);

            sta=0;
            l=0;
            e=0;
            key=0;
        }
        //等于的分支
        else if(key==15)
        {
            float daan[4]={0};
            uchar fg[3]={0},t_daan,t_fg;
            uchar tt,f_f;

            t_daan=0;
            t_fg=0;
            f_f=0;

            if(l==0||e!=0)
            {
                //输出错误
                if(l==0)
                    e=1;
                err_mo(e);
                goto main_loop;
            }

            t[sta]='=';
            sta++;
            for(l=0;l<sta;l++)
            {
                switch(t[l])
                {
                    case('1'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=1;
                        break;
                    case('2'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=2;
                        break;
                    case('3'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=3;
                        break;
                    case('4'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=4;
                        break;
                    case('5'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=5;
                        break;
                    case('6'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=6;
                        break;
                    case('7'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=7;
                        break;
                    case('8'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=8;
                        break;
                    case('9'):
                        daan[t_daan]*=10;
                        daan[t_daan]+=9;
                        break;
                }
                if(t[l]=='+'||t[l]=='-'||t[l]=='*'||t[l]=='/'||t[l]=='=')
                {
                    switch(t[l])
                    {
                                case('+'): f_f=11; break;
                                case('-'): f_f=12; break;
                                case('*'): f_f=21; break;
                                case('/'): f_f=22; break;
                                case('='): f_f=0;
                    }

                    if(f_f/10>fg[t_fg]/10)
                    {
                        t_fg+=1;
                        t_daan+=1;
                        fg[t_fg]=f_f;
                    }
                    else
                    {

                        while(f_f/10<=fg[t_fg]/10&&fg[t_fg]!=0)
                        {
                            t_daan-=1;
                            switch(fg[t_fg])
                            {
                                case('+'): daan[t_daan]+=daan[t_daan+1]; break;
                                case('-'): daan[t_daan]-=daan[t_daan+1]; break;
                                case('*'): daan[t_daan]*=daan[t_daan+1]; break;
                                case('/'):
                                    if(daan[t_daan+1]==0)
                                    {
                                        err_mo(3);
                                        goto main_loop;
                                    }
                                    daan[t_daan]/=daan[t_daan+1]; break;
                            }
                            daan[t_daan+1]=0;
                            t_fg-=1;
                        }
                        t_fg+=1;
                        t_daan+=1;
                        fg[t_fg]=f_f;
                    }
                }




            }



            //得出答案，现在显示
            w_com(0x80+0x40+sta);
            w_com(0x0c);
            w_com(0x04);
            daan[0]*=100;
            for(l=0;tt>1;l++)
            {
                w_data(0x30+(char)((int)(daan[0]/pow(10,l))%10));
                if(l==1)
                    w_data('.');
            }







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































