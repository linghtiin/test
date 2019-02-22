/*
    计算数的高次幂,只取得其后3位尾数.

*/

#include<iostream>

using namespace std;

int power_num_en(int x,int i);

int main()
{
    int x,i,n;

    cin>>x>>i;
    n=power_num_en(x,i);
    cout<<n<<endl;

    return 0;
}


int power_num_en(int x,int i)
{
    int n;
    n=0;
    if (i>1)
        n=power_num_en(x,i-1)*x %10000;
    else if (i==1)
        n=x%10000;
    else
        return -1;

    return n;
}
