#include <stdio.h>
#include <string.h>

#define N 50
typedef struct student
{
    long int num[N];
    int score[N];
    int len;
    char name[N][10];

}STU;


void inst(STU* l,int i,int num,char name[],int score)
{
    if(i<0||i>N)
        printf("error 1\n");
    else if(i>l->len)
        printf("error 2\n");
    else
    {
        int j;
        for(j=l->len-1;j>=i;j--)
        {
            strcpy(l->name[j+1],l->name[j]);
            l->num[j+1]=l->num[j];
            l->score[j+1]=l->score[j];
        }
        l->num[i]=num;
        strcpy(l->name[i],name);
        l->score[i]=score;

        l->len+=1;
    }

}


int main()
{
    STU s1;
    int l,n,s;
    char name[10];

    char i;
    scanf("%d",&s1.len);
    for(i=0;i<s1.len;i++)
        scanf("%s%d%d",s1.name[i],&s1.num[i],&s1.score[i]);

    printf("the new one is:\n");
    scanf("%d",&l);
    scanf("%s%d%d",name,&n,&s);
    inst(&s1,l-1,n,name,s);

    printf("the new list is:\n");
    for(i=0;i<s1.len;i++)
        printf("%s\t%d %d\n",s1.name[i],s1.num[i],s1.score[i]);

    return 0;
}
