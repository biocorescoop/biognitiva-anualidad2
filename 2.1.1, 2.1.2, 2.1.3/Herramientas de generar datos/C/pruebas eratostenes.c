#include <stdio.h>
#include <stdlib.h>

#define CMAX 5000 /* maximo de primos */
#define Nanid 7  /* nivel de anidación */
#define MAX_MATRICES_GENERADAS 1000 //maximos de matrices a generar
#define MAX_DIGITOS_PRIMOS 10

#define ARCHIVO_3X3 matrices_3x3.csv
#define ARCHIVO_5X5 matrices_5x5.csv
#define ARCHIVO_7X7 matrices_7x7.csv
#define ARCHIVO_9X9 matrices_9x9.csv
#define ARCHIVO_11X11 matrices_11x11.csv

/* Utilizamos la Criba de Erastótenes (https://es.wikipedia.org/wiki/Criba_de_Erat%C3%B3stenes)
   para buscar todos los primos hasta el doble del máximo central posible */
void eratostenes(char esprimo [], int cmax) {
	// esprimo tiene tamaño cmax*2
	int k = 0;
	int j = 0;
	while (k < cmax*2) {
		esprimo[k] = 1;
		k++;
	}
	esprimo[0] = 0;
	esprimo[1] = 0;
	k = 2;
	while (k*k <= (cmax*2)) {
		/* Si ya hemos eliminado este número continuamos */
		if (esprimo[k] == 0) {
			k++;
			continue;
		}
		j = 2*k;
		while (j < (cmax*2)) {
			/* Eliminamos este número, ya que es compuesto */
			esprimo[j] = 0;
			/* Incrementamos j en i unidades porque queremos tachar todos los múltiplos */
			j = j + k;
		}
		k++;
	}
}

int cuantos_primos(char esprimo [], int elementos) {
	int k;
	int numprimos = 0;
	for (k = 0; k < elementos; k++) {
		numprimos = numprimos + esprimo[k];
	}
	return numprimos;
}

void cuales_primos(char esprimo [], int elementos) {
	int k;
	for (k = 0; k < elementos; k++) {
		if (esprimo[k] == 1) {
			printf("%d ", k);
		}
	}
	printf("\n");
}

int main(int argc, char *argv[]) {
	int cmax = 0;
	
	printf("Hay %d argumentos\n", argc);
	
	printf("%s %s\n", argv[0], argv[1]);
	
	cmax = CMAX;
	char esprimo[cmax*2];
	
	eratostenes(esprimo, cmax);
	
	int numprimos = cuantos_primos(esprimo, cmax*2);
	
	printf("Se han encontrado %d primos\n", numprimos);
	
	cuales_primos(esprimo, cmax*2);
	return 0;
}
