/*
    建立二叉树
        深度遍历


*/
#define STACK_H_INCLUDED


#include <stdio.h>
#include <stdlib.h>
#include "stack.h"

using namespace std;


typedef struct btnode
{
    char data;
    struct btnode* lchild;
    struct btnode* rchild;
}BTD;

void traveltree1(BTD *t)
{
    if(t!=NULL)
    {
        traveltree1(t->lchild);
        printf("%d\t",t->data);
        traveltree1(t->rchild);
    }
}

void traveltree2(BTD *t)
{
    BTD *p;
    SNO s,*top;

    top=&s;
    init(top);
    p=t;

    while(p!=NULL||s.next!=NULL)
    {
        while(p!=NULL)
        {
            push(top,p);
            p=p->lchild;
        }
        if(top->next!=NULL)
        {
            p=pop(top);
            printf("%d\t",p->data);
            p=p->rchild;
        }
    }


}

BTD* ctreat(int a[],int n)
{
    BTD *t,*newnode,*p,*q;
    t=(BTD*)malloc(sizeof(BTD));
    t->data=a[0];
    t->lchild=t->rchild=NULL;

    for(int i=1;i<n;i++)
    {
        newnode=(BTD*)malloc(sizeof(BTD));
        newnode->data=a[i];
        newnode->lchild=newnode->rchild=NULL;

        p=t;
        while(p!=NULL)
        {
            q=p;
            if(newnode->data<p->data)
                p=p->lchild;
            else
                p=p->rchild;
        }
        if(newnode->data<q->data)
            q->lchild=newnode;
        else
            q->rchild=newnode;
    }

    return t;
}


int main()
{
    int a[10];
    BTD* t;
    for(int i=0;i<10;i++)
        scanf("%d",&a[i]);
    printf("\n");

    t=ctreat(a,10);

    traveltree2(t);


    return 0;
}
