#ifndef COMPLEX_H
#define COMPLEX_H

#include<iostream>

class complex
{
    public:
        /** Default constructor */
        complex(double re,double im);
        /** Copy constructor
         *  \param other Object to copy from
         */
        complex(const complex& other);
        /** Assignment operator
         *  \param other Object to assign from
         *  \return A reference to this
         */
        complex& operator=(const complex& other);
        complex& operator++();
        complex operator++(int);
        complex& operator--();
        complex operator--(int);
        complex& operator~();

        friend complex operator+(complex& c1,complex& c2);
        friend complex operator-(complex& c1,complex& c2);

        friend std::ostream& operator<<(std::ostream& out,complex& c);


        /** Access real
         * \return The current value of real
         */
        double Getreal() { return real; }
        /** Set real
         * \param val New value to set
         */
        void Setreal(double val) { real = val; }
        /** Access imag
         * \return The current value of imag
         */
        double Getimag() { return imag; }
        /** Set imag
         * \param val New value to set
         */
        void Setimag(double val) { imag = val; }

    protected:

    private:
        double real; //!< Member variable "real"
        double imag; //!< Member variable "imag"
};

#endif // COMPLEX_H
