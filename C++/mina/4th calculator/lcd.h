#ifndef LCD_H_INCLUDED
#define LCD_H_INCLUDED


//头文件包含
// #include<reg51.H>
#include <STC89C5xRC.H>


//重定义
#ifndef uchar
#define uchar unsigned char
#endif

#ifndef uint
#define uint unsigned int
#endif

//PIN口定义
#define lcd_data P0
#define keyline P1
sbit en=P2^7;
sbit rw=P2^5;
sbit rs=P2^6;



//函数声明
void delayms(uint xms);
void keyscan();
void init();
void w_com(uchar com);
void w_data(uchar dat);
uchar re_data();
uchar re_sta();

#endif // LCD_H_INCLUDED
