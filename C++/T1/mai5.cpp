#include <stdio.h>
#include <stdlib.h>

#define N 30

typedef struct my_stack
{
    int v[N];
    int top;
}STA;

typedef struct my_snode
{
    int data;
    struct my_snode *next;

}SNO;

void init(STA *s)
{
    s->top=-1;
}

void init(SNO *top)
{
    top->next=NULL;
}

void push(STA *s,int x)
{
    if(s->top==N-1)
    {
        printf("the stack is full.\n");
        exit(1);
    }
    else
    {
        s->top=s->top+1;
        s->v[s->top]=x;
    }
}


int pop(STA *s)
{
    int x;
    if(s->top<=-1)
    {
        printf("the stack is empty.\n");
        exit(2);
    }
    else
    {
        x=s->v[s->top];
        s->top=s->top-1;
    }
    return x;
}


void push(SNO *top,int x)
{
    SNO *pnew;
    pnew=(SNO*)malloc(sizeof(SNO));
    if(pnew==NULL)
    {
        printf("the stack is full.\n");
        exit(1);
    }
    else
    {
        pnew->data=x;
        pnew->next=top->next;
        top->next=pnew;
    }


}

int pop(SNO* top)
{
    int x;
    SNO *p;
    p=top->next;
    if(p==NULL)
    {
        printf("the stack is empty.\n");
        exit(2);
    }
    else
    {
        x=p->data;
        top->next=p->next;
        free(p);
    }
    return x;
}
















int main()
{
    SNO s1,*p;


    int x,i;

    p=&s1;
    init(p);
    while(1)
    {
        scanf("%d%d",&i,&x);
        if(i==1)
            push(p,x);
        else
        {
            while(p->next!=NULL)
                printf("%d\t",pop(p));
            printf("\n");
        }


    }

}
