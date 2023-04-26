#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "matanid.h"

int main(int argc, char *argv[]) {
	int k, i, n = -1, c, cmax = 5000, cmin = 0;
	char *archivo_salida;
	char *archivo_entrada;
	char *archivo_perm;
	//char *archivo_salida_datos;
	archivo_salida = NULL;
	archivo_entrada = NULL;
	archivo_perm = NULL;
	char verbose = 0;
	
	for (k = 1; k < argc; k++) {
		if (!strcmp(argv[k], "-n")) {
			sscanf(argv[k+1], "%d", &n);
			k = k + 2;
			printf("n = %d\n", n);
			continue;
		}
		if (!strcmp(argv[k], "-cmax")) {
			sscanf(argv[k+1], "%d", &cmax);
			printf("cmax = %d\n", cmax);
			k = k + 2;
			continue;
		}
		if (!strcmp(argv[k], "-cmin")) {
			sscanf(argv[k+1], "%d", &cmin);
			printf("cmin = %d\n", cmin);
			k = k + 2;
			continue;
		}
		if (!strcmp(argv[k], "-i")) {
			archivo_entrada = argv[k+1];
			printf("archivo de entrada %s\n", archivo_entrada);
			k = k + 2;
			continue;
		}
		if (!strcmp(argv[k], "-o")) {
			archivo_salida = argv[k+1];
			printf("archivo de salida %s\n", archivo_salida);
			k = k + 2;
			continue;
		}
		if (!strcmp(argv[k], "-perm")) {
			archivo_perm = argv[k+1];
			//printf("cmax = %d\n", cmax);
			k = k + 2;
			continue;
		}
		if (!strcmp(argv[k], "-v")) {
			verbose = 1;
			k++;
			continue;
		}
		printf("Argumento no identificado %s\n", argv[k]);
	}
	
	if (n < 0) {
		n = 1;
	}
	
	/*if (archivo_salida == NULL) {
		archivo_salida = alloca(25);
		sprintf(archivo_salida, "mismos_elem %dx%d.csv", 2*n+1, 2*n+1);
	}*/
	
	FILE *salida;
	FILE *entrada;
	//
	
	if (archivo_entrada == NULL) {
		archivo_entrada = alloca(30);
		sprintf(archivo_entrada, "matrices_%dx%d.csv", 2*n+1, 2*n+1);
	}
	entrada = fopen(archivo_entrada, "r");
	if (entrada == NULL) {
		printf("Archivo de entrada no puede ser abierto\n");
		exit(1);
	}
	else {
		printf("Archivo %s abierto correctamente\n", archivo_entrada);
		printf("%p\n", entrada);
	}
	
	if (archivo_salida == NULL) sprintf(archivo_salida = alloca(25), "matrices_similares_%dx%d.csv", 2*n+1, 2*n+1);
	salida = fopen(archivo_salida, "w");
		
	//printf("\nEmpezamos Eratostenes\n");
	//esprimo = (char*) malloc(sizeof(char)*cmax*2);
	//gen_esprimo(esprimo, cmax);
	
	int numpares = 2*n*(n+1), tam_red = 1+2*n*(n+1), tam_anid = (2*n+1)*(2*n+1);
	long int cont;
	
	int *reducida;
	reducida = calloc(tam_red, sizeof(int));
	
	int *array_anid, *array_anid2;
	int sentido, encontradas, j;
	
	struct mibuffer buffanidadas;
	buffanidadas.tam = tam_anid*2;
	buffanidadas.elemxbloque = MAT_X_BLOQUE;
	buffanidadas.elementos = 0;
	buffanidadas.bloques_reservados = 0;
	
	//perm = malloc(numpares*sizeof(int));
	
	c = - 1;
	
	do {
		cont = 0;
		if (reducida[0] != 0) {
			array_anid = get_from_mibuff(&buffanidadas, cont);
			desreducir_array(array_anid, reducida, n);
			cont++;
		}
		do {
			// reducida = get_from_mibuff(&buffanidadas, cont);
			if(leer_linea_csv(entrada, reducida, tam_anid)) return 0;
			if (c == -1) c = reducida[0];
			
			array_anid = get_from_mibuff(&buffanidadas, cont);
			desreducir_array(array_anid, reducida, n);
			copiar_array(array_anid, array_anid + tam_anid, tam_anid);
			ordenar_burbuja(array_anid, tam_anid);
			
			cont++;
		} while (reducida[0] == c);
		
		for (i = 0; i < cont; i++) {
			array_anid = get_from_mibuff(&buffanidadas, i);
			encontradas = 1;
			for (j = i+1; j < cont; j++) {
				array_anid2 = get_from_mibuff(&buffanidadas, j);
				
				if (array_anid2[0] == 0) continue;
				if (!comp_arrays(array_anid, array_anid2, tam_anid)) continue;
				encontradas++;
				
				if (encontradas == 2) escribir_array(salida, array_anid + tam_anid, tam_anid);
				escribir_array(salida, array_anid2 + tam_anid, tam_anid);
				array_anid2[0] = 0;
			}
			if (encontradas > 1) fprintf(salida, "\n");
		}
		c = reducida[0];
		
	} while (c < cmax);
	
	
	return 0;
}

