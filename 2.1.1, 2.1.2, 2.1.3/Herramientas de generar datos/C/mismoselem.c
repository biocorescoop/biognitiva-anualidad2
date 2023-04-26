#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <alloca.h>

#include "matanid.h"

int main(int argc, char *argv[]) {
	int k, i, n = -1, c, cmax = 5000, cmin = 0;
	char *archivo_salida;
	char *archivo_entrada;
	//char *archivo_salida_datos;
	archivo_salida = NULL;
	archivo_entrada = NULL;
	
	for (k = 1; k < argc; k++) {
		if (!strcmp(argv[k], "-n")) {
			sscanf(argv[k+1], "%d", &n);
			k++;
			printf("n = %d\n", n);
			continue;
		}
		if (!strcmp(argv[k], "-cmax")) {
			sscanf(argv[k+1], "%d", &cmax);
			printf("cmax = %d\n", cmax);
			k++;
			continue;
		}
		if (!strcmp(argv[k], "-cmin")) {
			sscanf(argv[k+1], "%d", &cmin);
			printf("cmin = %d\n", cmin);
			k++;
			continue;
		}
		if (!strcmp(argv[k], "-i")) {
			archivo_entrada = argv[k+1];
			printf("archivo de entrada %s\n", archivo_entrada);
			k++;
			continue;
		}
		if (!strcmp(argv[k], "-o")) {
			archivo_salida = argv[k+1];
			printf("archivo de salida %s\n", archivo_salida);
			k++;
			continue;
		}
		printf("Argumento no identificado %s\n", argv[k]);
	}
	
	if (n < 0) {
		n = 2;
	}
	
	if (archivo_salida == NULL) {
		archivo_salida = alloca(25);
		sprintf(archivo_salida, "mismos_elem %dx%d.csv", 2*n+1, 2*n+1);
	}
	
	FILE *salida;
	FILE *entrada;
	salida = fopen(archivo_salida, "w");
	
	if (n > 1) {
		if (archivo_entrada == NULL) {
			archivo_entrada = alloca(25);
			sprintf(archivo_entrada, "matrices_%dx%d.csv", 2*n+1, 2*n+1);
		}
		entrada = fopen(archivo_entrada, "r");
	}
	
	if (archivo_salida == NULL) {
		archivo_entrada = alloca(25);
		sprintf(archivo_entrada, "matrices_%dx%d_similares.csv", 2*n+1, 2*n+1);
	}
	
	int tam = (2*n+1)*(2*n+1), *matriz, matriz_ordenada[tam], *similar_ordenada;
	
	printf("Empezamos\n");
	
	struct mibuffer mismatrices;
	mismatrices.tam = tam;
	mismatrices.bloques_reservados = 0;
	mismatrices.elemxbloque = MAT_X_BLOQUE;
	
	//mibufferptr *matrices_similares;
	struct mibufferptr ind_similares;
	ind_similares.elementos = 0;
	ind_similares.bloques_reservados = 0;
	ind_similares.elemxbloque = MAT_X_BLOQUE;
	
	struct mibufferptr *similares, **similares_ptr;
	//similares.actual = 0;
	//similares.bloques_reservados = 0;
	//similares.elemxbloque = MAT_X_BLOQUE;
	
	int **mat_actual, encontrada;
		
	ind_similares.elementos = 0;
	
	for (mismatrices.elementos = 0; ; mismatrices.elementos++) {
		printf("Leyendo la matriz %d\n", mismatrices.elementos);
		matriz = get_from_mibuff(mismatrices, mismatrices.elementos);
		printf("La matriz %d va en la posición %p\n", mismatrices.elementos, matriz);
		if(leer_linea_csv(entrada, matriz, tam)) break;
		printf("Matriz %d leída\n", mismatrices.elementos);
		c = matriz[0];
		if (c < cmin) continue;
		if (c > cmax) return 0;
		
		copiar_array(matriz, matriz_ordenada, 0, tam);
		ordenar_burbuja(matriz_ordenada, tam);
		encontrada = 0;
		for (i = 0; i < ind_similares.elementos; i++) {
			similar_ordenada = (int*) get_from_mibuffptr(ind_similares, i);
			if (comp_arrays(matriz_ordenada, similar_ordenada, tam)) {
				similares = (struct mibufferptr*) get_from_mibuffptr(ind_similares, i);
				mat_actual = (int**) get_prt_from_mibuffptr(*similares, similares->elementos);
				*mat_actual = matriz;
				similares->elementos++;
				encontrada = 1;
				break;
			}
		}
		if (encontrada) continue;
		
		// Hay un ind nuevo -> incializar similares
		printf("inicializando similares %d\n", i);
		ind_similares.elementos = i;
		similar_ordenada = (int*) get_from_mibuffptr(ind_similares, i);
		printf("similar ordenada obtenida en %p\n", similar_ordenada);
		copiar_array(matriz_ordenada, similar_ordenada, 0, tam);
		mostrar_array(similar_ordenada, tam);
		similares_ptr = (struct mibufferptr**) get_prt_from_mibuffptr(ind_similares, i);
		*similares_ptr = (struct mibufferptr*) malloc(sizeof(struct mibufferptr));
		similares = *similares_ptr;
		similares->elementos = 0;
		similares->elemxbloque = MAT_X_BLOQUE;
		similares->bloques_reservados = 0;
		
		mat_actual = (int**) get_prt_from_mibuffptr(*similares, similares->elementos);
		*mat_actual = matriz;
		similares->elementos++;
	}
	
	for (i = 0; i < ind_similares.elementos; i++) {
		similares = get_from_mibuffptr(ind_similares, i);
		mat_actual = (int**) get_prt_from_mibuffptr(ind_similares, i);
		escribir_array(salida, *mat_actual, tam);
		for (k = 0; k < similares->elementos; k++) {
			mat_actual = (int**) get_from_mibuffptr(*similares, k);
			escribir_array(salida, *mat_actual, tam);
		}
		fprintf(salida, "\n");
	}
	
	
}
