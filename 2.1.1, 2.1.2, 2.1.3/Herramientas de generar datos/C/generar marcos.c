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
	char *archivo_entrada;
	archivo_entrada = NULL;
	ppio_archivo_salida = NULL;
	
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
			ppio_archivo_salida = argv[k+1];
			printf("archivo de salida %s\n", ppio_archivo_salida);
			k++;
			continue;
		}
		printf("Argumento no identificado %s\n", argv[k]);
	}
	if (ppio_archivo_salida == NULL) {
		ppio_archivo_salida = "marcos";
	}
	
	//inicializar_var_globales(n);
	//printf("Variables globales inicializadas\n");
	
	struct buffthread *buff_hilo = malloc(sizeof(struct buffthread)*n);
	for (k = 1; k <= n; ++k) inicializar_buff_hilo(buff_hilo+k-1, k);
	
	FILE *archivo_filas_posibles = fopen("filas_posibles.csv", "w");
	printf("filas_posibles.csv -> %p\n", archivo_filas_posibles);
	
	fprintf(archivo_filas_posibles, "primo central");
	for (k = 1; k <=n; ++k) fprintf(archivo_filas_posibles, ", filas nivel %d", k);
	fputc('\n', archivo_filas_posibles);
	
	filas_posibles = malloc(sizeof(long int)*(n+2));
	
	FILE *archivo_marcos_posibles;
	archivo_marcos_posibles = fopen("marcos_posibles.csv", "w");
	
	fprintf(archivo_marcos_posibles, "primo central");
	for (k = 1; k <=n; ++k) fprintf(archivo_marcos_posibles, ", marcos nivel %d", k);
	fputc('\n', archivo_marcos_posibles);
	
	long int* marcos_posibles = malloc(sizeof(long int)*(n+1));
	
	FILE *archivo_duplicidades;
	archivo_duplicidades = fopen("duplicidades_al_generar.csv", "w");
	
	fprintf(archivo_duplicidades, "primo central");
	for (k = 1; k <=n; ++k) fprintf(archivo_duplicidades, ", duplicidades nivel %d", k);
	fputc('\n', archivo_duplicidades);
	
	duplicidades = malloc(sizeof(long int)*(n+1));
	
	//FILE *salida[n];
	char archivo_salida[strlen(ppio_archivo_salida)+12];
	
	for (k = 1; k <=n; k++){
		sprintf(archivo_salida, "%s_%dx%d.csv", ppio_archivo_salida, 2*k+1, 2*k+1);
		buff_hilo[k-1].salida = fopen(archivo_salida, "w");
		if (buff_hilo[k-1].salida == NULL) {
			printf("Error al crear el archivo %s\n", archivo_salida);
			exit(1);
		}
		//printf("%d caracteres escritos en el archivo %s\n", fprintf(salida[k-1], "marcos %dx%d\n", 2*k+1, 2*k+1), archivo_salida);
	}
	
	
	// criba de eratostenes
	if (cmax == 0) cmax = CMAX;
	
	printf("\nEmpezamos Eratostenes\n");
	esprimo = (char*) malloc(sizeof(char)*cmax*2);
	gen_esprimo(esprimo, cmax);
	//mostrar_esprimo(2*cmax);
	
	int numprimos = cuantos_primos(cmax*2);
	printf("Se han encontrado %d primos entre 0 y %d\n", numprimos, cmax*2);
	
	
	// Empezamos a calcular matrices
	printf("Empezamos a calcular marcos\n");
	
	int c = CMIN;
	
	struct paresposibles parposib;
	parposib.posibles = malloc(numprimos/2*sizeof(int));
	parposib.usados = NULL;
	parposib.cuantos_usados = 0;
	
	for (k = 1; k <= n; ++k) buff_hilo[k-1].parposib = &parposib;
	
	printf("Inicializamos signos\n");
	for (k = 1; k <= n; k++) gen_signos_pa_filas(&buff_hilo[k-1].buffsignos);
	
	for (i = 0; i < numprimos; ++i) {
		for (; esprimo[c]== 0 && c < cmax; ++c) {}
		if (c >= cmax) {
			printf("Hemos llegado a %d\n", cmax);
			return 0;
		}
		printf("\nEmpezamos con el primo %d\n", c);
		
		parposib.c = c;
		gen_primos_posibles(&parposib);
		parposib.cuantos = parposib.cuantos_total;
		
		printf("Se han encontrado %d pares de primos\n", parposib.cuantos_total);
		
		filas_posibles[0] = c;
		filas_posibles[1] = parposib.cuantos_total;
		marcos_posibles[0] = c;
		duplicidades[0] = c;
		for (k = 1; k<= n; ++k) filas_posibles[k+1] = 0;
		for (k = 1; k<= n; ++k) marcos_posibles[k] = 0;
		for (k = 1; k<= n; ++k) duplicidades[k] = 0;
		
		// modo secuencial
		for (k = 1; k <= n; k++) {
			if (parposib.cuantos_total < 4*k) {
				printf("No hay suficientes primos\n");
				break;
			}
			
			buff_hilo[k-1].c = c;
			if (k > 1) filas_posibles[k+1] = gen_filas_hilo(buff_hilo+k-1, (2*k+1)*c);
			else filas_posibles[k+1] = gen_filas_3_hilo(buff_hilo+k-1, 3*c);
			
			printf("Se han generado %ld filas\n", buff_hilo[k-1].buff_filas.elementos);
			
			if (k == 1) marcos_posibles[1] = gen_marcos_anid_3(buff_hilo, c);
			else marcos_posibles[k] = gen_marcos_anid_n(buff_hilo+k-1, c, k);
			if (marcos_posibles[k] == 0) break;
		}
		
		for (k = 0; k < n; ++k) fprintf(archivo_filas_posibles, "%ld,", filas_posibles[k]);
		fprintf(archivo_filas_posibles, "%ld\n", filas_posibles[n]);
		
		for (k = 0; k < n; ++k) fprintf(archivo_marcos_posibles, "%ld,", marcos_posibles[k]);
		fprintf(archivo_marcos_posibles, "%ld\n", marcos_posibles[n]);
		
		for (k = 0; k < n; ++k) fprintf(archivo_duplicidades, "%ld,", duplicidades[k]);
		fprintf(archivo_duplicidades, "%ld\n", duplicidades[n]);
		
		for (k = 0; k < n; ++k) if (fflush(buff_hilo[k].salida) == -1) printf("Error de escritura en salida[%d]\n", k);
		if (fflush(archivo_filas_posibles) == -1) printf("Error de escritura en archivo_filas_posibles\n");
		if (fflush(archivo_marcos_posibles) == -1) printf("Error de escritura en archivo_marcos_posibles\n");
		if (fflush(archivo_duplicidades) == -1) printf("Error de escritura en archivo_duplicidades\n");
		
		++c;
	}
	return 0;
}
