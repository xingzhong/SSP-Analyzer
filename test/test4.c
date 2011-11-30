
void work1(double *x, double *y, double *h){
    int i;
    for (i=0; i < 10; i++){
        y[i] = x[10-i]*h[i];
    }
}
void work2(double *x, double *y, double h){
    int i;
    for (i=0; i < 10; i++){
        y[i] = x[10-i]+h;
    }
}
void work3(double *x, double *y, double *h){
    int i, j ;
    for (i=0; i < 10; i++){
        y[i] = 0;
        for (j=i; j<10; j++){
            y[i] += x[i]*h[10-i];
        }
    }
}
