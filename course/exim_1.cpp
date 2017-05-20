#include<stdio.h>

#define N 1000

int main ()
{
	char n[N],m[N],o[N],p[N]={"\0"};
	int i,j=0;
	
	scanf("%s",n);
	scanf("%s",m);
	scanf("%s",o);
	
	for(i=0;i<N&&n[i]!='\0';i++)
	    for(j=0;j<N&&m[j]!='\0'&&n[i+j]==m[j];j++)
	      if(m[j]=='\0')
	        for()
	
	
	printf("%s",p);
	
	return 0;
}
