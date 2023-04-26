#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "matanid.h"

#define CMAX 5000 /* maximo de primos */
#define CMIN 3 /* primer primo en el que empezar */
#define Nanid 7  /* nivel de anidación */
#define MAX_MATRICES_GENERADAS 10000 //maximos de matrices a generar

/*
Creamos un buffer donde ir almacenando las matrices que se generan.
Será una lista de punteros, donde cada uno llevará a un bloque donde se
almacenarán MAT_X_BLOQUE matrices.
*/
char mostramos_matrices = 0;

void imprimir_ayuda(char *argv[]) {
	printf("%s -n nivel -cmin cmin -cmax cmax -i input.csv -o output.csv\n", argv[0]);
}

int main(int argc, char *argv[]) {
	// recorrer argumentos
	int k, i;
	int n = 3;
	int cmax = 0;
	int cmin = CMIN;
	
	char *ppio_archivo_salida;
	ppio_archivo_salida = NULL;
	char *ppio_archivo_entrada;
	ppio_archivo_entrada = NULL;
	
	for (k = 1; k < argc; ++k) {
		if (!strcmp(argv[k], "-h")) {
			imprimir_ayuda(argv);
			return 0;
		}
		if (!strcmp(argv[k], "-n")) {
			sscanf(argv[k+1], "%d", &n);
			++k;
			printf("n = %d\n", n);
			continue;
		}
		if (!strcmp(argv[k], "-cmax")) {
			sscanf(argv[k+1], "%d", &cmax);
			printf("cmax = %d\n", cmax);
			++k;
			continue;
		}
		if (!strcmp(argv[k], "-cmin")) {
			sscanf(argv[k+1], "%d", &cmin);
			printf("cmin = %d\n", cmin);
			++k;
			continue;
		}
		if (!strcmp(argv[k], "-i")) {
			ppio_archivo_entrada = argv[k+1];
			printf("archivo de entrada %s\n", ppio_archivo_entrada);
			++k;
			continue;
		}
		if (!strcmp(argv[k], "-o")) {
			ppio_archivo_salida = argv[k+1];
			printf("archivo de salida %s\n", ppio_archivo_salida);
			++k;
			continue;
		}
		printf("Argumento no identificado %s\n", argv[k]);
	}
	
	inicializar_var_globales(n);
	printf("Variables globales inicializadas\n");
	
	if (ppio_archivo_entrada == NULL) {
		ppio_archivo_entrada = "marcos";
	}
	if (ppio_archivo_salida == NULL) {
		ppio_archivo_salida = "matrices";
	}
	
	FILE *archivo_num_generadas;
	archivo_num_generadas = fopen("num_generadas.csv", "w");
	printf("num_generadas.csv -> %p\n", archivo_num_generadas);
	num_generadas = malloc(sizeof(long int)*(n+1));
	
	FILE *salida_matrices[n];
	char archivo_salida_matrices[strlen(ppio_archivo_salida)+12];
	
	FILE *entrada_marcos[n];
	char archivo_entrada_marcos[strlen(ppio_archivo_entrada)+12];
	
	for (k = 1; k <=n; ++k){
		sprintf(archivo_salida_matrices, "%s_%dx%d.csv", ppio_archivo_salida, 2*k+1, 2*k+1);
		salida_matrices[k-1] = fopen(archivo_salida_matrices, "w");
		
		sprintf(archivo_entrada_marcos, "%s_%dx%d.csv", ppio_archivo_entrada, 2*k+1, 2*k+1);
		entrada_marcos[k-1] = fopen(archivo_entrada_marcos, "r");
		
		if (salida_matrices == NULL) {
			printf("Error al crear el archivo %s\n", archivo_salida_matrices);
			exit(1);
		}
		//printf("%d caracteres escritos en el archivo %s\n", fprintf(salida[k-1], "marcos %dx%d\n", 2*k+1, 2*k+1), archivo_salida);
	}
	
	if (cmax == 0) cmax = CMAX;
	
	int c;
	int marco[8*n+1];
	int *reserva[n];
	
	for (k = 1; k <= n; k++) reserva[k-1] = malloc(sizeof(int)*(8*(k)+1));
	
	for (k = 1; k <= n; k++) {
		do {
			if (leer_linea_csv(entrada_marcos[k], marco, 8*k+1)) {
				if (k == 1) return 0;
				else  n = k-1;
			}
		} while (marco[0] < cmin);
		copiar_array(marco, reserva[k-1], 8*k+1);
	}
	
	c = marco[0];
		
	do {
		for (k = 1; k <= n; ++k) {
			if (reserva[k-1][0] == c) copiar_array(reserva[k-1]+1, get_from_mibuff(&matrices_generadas[k-1], matrices_generadas[k-1].elementos++), 8*k);
			else if (reserva[k-1][0] == -1) {
				n = --k;
				break;
			} else {
				--k;
				break;
			}
			
			if (leer_linea_csv(entrada_marcos[k-1], marco, 8*k+1)) {
				reserva[k-1][0] = -1;
				break;
			}
			
			if (marco[0] == c) copiar_array(marco+1, get_from_mibuff(&matrices_generadas[k-1], matrices_generadas[k-1].elementos++), 8*k);
			else if (marco[0] < c) continue;
			else {
				copiar_array(marco, reserva[k-1], 8*k+1);
				if (matrices_generadas[k-1].elementos == 0) {
					--k;
					break;
				}
			}
		}
		
		ensamblar_y_escribir(salida_matrices, c, k);
		for (--k; k >= 0; --k) fflush(salida_matrices[k]);
		
		num_generadas[0] = c;
		for (k = 0; k < n; k++) fprintf(archivo_num_generadas, "%ld,", num_generadas[k]);
		fprintf(archivo_num_generadas, "%ld\n", num_generadas[n]);
		if (fflush(archivo_num_generadas) == -1) printf("Error de escritura en archivo_num_generadas\n");
				
		for (k = 1; k <= n; k++) matrices_generadas[k-1].elementos = 0;
		
		if ((c = reserva[0][0]) > 0) copiar_array(reserva[0], get_from_mibuff(&matrices_generadas[0], matrices_generadas[0].elementos++), 8);
		else return 0;
	} while (c < cmax);
	
	return 0;
}
