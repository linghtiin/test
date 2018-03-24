/*
    简单成绩分析(结构体)

    取得最高分
    取得最低分


*/

#include<stdio.h>
#include<stdlib.h>

#define N 3

typedef struct node
{
	char name[10];
	int s1;
	int s2;
	int s3;
	float ave;
	struct node *next;
}NODE;

NODE st[N];

int main()
{
    int i;
    for(i=0;i<N;i++)
    {
        printf("请按顺序输入姓名，数学成绩，语文成绩，英语成绩：\n");
		scanf("%s%d%d%d",st[i].name,&st[i].s1,&st[i].s2,&st[i].s3);
        st[i].ave=(st[i].s1+st[i].s2+st[i].s3)/3.0;
    }

    NODE *m=&st[0];
    for(i=0;i<N;i++)
    {
        if(st[i].ave>m->ave)
        m=&st[i];
    }
    printf("平均分最高的是:\n");
    printf("%s\t%d\t%d\t%d\t%.2f\n",m->name,m->s1,m->s2,m->s3,m->ave);

    m=&st[0];
    for(i=0;i<N;i++)
    {
        if(st[i].ave<m->ave)
        m=&st[i];
    }
    printf("平均分最低的是:\n");
    printf("%s\t%d\t%d\t%d\t%.2f\n",m->name,m->s1,m->s2,m->s3,m->ave);


    return 0;

}
