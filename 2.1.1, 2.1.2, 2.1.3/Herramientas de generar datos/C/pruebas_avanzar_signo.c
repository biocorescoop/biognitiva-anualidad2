#include <stdio.h>
#include <stdlib.h>
#include "matanid.h"

#define CMAX 5000 /* maximo de primos */
#define Nanid 7  /* nivel de anidación */
#define MAX_MATRICES_GENERADAS 1000 //maximos de matrices a generar
#define MAX_DIGITOS_PRIMOS 10
#define MAT_X_BLOQUE 1024

#define ARCHIVO_3X3 matrices_3x3.csv
#define ARCHIVO_5X5 matrices_5x5.csv
#define ARCHIVO_7X7 matrices_7x7.csv
#define ARCHIVO_9X9 matrices_9x9.csv
#define ARCHIVO_11X11 matrices_11x11.csv




int main(int argc, char *argv[]) {
	int signo[5];
	for (int i = 0; i < 5; i++) signo[i] = 0;
	
	do {
		mostrar_array(signo, 5);
		printf("Numero: %d\n", num_signo(signo, 5));
	} while (avanzar_signo(signo, 5));
	
	return 0;
}
