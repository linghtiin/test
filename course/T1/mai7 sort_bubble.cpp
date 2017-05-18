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
    int i,j,f=1;
    List t;
    for(i=0;i<n;i++)
        while(i<n&&f=1)
        {
            f=0;
            for(j=0;j<n-i;j++)
            {
                if(l[j]->key>l[j+1]->key)
                {
                    t=l[j];
                    l[j]=l[j+1];
                    l[j+1]=t;
                    f=1;
                }
            }
        }

        
}

int main()
{
    

    return 0;

}
