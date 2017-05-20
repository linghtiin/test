#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define N 1000

typedef struct my_queue
{
    char v[N];
    int f;
    int r;
}QUE;

void init(QUE *q);
void add_queue(QUE *q,char x);
char del_queue(QUE *q);


int main ()
{
	char n[N],m[N],o[N],*p,*p1;
	QUE *q,q1;

	int i,j,k,l,l_m;


	q=&q1;

	init(q);

	scanf("%s",n);
	scanf("%s",m);
	scanf("%s",o);

	l=strlen(n);
	l_m=strlen(m);
	p=n+1;

	for(i=0;i<=l;i++)
    {
        p1=strstr(p-1,m);
        if(p1!=NULL)
        {
            k=p1-p;
            printf("%d\n",k);
            if(k==-1&&p!=n+1)
                q->r=q->r-1;
            for(j=0;j<k;j++)
                add_queue(q,p[j]);
            for(j=0;o[j]!='\0';j++)
                add_queue(q,o[j]);
            p=p1+l_m;
        }
        else
        {
            for(j=0;p[j]!='\0';j++)
                add_queue(q,p[j]);
            break;
        }
    }




    while(q->f!=q->r)
        printf("%c",del_queue(q));
    printf("\n");

	return 0;
}



void init(QUE *q)
{
    q->f=-1;
    q->r=-1;
}

void add_queue(QUE *q,char x)
{
    if((q->r+1)%N==q->f)
    {
        printf("the queue is full.\n");
        exit(1);
    }
    else
    {
        q->r=(q->r+1)%N;
        q->v[q->r]=x;
    }
}

char del_queue(QUE *q)
{
    char x;
    if(q->f==q->r)
    {
        printf("the queue is empty.\n");
        exit(2);
    }
    else
    {
        q->f=(q->f+1)%N;
        x=q->v[q->f];
    }
    return x;
}
