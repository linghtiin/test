#include <iostream>
#include <cstdio>
using namespace std;

int timecount(double VUL, double D);

int main(){

    #ifdef ONLINE_JUDGE
    freopen("input.txt","r",stdin);
    freopen("output.txt","w",stdout);
    #endif // ONLINE_JUDGE
    double VUL,D;
    int t;
    while(cin >> VUL >> D){
        t = timecount(VUL,D);
        cout << t << endl;
    }
    return 0;
}

int timecount(double VUL,double D){
    double d_vul = 0;
    int t = 0;
    for (int i=1;VUL>d_vul;i++){
        d_vul+= i*D;
        if (VUL>d_vul)
            t += i+1;
        else
            t += i + int(VUL-d_vul);
    }
    return t;
}
