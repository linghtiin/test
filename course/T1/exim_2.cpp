/*

    输入music-?.MP3与n;
    输出music-?+1.MP3至music-?+n.MP3的字符串.

*/

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
