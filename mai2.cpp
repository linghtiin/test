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

NODE* creat (int n)
{
	NODE *head,*p;
	head=(NODE*)malloc(sizeof(NODE));
	p=head;
	int i=1;
	while(1)
	{
		printf("请按顺序输入姓名，数学成绩，语文成绩，英语成绩：\n");
		scanf("%s%d%d%d",p->name,&p->s1,&p->s2,&p->s3);
		p->ave=(p->s1+p->s2+p->s3)/3.0;
		if(i<n)
		{
			p->next=(NODE*)malloc(sizeof(NODE));
				if(p->next==NULL)
				{
					printf("无法申请内存！！");
					exit(1);
				}
			p=p->next;
			i++;
		}
		else
		{
		    p->next=NULL;
			return head;
		}


	}

}

void smax(NODE *head,int i)
{
    NODE *p,*m;
    p=head;
    m=head;

    while(p!=NULL)
    {
        switch(i)
        {
            case(1):
                if(p->s1>m->s1)
                    m=p;
                break;
            case(2):
                if(p->s2>m->s2)
                    m=p;
                break;
            case(3):
                if(p->s3>m->s3)
                    m=p;
                break;
            case(4):
                if(p->ave>m->ave)
                    m=p;
                break;
        }
        p=p->next;
    }
    printf("平均分最高的是:\n");
    printf("%s\t%d\t%d\t%d\t%.2f\n",m->name,m->s1,m->s2,m->s3,m->ave);
}

void smin(NODE *head,int i)
{
    NODE *p,*m;
    p=head;
    m=head;

    while(p!=NULL)
    {
        switch(i)
        {
            case(1):
                if(p->s1<m->s1)
                    m=p;
                break;
            case(2):
                if(p->s2<m->s2)
                    m=p;
                break;
            case(3):
                if(p->s3<m->s3)
                    m=p;
                break;
            case(4):
                if(p->ave<m->ave)
                    m=p;
                break;
        }
        p=p->next;
    }
    printf("平均分最低的是:\n");
    printf("%s\t%d\t%d\t%d\t%.2f\n",m->name,m->s1,m->s2,m->s3,m->ave);
}

int main()
{
    NODE *head,*p;
    head=creat(N);
    smax(head,4);
    smin(head,4);

    return 0;
}
