/*
    结构体关键字排序
    冒泡算法排序
    快速排序

*/

#include<stdio.h>
#include<stdlib.h>

#define N 7






typedef struct LIST
{
    int key;        //排序用关键字
    char info[20];
    char name[5];
}List;










//冒泡算法排序
void bubble_sort(List l[],int n)
{
    int i=1,j,f=1;
    List t;
    while(i<n&&f==1)
    {
        f=0;
        for(j=1;j<=n-i;j++)
            if(l[j].key>l[j+1].key)
            {
                t=l[j];
                l[j]=l[j+1];
                l[j+1]=t;
                f=1;
            }
    i++;
    }


}


//快速排序
void Qsort(List l[],int low,int high)
{
    int part(List l[],int i,int j);

    int m;
    if(low<high){
        m = part(l,low,high);
        Qsort(l,low,m-1);
        Qsort(l,m+1,high);

    }
}

int part(List l[],int i,int j)
{
    int key;
    l[0]=l[i];
    key=l[0].key;
    while(i<j){
        while(i<j&&key<l[j].key)
            j--;
        l[i]=l[j];
        while(i<j&&key>=l[i].key)
            i++;
        l[j]=l[i];

    }
    l[i]=l[0];
    return i;
}

int main()
{
    List l[N+1];
    int i;
    for(i=1;i<=N;i++)
        scanf("%d%s%s",&l[i].key,l[i].name,l[i].info);
    Qsort(l,1,N);
    for(i=1;i<=N;i++)
        printf("%d\t%s\t%s\n",l[i].key,l[i].name,l[i].info);

    return 0;

}
