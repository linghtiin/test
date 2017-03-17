#include<reg51.h>

#define KEY P1
#define LCD P2

typedef unsigned int u16 ;
typedef unsigned char u8 ;


void delayms (u16 xms);
void keyscan();
void init();

u8 key,t[20]; //其十位用于错误检测
double n[20],daan;

void main()
{
 u8 l=0,f=0;
 init();
 keyscan();
 if(key%4==0)
 {
  switch(key)
  {
   case(4): t[f]=1;f++;l=0;break;
   case(8): t[f]=2;f++;break;
   case(12): t[f]=3;  break;
   case(16): t[f]=4;  break;

    
  }
 }
 else if(key==13)
 {
  for...
   n[]==0
   f=0
   
 }
 
 else if(key==15)
 {
  if(l==1...)
   err=1;
  daan=n[0]
   for(u8 i;i<=f;i++)
    switch t[i]
     case 1:
      daan+n[i
     case 2:
      daan
      ...
 }
 else
 {
  if(key==14)
   key=0;
  n[f]*=10;
  n[f]+=key;
  key=0;
  l=1;
 }

}















