#ifndef LCD_H_INCLUDED
#define LCD_H_INCLUDED


//ͷ�ļ�����
// #include<reg51.H>
#include <STC89C5xRC.H>


//�ض���
#ifndef uchar
#define uchar unsigned char
#endif

#ifndef uint
#define uint unsigned int
#endif

//PIN�ڶ���
#define lcd_data P0
#define keyline P1
sbit en=P2^7;
sbit rw=P2^5;
sbit rs=P2^6;



//��������
void delayms(uint xms);
void keyscan();
void init();
void w_com(uchar com);
void w_data(uchar dat);
uchar re_data();
uchar re_sta();

#endif // LCD_H_INCLUDED
