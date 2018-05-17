#include "m_complex.h"

using namespace std;

complex::complex(double re=0,double im=0)
{
    real=re;
    imag=im;
    //ctor
}

complex::complex(const complex& other)
{
    //copy ctor
}

complex& complex::operator=(const complex& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    real=rhs.real;
    imag=rhs.imag;
    //assignment operator
    return *this;
}

complex& complex::operator++()
{
    real+=1;
    imag+=1;

    return *this;
}
complex complex::operator++(int)
{
    complex t;
    t=*this;
    real+=1;
    imag+=1;

    return t;
}
complex& complex::operator--()
{
    real-=1;
    imag-=1;

    return *this;
}
complex complex::operator--(int)
{
    complex t;
    t=*this;
    real-=1;
    imag-=1;

    return t;
}
complex& complex::operator~()
{
    imag=-imag;

    return *this;
}



complex operator+(complex& c1,complex& c2)
{
    complex t;
    t.real=c1.real+c2.real;
    t.imag=c1.imag+c2.imag;
    return t;
}
complex operator-(complex& c1,complex& c2)
{
    complex t;
    t.real=c1.real-c2.real;
    t.imag=c1.imag-c2.imag;
    return t;
}

ostream& operator<<(ostream& out,complex& c)
{
    if(c.imag<0)
        out<<c.real<<c.imag<<"i";
    else
        out<<c.real<<"+"<<c.imag<<"i";

    return out;
}
