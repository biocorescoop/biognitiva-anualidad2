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
//char log = 0;
FILE* logfile;


void imprimir_ayuda(char *argv[]) {
	printf("%s -n nivel -cmin cmin -cmax cmax -i input.csv -o output.csv\n", argv[0]);
}

int main(int argc, char *argv[]) {
	// recorrer argumentos
	int k, i;
	int n = 3;
	int cmax = 0;
	int cmin = CMIN;
	
	
	char *archivo_salida;
	char *archivo_entrada;
	//char *archivo_salida_datos;
	archivo_salida = NULL;
	archivo_entrada = NULL;
	
	for (k = 1; k < argc; k++) {
		if (!strcmp(argv[k], "-h")) {
			imprimir_ayuda(argv);
			return 0;
		}
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
		if (!strcmp(argv[k], "-logfile")) {
			logfile = fopen(argv[k+1], "w");
			//log = 1;
			printf("archivo de log %s\n", archivo_entrada);
			k++;
			continue;
		}
		printf("Argumento no identificado %s\n", argv[k]);
	}
	if (archivo_salida == NULL) {
		archivo_salida = alloca(25);
		sprintf(archivo_salida, "matrices_%dx%d.csv", 2*n+1, 2*n+1);
	}
	
	inicializar_var_globales(n);
	printf("Variables globales inicializadas\n");
	
	FILE *salida;
	FILE *entrada;
	salida = fopen(archivo_salida, "w");
	
	if (n > 1) {
		if (archivo_entrada == NULL) {
			archivo_entrada = alloca(25);
			sprintf(archivo_entrada, "matrices_%dx%d.csv", 2*n-1, 2*n-1);
		}
		entrada = fopen(archivo_entrada, "r");
	}
	
	// criba de eratostenes
	if (cmax == 0) {
		cmax = CMAX;
	}
	
	printf("\nEmpezamos Eratostenes\n");
	esprimo = (char*) malloc(sizeof(char)*cmax*2);
	gen_esprimo(esprimo, cmax);
	//mostrar_esprimo(2*cmax);
	
	int numprimos = cuantos_primos(cmax*2);
	printf("Se han encontrado %d primos entre 0 y %d\n", numprimos, cmax*2);
	
	int matriz_prev[(2*n-1)*(2*n-1)];
	int *matriz_anid[n+1];
	matriz_anid[0] = &matriz_prev[0];
	for (k = 1; k < n; k++) {
		matriz_anid[k] = matriz_prev + (2*k+1)*(2*k+1);
		printf("matriz_anid[%d] = %p\n", k, matriz_anid[k]);
	}
	
	// Empezamos a calcular matrices
	printf("Empezamos a calcular matrices\n");
	
	int c = CMIN;
	int c_anterior = 0;
	
	int cuantas_matrices = 0;
	int total_matrices = 0;
	
	//matrices_generadas[n-1].bloques_reservados = 0;
	//matrices_generadas[n-1].elementos = 0;
	//matrices_generadas[n-1].elemxbloque = MAT_X_BLOQUE;
	//matrices_generadas[n-1].tam = 8*n;
	
	struct paresposibles parposib;
	parposib.posibles = malloc(numprimos/2*sizeof(int));
	parposib.usados = NULL;
	parposib.cuantos_usados = 0;
	
	printf("Inicializamos signos\n");
	gen_signos_pa_filas(n);
	
	if (n == 1) {
		printf("Calculamos matrices 3x3\n");
		for (i = 0; i < numprimos; i++) {
			for (; esprimo[c]== 0 && c < cmax; c++) {}
			if (c >= cmax) {
				printf("Hemos llegado a %d\n", cmax);
				return 0;
			}
			printf("Empezamos con el primo %d\n", c);
			*matriz_anid[0] = c;
			
			parposib.c = c;
			gen_primos_posibles(&parposib);
			parposib.cuantos = parposib.cuantos_total;
			
			printf("Se han encontrado %d pares de primos\n", parposib.cuantos_total);
			
			cuantas_matrices = gen_nuevas_anid(&parposib, c, n);
			total_matrices = total_matrices + cuantas_matrices;
			
			printf("Se han generado %d matrices\n", cuantas_matrices);
			
			for (k = 0; k < cuantas_matrices; k++) {
				matriz_anid[1] = get_from_mibuff(&matrices_generadas[n-1], k);
				escribir_anidada(salida, matriz_anid, 1);
				//escribir_anidada(salida, matriz_anid, ind_matrices_generadas[k], n);
				//escribir_datos(salida_datos, matriz_anid, cuantas_matrices, n);
			}
			c++;
		}
		return 0;
	}
	
	int escritas;
	
	parposib.cuantos_usados = ((2*n-1)*(2*n-1)-1)/2;
	buff_filas[n-1].tam = 2*n + 1;
	
	for (i = 0;;i++) {
		//if (1 || (i % 100 == 0)) printf("%d matrices procesadas\n", i);
		
		// Leemos una matriz anidada
		if (leer_anidada(entrada, matriz_anid, n)) return 1;
				
		c = *matriz_anid[0];
		
		//printf("matriz[0][0] = %d\n", matriz_anid[0][0]);
		//for (k = 1; k < n; k++) for (i = 0; i < 8*k; i++) printf("matriz[%d][%d] = %d\n", k, i, matriz_anid[k][i]);
		
		if (c < cmin) continue;
		
		if (c > cmax) {
			printf("c = %d y hemos llegado a %d\n", c, cmax);
			return 0;
		}
		
		putchar('\n');
		mostrar_matriz(matriz_anid[n-1], matriz_anid, n-1);
		
		if (c != c_anterior) {
			//printf("generamos primos posibles\n");
			c_anterior = c;
			parposib.c = c;
			gen_primos_posibles(&parposib);
			//parposib.cuantos = parposib.cuantos_total;
			printf("Se han generado %d pares\n", parposib.cuantos_total);
		}
		
		elim_primos_usados(matriz_anid, n, &parposib);
		//printf("Generamos las matrices\n");
		cuantas_matrices = gen_nuevas_anid(&parposib, c, n);
		
		printf("\n%d matrices generadas con el primo %d\n", cuantas_matrices, c);
		
		if (cuantas_matrices < 1) {
			continue;
		}
		
		//mostrar_matriz(get_from_mibuff(&matrices_generadas, 0), matriz_anid, n);
		escritas = escribir_generadas(salida, matriz_anid, n);
		if (escritas != cuantas_matrices) printf("¡Faltan matrices por escribir\n");
		
		total_matrices = total_matrices + cuantas_matrices;
	}
	return 0;
}
