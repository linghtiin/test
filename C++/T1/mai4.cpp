#include <stdio.h>
#include <stdlib.h>

typedef struct student
{
    int num;
    int sre;
    char name[10];
    struct student *next;
}STU;

STU* creat(STU *h,int n)
{
    STU *p,*pnew;
    p=h;
    for(int i=0;i<n;i++)
    {
        pnew=(STU*)malloc(sizeof (STU));
        if(pnew==NULL)
        {
            printf("error 1");
            exit(1);
        }
        scanf("%s%d%d",pnew->name,&pnew->num,&pnew->sre);
        p->next=pnew;
        p=p->next;
    }
    p->next=NULL;
    return h;
}



STU* into(STU* h,int n)
{
    STU *p,*pnew;
    int i;
    p=h;
    i=1;
    while(i<n&&p!=NULL)
    {
        p=p->next;
        i++;
    }

    pnew=(STU*)malloc(sizeof (STU));
    scanf("%s%d%d",pnew->name,&pnew->num,&pnew->sre);
    pnew->next=p->next;
    p->next=pnew;

    return h;
}



void print_list(STU *h)
{
    STU *p;
    p=h->next;

    printf("the list is:\n");
    while(p!=NULL)
    {
        printf("%d\t%s\t%d\n",p->num,p->name,p->sre);
        p=p->next;
    }

}

int main()
{
    STU *head,*p;
    int n,i;

    head=(STU*)malloc(sizeof (STU));

    scanf("%d",&n);
    p=creat(head,n);

    scanf("%d",&i);
    p=into(head,i);

    print_list(head);

    return 0;
}
