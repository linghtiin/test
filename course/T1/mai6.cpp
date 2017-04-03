#include <stdio.h>
#include <stdlib.h>

#define N 30

typedef struct my_queue
{
    int v[N];
    int f;
    int r;
}QUE;
void init(QUE *q)
{
    q->f=-1;
    q->r=-1;
}
void add_queue(QUE *q,int x)
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


int del_queue(QUE *q)
{
    int x;
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



int main()
{
    QUE q1,*p;
    int x,i;

    p=&q1;

    init(p);
    while(1)
    {
        scanf("%d%d",&i,&x);
        if(i==1)
            add_queue(p,x);
        else
        {
            while(p->f!=p->r)
                printf("%d\t",del_queue(p));
            printf("\n");
        }
    }
}


