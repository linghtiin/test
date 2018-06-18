#include<iostream>

#define pi 3.1415926

using namespace std;



class space1
{
public:
    space1(){}
    virtual double cubage()=0;
protected:
//    int nuber;
private:
};

class cube:public space1
{
public:
    cube();
    cube(double x):len(x){}

    double cubage();
protected:
    double len;
private:
};

class sphere:public space1
{
public:
    sphere();
    sphere(double x):rad(x){}

    double cubage();
protected:
    double rad;
private:
};

double cube::cubage()
{
    return len*len*len;
}

double sphere::cubage()
{
    return rad*rad*rad*pi*3/4;
}

int main()
{
    space1 *p;
    cube a(3);
    sphere b(5);

    p=&a;
    cout<<p->cubage()<<endl;
    p=&b;
    cout<<p->cubage()<<endl;

    return 0;
}
