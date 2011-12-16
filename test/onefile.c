/* the following function is for sspcl I/O recognition test */
/* collect from the http://www.ece.rutgers.edu/~orfanidi/intro2sp/  */
/* Manually label the output label as OUTPUT */

/* fir.c - FIR filter in direct form */

double fir(M, h, w, x)                       /* Usage: y = fir(M, h, w, x); */
double *h, *w, x;                            /* \(h\) = filter, \(w\) = state, \(x\) = input sample */
int M;                                       /* \(M\) = filter order */
{                        
       int i;
       double OUTPUT;                             /* output sample */

       w[0] = x;                             /* read current input sample \(x\) */

       for (OUTPUT=0, i=0; i<=M; i++)
              OUTPUT += h[i] * w[i];              /* compute current output sample \(y\) */

       for (i=M; i>=1; i--)                  /* update states for next call */
              w[i] = w[i-1];                 /* done in reverse order */

       return OUTPUT;
}


/* dir.c - IIR filtering in direct form */

double dir(M, a, L, b, OUTPUT, v, x)           /* usage: y = dir(M, a, L, b, w, v, x); */
double *a, *b, *OUTPUT, *v, x;                 /* \(v,w\) are internal states */
int M, L;                                 /* denominator and numerator orders */
{
       int i;

       v[0] = x;                          /* current input sample */
       OUTPUT[0] = 0;                          /* current output to be computed */

       for (i=0; i<=L; i++)               /* numerator part */
              OUTPUT[0] += b[i] * v[i];

       for (i=1; i<=M; i++)               /* denominator part */
              OUTPUT[0] -= a[i] * OUTPUT[i];

       for (i=L; i>=1; i--)               /* reverse-order updating of \(v\) */
              v[i] = v[i-1];

       for (i=M; i>=1; i--)               /* reverse-order updating of \(w\) */
              OUTPUT[i] = OUTPUT[i-1];

       return OUTPUT[0];                       /* current output sample */
}


/* conv.c - convolution of x[n] with h[n], resulting in y[n] */

//#include <stdlib.h>                       /* defines max( ) and min( ) */

//void conv(M, h, L, x, OUTPUT)
//double *h, *x, *OUTPUT;                        /* \(h,x,y\) = filter, input, output arrays */
//int M, L;                                 /* \(M\) = filter order, \(L\) = input length */
//{
//       int n, m;
//
//       for (n = 0; n < L+M; n++)
//              for (OUTPUT[n] = 0, m = max(0, n-L+1); m <= min(n, M); m++)
//                     OUTPUT[n] += h[m] * x[n-m];
//}


/* sos.c - IIR filtering by single second order section */

double sos(a, b, w, x)                    /* \(a, b, w\) are 3-dimensional */
double *a, *b, *w, x;                     /* \(a[0]=1\) always */
{
       double OUTPUT;

       w[0] = x - a[1] * w[1] - a[2] * w[2];
       OUTPUT = b[0] * w[0] + b[1] * w[1] + b[2] * w[2];

       w[2] = w[1];
       w[1] = w[0];

       return OUTPUT;
}


/* tap.c - i-th tap of circular delay-line buffer */

double tap(D, w, p, i)                    /* usage: si = tap(D, w, p, i); */
double *w, *p;                            /* \(p\) passed by value */
int D, i;                                 /* \(i=0,1,\dotsc, D\) */
{
	double OUTPUT = w[(p - w + i) % (D + 1)];
	return OUTPUT;
}



/* delay.c - delay by D time samples */

void delay(D, OUTPUT)                          /* \(w[0]\) = input, \(w[D]\) = output */
int D;
double *OUTPUT;
{
       int i;

       for (i=D; i>=1; i--)               /* reverse-order updating */
              OUTPUT[i] = OUTPUT[i-1];

}


/* dac.c - bipolar two's complement D/A converter */

double dac(b, B, R)
int *b, B;                         /* bits are dimensioned as \(b[0], b[1], \dotsc, b[B-1]\) */
double R;
{
       int i;
       double OUTPUT = 0;

       b[0] = 1 - b[0];                          /* complement MSB */

       for (i = B-1; i >= 0; i--)                /* H\"orner's rule */
          OUTPUT = 0.5 * (OUTPUT + b[i]);

       OUTPUT = R * (OUTPUT - 0.5);                    /* shift and scale */

       b[0] = 1 - b[0];                          /* restore MSB */

       return OUTPUT;
}


/* bitrev.c - bit reverse of a B-bit integer n */

#define two(x)       (1 << (x))                  /* \(2\sp{x}\) by left-shifting */

int bitrev(n, B)
int n, B;
{
       int m, OUTPUT;

       for (OUTPUT=0, m=B-1; m>=0; m--)
          if ((n >> m) == 1) {                   /* if \(2\sp{m}\) term is present, then */
             OUTPUT += two(B-1-m);                    /* add \(2\sp{B-1-m}\) to \(r\), and */
             n -= two(m);                        /* subtract \(2\sp{m}\) from \(n\) */
             }

       return(OUTPUT);
}


/* corr.c - sample cross correlation of two length-N signals */

