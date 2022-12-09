#include <stdio.h>
#include <math.h>


// Somma primi n numeri naturali
int sum_n(int n){

  int somma = 0;

  int i;
  for( i=0; i<=n; ++i) 
    somma += i;

  return somma; 
}



// Somma delle radici quadrate dei primi n numeri naturali
double sum_sqrtn(int n){

  double somma = 0;

  int i;
  for( i=0; i<=n; ++i) 
    somma += sqrt(i);

  return somma; 
}



// Somma degli elementi di un array
// *av: puntatore ad un array di double
// n  : numero di elementi dell'array
double sum_array(double *av, int n){

  double somma = 0;

   int i;
  for(i=0; i<n; ++i)
    somma += av[i];
  
  return somma;  
}



