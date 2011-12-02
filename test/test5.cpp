#include <iostream>
using namespace std;
int work(double *x, double *y){
    for (int i=0; i<10; i++)
        y[i] = x[i] + 10;
}
