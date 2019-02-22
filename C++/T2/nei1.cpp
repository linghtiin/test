/*
    ���ֵ������
    ֧�ַ��Ÿ�����
    �������֧��1-6;

*/


#include<iostream>
#include<iomanip>
#include<cmath>
#include<cstdlib>

using namespace std;


int numlen(double num);         //ȡ���������ֳ���
int numlen_e(double num);         //ȡ��С�����ֳ���
double renum_d(double num);     //���ֵ����Ӻ���

int main()
{
    double num;

    cin>>num;
    num=renum_d(num);
    cout <<setiosflags(ios::fixed);         //ֻ�����������ú�setprecision��������С����λ����
    cout<<setprecision(6)<<num<<endl;

    return 0;
}


double renum_d(double num)
{
    int i;
    int l,l_e;
    double rnum=0,t=0;

    l=numlen(num);
    l_e=numlen_e(num);

    t=long(num);
    while(l>0)
    {
        rnum=rnum+long(t/ pow(10,l-1)+1e-7) % 10 * pow(10,-l);
        l--;
    }

    t=num-long(num)+1e-7;
    while(l_e>0)
    {
        rnum=rnum+long(t*pow(10,l_e)+1e-7) %10 * pow(10,l_e-1);
        l_e--;
    }

    return rnum;
}


int numlen(double num)
{
    int i=0;
    num=long(num);
    do
    {
        num=num/10;
        i++;
    }while(fabs(long(num))>0);
    return i;
}

int numlen_e(double num)
{
    int i=-1;
    num=num-long(num)+1e-7;
    do
    {
        num=num*10;
        i++;
    }while(fabs(long(num)%10)>0);
    return i;
}


