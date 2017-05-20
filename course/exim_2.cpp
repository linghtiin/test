#include<stdio.h>

#define N 1000

int main ()
{
	int n;
	int i,j;

	scanf("music-%d.MP3",&n);
	scanf("%d",&i);

	for(j=1;i>0;i--,j++)
	    printf("music-%d.MP3\n",j+n);

	return 0;
}
