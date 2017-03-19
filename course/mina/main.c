/*
    单片机实现计算器功能；
    使用LCD602；
    矩阵键盘；
    可实现加减多位加减乘除；

 */

#include <STC89C5xRC.H>

#include "lcd.H"

#define N 20


uchar key,t[N]; //其十位用于错误检测
double n[N],daan;
uchar l,f,e;

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
    l=0,f=0,e=0;
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
                    t[f]=1;f++;l=0;break;
                case(8):
                    t[f]=2;f++;l=0;break;
                case(12):
                    t[f]=3;f++;l=0;break;
                case(16):
                    t[f]=4;f++;l=0;break;
            }
        }
        //清零的分支
        else if(key==13)
        {
            for(uchar i=0;i<f;i++)
            {
                n[i]=0;
                t[i]=0;
            }

            f=0;
            l=0;
        }
        //等于的分支
        else if(key==15)
        {
            if(l==0||e!=0)
            {
                //输出错误
            }

            daan=n[0];

            for(uchar i=0;i<f;i++)
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
                            e=4;
                        else
                            daan/=n[i+1];
                        break;
                    default:
                        e=3;
                }
            }

            //得出答案，现在显示


        }
        //数字的分支
        else
        {
            if(key==14)
                key=0;
            if(l>8)
                e=2;
            n[f]*=10;
            n[f]+=key;
            key=0;
            l+=1;
        }
    }


}































