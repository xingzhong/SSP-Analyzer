
void work(double *x, double *y, double *h){
    int i;
    for (i=0; i < 10; i++){
        y[i] = x[10-i]*h[i];
    }
}