void corr(N, x, y, M, OUTPUT)                  /* computes \(R[k]\), \(k = 0, 1,\dotsc, M\) */
double *x, *y, *OUTPUT;                        /* \(x,y\) are \(N\)-dimensional */
int N, M;                                 /* \(R\) is \((M+1)\)-dimensional */
{
       int k, n;

       for (k=0; k<=M; k++)
              for (OUTPUT[k]=0, n=0; n<N-k; n++)
                     OUTPUT[k] += x[n+k] * y[n] / N;
}


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
void work2(double *x, double *OUTPUT, double h){
    int i;
    for (i=0; i < 10; i++){
        OUTPUT[i] = x[10-i]+h;
    }
}
void work3(double *x, double *OUTPUT, double *h){
    int i, j ;
    for (i=0; i < 10; i++){
        OUTPUT[i] = 0;
        for (j=i; j<10; j++){
            OUTPUT[i] += x[i]*h[10-i];
        }
    }
}

double *trinomial_mult( int n, double *b, double *c )
{
    int i, j;
    double *OUTPUT;

    OUTPUT = (double *)calloc( 4 * n, sizeof(double) );
    if( OUTPUT == NULL ) return( NULL );

    OUTPUT[2] = c[0];
    OUTPUT[3] = c[1];
    OUTPUT[0] = b[0];
    OUTPUT[1] = b[1];
  
    for( i = 1; i < n; ++i )
    {
	OUTPUT[2*(2*i+1)]   += c[2*i]*OUTPUT[2*(2*i-1)]   - c[2*i+1]*OUTPUT[2*(2*i-1)+1];
	OUTPUT[2*(2*i+1)+1] += c[2*i]*OUTPUT[2*(2*i-1)+1] + c[2*i+1]*OUTPUT[2*(2*i-1)];

	for( j = 2*i; j > 1; --j )
	{
	    OUTPUT[2*j]   += b[2*i] * OUTPUT[2*(j-1)]   - b[2*i+1] * OUTPUT[2*(j-1)+1] + 
		c[2*i] * OUTPUT[2*(j-2)]   - c[2*i+1] * OUTPUT[2*(j-2)+1];
	    OUTPUT[2*j+1] += b[2*i] * OUTPUT[2*(j-1)+1] + b[2*i+1] * OUTPUT[2*(j-1)] +
		c[2*i] * OUTPUT[2*(j-2)+1] + c[2*i+1] * OUTPUT[2*(j-2)];
	}

	OUTPUT[2] += b[2*i] * OUTPUT[0] - b[2*i+1] * OUTPUT[1] + c[2*i];
	OUTPUT[3] += b[2*i] * OUTPUT[1] + b[2*i+1] * OUTPUT[0] + c[2*i+1];
	OUTPUT[0] += b[2*i];
	OUTPUT[1] += b[2*i+1];
    }

    return( OUTPUT );
}


/**********************************************************************
  FFT - calculates the discrete fourier transform of an array of double
  precision complex numbers using the FFT algorithm.

  c = pointer to an array of size 2*N that contains the real and
    imaginary parts of the complex numbers. The even numbered indices contain
    the real parts and the odd numbered indices contain the imaginary parts.
      c[2*k] = real part of kth data point.
      c[2*k+1] = imaginary part of kth data point.
  N = number of data points. The array, c, should contain 2*N elements
  isign = 1 for forward FFT, -1 for inverse FFT.
*/

void FFT( double *OUTPUT, int N, int isign )
{
  int n, n2, nb, j, k, i0, i1;
  double wr, wi, wrk, wik;
  double d, dr, di, d0r, d0i, d1r, d1i;
  double *cp;

  j = 0;
  n2 = N / 2;
  for( k = 0; k < N; ++k )
  {
    if( k < j )
    {
      i0 = k << 1;
      i1 = j << 1;
      dr = OUTPUT[i0];
      di = OUTPUT[i0+1];
      OUTPUT[i0] = OUTPUT[i1];
      OUTPUT[i0+1] = OUTPUT[i1+1];
      OUTPUT[i1] = dr;
      OUTPUT[i1+1] = di;
    }
    n = N >> 1;
    while( (n >= 2) && (j >= n) )
    {
      j -= n;
	  n = n >> 1;
    }
    j += n;
  }

  for( n = 2; n <= N; n = n << 1 )
  {
    wr = cos( 2.0 * M_PI / n );
    wi = sin( 2.0 * M_PI / n );
    if( isign == 1 ) wi = -wi;
    cp = OUTPUT;
    nb = N / n;
    n2 = n >> 1;
    for( j = 0; j < nb; ++j )
    {
      wrk = 1.0;
      wik = 0.0;
      for( k = 0; k < n2; ++k )
      {
        i0 = k << 1;
        i1 = i0 + n;
        d0r = cp[i0];
        d0i = cp[i0+1];
        d1r = cp[i1];
        d1i = cp[i1+1];
        dr = wrk * d1r - wik * d1i;
        di = wrk * d1i + wik * d1r;
        cp[i0] = d0r + dr;
        cp[i0+1] = d0i + di;
        cp[i1] = d0r - dr;
        cp[i1+1] = d0i - di;
        d = wrk;
        wrk = wr * wrk - wi * wik;
        wik = wr * wik + wi * d;
      }
      cp += n << 1;
    }
  }
}
