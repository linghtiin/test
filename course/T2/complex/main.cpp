#include"m_complex.h"


using namespace std;

int main()
{
    cout << "Hello world!" << endl;
    complex c1(1,3),c2(2,6),c3(c1);
    c3=c1+c2;
    cout<<c3.Getreal()<<"+"<<c3.Getimag()<<"i"<<endl;
    c3=c1++;
    cout<<c3<<endl;
    c3=++c2;
    cout<<c3<<endl;
    c3=~c1;
    cout<<c3<<endl;
    c3=c1--;
    cout<<c3<<endl;
    c3=--c2;
    cout<<c3<<endl;
    return 0;
}
