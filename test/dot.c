/* dot.c - dot product of two length-(M+1) vectors */

double dot(M, h, w)                            /* Usage: y = dot(M, h, w); */
double *h, *w;                                 /* \(h\) = filter vector, \(w\) = state vector */
int M;                                         /* \(M\) = filter order */
{                        
       int i;
       double OUTPUT;

       for (OUTPUT=0, i=0; i<=M; i++)               /* compute dot product */
              OUTPUT += h[i] * w[i];      

       return OUTPUT;
}

void work1(double *x, double *OUTPUT, double *h){
    int i;
    for (i=0; i < 10; i++){
        OUTPUT[i] = x[10-i]*h[i];
    }
}
