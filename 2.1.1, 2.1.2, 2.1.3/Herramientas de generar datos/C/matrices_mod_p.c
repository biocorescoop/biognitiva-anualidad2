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
	printf("%s -n nivel -cmin cmin -cmax cmax  -modc -mod p -i input.csv -o output.csv\n", argv[0]);
}

int main(int argc, char *argv[]) {
	// recorrer argumentos
	int k, i;
	int n = 3;
	int cmax = 0;
	int cmin = CMIN;
	int modc = 0;
	int p = 0;
	
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
		if (!strcmp(argv[k], "-modc")) {
			modc = 1;
			continue;
		}
		if (!strcmp(argv[k], "-mod")) {
			sscanf(argv[k+1], "%d", &p);
			printf("p = %d\n", p);
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
	
	char *archivo_entrada_marcos = malloc(sizeof(char)*(strlen(ppio_archivo_entrada)+22));
	char *archivo_salida_mod_c = malloc(sizeof(char)*(strlen(ppio_archivo_salida)+22));
	char *archivo_salida_mod_p = malloc(sizeof(char)*(strlen(ppio_archivo_salida)+22));
	
	FILE *entrada_marcos[n];
	FILE *salida_mod_c[n];
	FILE *salida_mod_p[n];
	
	for (k = 1; k <=n; ++k){
		if (modc) {
			sprintf(archivo_salida_mod_c, "%s_%dx%d_mod_c.csv", ppio_archivo_salida, 2*k+1, 2*k+1);
			salida_mod_c[k-1] = fopen(archivo_salida_mod_c, "w");
		}
		if (p) {
			sprintf(archivo_salida_mod_p, "%s_%dx%d_mod_%d.csv", ppio_archivo_salida, 2*k+1, 2*k+1, p);
			salida_mod_p[k-1] = fopen(archivo_salida_mod_p, "w");
		}
		
		sprintf(archivo_entrada_marcos, "%s_%dx%d.csv", ppio_archivo_entrada, 2*k+1, 2*k+1);
		entrada_marcos[k-1] = fopen(archivo_entrada_marcos, "r");
		
		if (modc) if (salida_mod_c[k-1] == NULL) {
			printf("Error al crear el archivo %s\n", archivo_salida_mod_c);
			exit(1);
		}
		if (p) if (salida_mod_p[k-1] == NULL) {
			printf("Error al crear el archivo %s\n", archivo_salida_mod_p);
			exit(1);
		}
		//printf("%d caracteres escritos en el archivo %s\n", fprintf(salida[k-1], "marcos %dx%d\n", 2*k+1, 2*k+1), archivo_salida);
	}
	
	struct buffthread *buff_hilo_mod_c = malloc(n*sizeof(struct buffthread));
	struct buffthread *buff_hilo_mod_p = malloc(n*sizeof(struct buffthread));
	
	long int *elems_por_clase;
	long int *elem_por_clase_p[n];
	
	FILE *matrices_generadas_mod_p;
	char archivo_matrices_generadas_mod_p[30];
	
	printf("Archivos y buffers declarados\n");
	
	for (k = 0; k < n; k++) {
		if (modc) {
			printf("inicializando buff_hilo_mod_c[%d]...\n", k);
			inicializar_buff_hilo(buff_hilo_mod_c + k, k+1);
			buff_hilo_mod_c[k].matrices_generadas.tam++;
		}
		if (p) {
			printf("inicializando buff_hilo_mod_p[%d]...\n", k);
			inicializar_buff_hilo(&buff_hilo_mod_p[k], k + 1);
			buff_hilo_mod_p[k].matrices_generadas.tam = 8*(k+1)+1;
			
			sprintf(archivo_matrices_generadas_mod_p, "matrices_generadas_%dx%d.csv", 2*(k+1)+1, 2*(k+1)+1);
			buff_hilo_mod_p[k].salida = fopen(archivo_matrices_generadas_mod_p, "w");
			
			gen_marcos_mod_p(&buff_hilo_mod_p[k], p, k + 1);
			printf("%ld filas generadas mod %d\n", buff_hilo_mod_p[k].buff_filas.elementos, p);
			printf("%ld matrices generadas mod %d\n", buff_hilo_mod_p[k].matrices_generadas.elementos, p);
			elem_por_clase_p[k] = calloc(buff_hilo_mod_p[k].matrices_generadas.elementos, sizeof(long int));
		}
	}
	
	printf("Llegamos a elem_por_clase_p\n");
	
	printf("Inicialización terminada\n");
	
	if (cmax == 0) cmax = CMAX;
	
	int c;
	int marco[8*n+1];
	int *reserva[n];
	
	for (k = 1; k <= n; k++) reserva[k-1] = malloc(sizeof(int)*(8*k+1));
	
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
		
		if (p) for (k = 0; k < n; k++) clasificar_mod_p(matrices_generadas + k, buff_hilo_mod_p + k, elems_por_clase, c);
		
		if (modc) {
			for (k = 0; k < n; k++) {
				gen_marcos_mod_c(buff_hilo_mod_c + k, c, c, k+1);
				elems_por_clase = calloc(buff_hilo_mod_c[k].matrices_generadas.elementos, sizeof(long int));
				clasificar_mod_p(matrices_generadas + k, buff_hilo_mod_c + k, elems_por_clase, c);
				for (i = 0; i < buff_hilo_mod_c[k].matrices_generadas.elementos; i++) {
					fprintf(salida_mod_c[k], "%d,", c);
					fprintf(salida_mod_c[k], "%ld,", buff_hilo_mod_c[k].matrices_generadas.elementos);
					escribir_array(salida_mod_c[k], get_from_mibuff(&buff_hilo_mod_c[k].matrices_generadas, i), 8*(k+1));
				}
				free(elems_por_clase);
			}
		}
		
		for (--k; k >= 0; --k) fflush(salida_mod_c[k]);
				
		for (k = 1; k <= n; k++) matrices_generadas[k-1].elementos = 0;
		
		if ((c = reserva[0][0]) > 0) copiar_array(reserva[0], get_from_mibuff(&matrices_generadas[0], matrices_generadas[0].elementos++), 8);
		else return 0;
	} while (c < cmax);
	
	if (p) {
		for (k = 0; k < n; k++) for (i = 0; i < buff_hilo_mod_p[k].matrices_generadas.elementos; i++) {
			fprintf(salida_mod_p[k], "%ld,", elem_por_clase_p[k][i]);
			escribir_array(salida_mod_p[k], get_from_mibuff(&buff_hilo_mod_p[k].matrices_generadas, i), 8*(k+1));
		}
		for (--k; k >= 0; --k) fflush(salida_mod_c[k]);
	}
	
	return 0;
}
