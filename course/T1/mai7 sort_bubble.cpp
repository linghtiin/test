#include<stdio.h>
#include<stdlib.h>

#define N 3

typedef struct LIST
{
    int key;
    char info[20];
    char name[5];
}List;

void bubble_sort(List l[],int n)
{
    int i=1,j,f=1;
    List t;
    while(i<n&&f==1)
    {
        f=0;
        for(j=1;j<=n-i;j++)
            if(l[j]->key>l[j+1]->key)
            {
                t=l[j];
                l[j]=l[j+1];
                l[j+1]=t;
                f=1;
            }
    i++;
    }

        
}

void Qsort(List l[],int low.int high)
{
    int m;
    if(low<high){
        m=part(l,low,high);
        Qsort(l,low,m-1);
        Qsort(l,m+1,high);
        
    }
}

void part(List l[],int i,int j)
{
    int key;
    l[0]=l[i];
    key=l[0]->key;
    while(i<j){
        while(i<j&&key>=l[j]->key)
            j--;
        l[i]=l[j];
        while(i<j&&key<l[i]->key)
            i++;
        l[j]=l[i];
        
    }
    l[i]=l[0];
    return i;
}

int main()
{
    

    return 0;

}