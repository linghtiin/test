#include<stdio.h>

#define N 50
typedef struct student
{
    long int num[N];
    int score[N];
    int len ;
    char name[N][10];
    
}STU;


void inst(STU* l,int i,int num,char name[],int score)
{
    if(i<0||i>N)
        printf("error 1\n");
    else if(i>l.len)
        printf("error 2\n");
        
}


void main()
{
    STU s1;
    int l,n,s;
    char name[10];
    
    char i;
    scanf("%d",&l);
    for(i=0;i<l;i++)
        scanf("%s%d%d",s1.name[i],s1.num[i],s1.score[i]);
    
        
 
}















