#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <alloca.h>

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
	FILE *entrada_perm;
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
	
	if (archivo_salida == NULL) sprintf(archivo_salida = alloca(25), "repetición_permutaciones_%dx%d.csv", 2*n+1, 2*n+1);
	salida = fopen(archivo_salida, "w");
	
	if (archivo_perm != NULL) entrada_perm = fopen(archivo_perm, "r");
	
	printf("\nEmpezamos Eratostenes\n");
	esprimo = (char*) malloc(sizeof(char)*cmax*2);
	gen_esprimo(esprimo, cmax);
	
	//int matriz_prev[(2*n+1)*(2*n+1)];
	int *matriz_anid[n];
	matriz_anid[0] = malloc(sizeof(int));
	for (k = 1; k <= n; k++) matriz_anid[k] = malloc(sizeof(int)*8*k);
	
	//int matriz_post[(2*n+1)*(2*n+1)];
	int *nueva_anid[n];
	nueva_anid[0] = malloc(sizeof(int));
	for (k = 1; k <= n; k++) nueva_anid[k] = malloc(sizeof(int)*8*k);
	
	int *resta_matrices[n];
	resta_matrices[0] = malloc(sizeof(int));
	for (k = 1; k <= n; k++) resta_matrices[k] = malloc(sizeof(int)*8*k);
	
	int *perm, numpares = 2*n*(n+1), tam = 1+2*n*(n+1), es_anidada;
	long int num_perm;
	long int cont;
	
	struct permciclos *permciclada;
	permciclada = malloc(sizeof(struct permciclos));
	permciclada->ciclos = malloc(sizeof(int*)*numpares);
	permciclada->tam = malloc(sizeof(int)*numpares);
	permciclada->numciclos = 0;
	
	if (n == 1) { // para n = 2 ya tengo 2^8*8! = 10.321.920 permutaciones
		int reducida[tam], newreducida[tam];
		struct mibuffer *permutaciones;
		if (archivo_perm == NULL) permutaciones = gen_permutaciones(n);
		else permutaciones = leer_permutaciones(entrada_perm, n);
		printf("Se han generado/leído %ld permutaciones\n", permutaciones->elementos);
		
		int rep_permutaciones[permutaciones->elementos];
		for (i = 0; i < permutaciones->elementos; i++) rep_permutaciones[i] = 0;
		
		for (i = 0; i < numpares; i++) permciclada->ciclos[i] = malloc(sizeof(int)*(numpares-i));
		
		for (num_perm = 0; num_perm < permutaciones->elementos; num_perm++) {
			printf("permutación %ld: ", num_perm);
			perm = get_from_mibuff(permutaciones, num_perm);
			mostrar_array(perm, numpares);
			perm_to_ciclos(perm, permciclada, numpares);
			mostrar_ciclos(permciclada);
			putchar('\n');
		}
		
		printf("Empezamos a leer matrices\n");
		for (cont = 0; cont < 100 || 1; cont++) {
			//leer_anidada(entrada, matriz_anid, n+1);
			if (leer_linea_csv(entrada, reducida, tam)) break;
			//printf("Reducida: ");
			//mostrar_array(reducida, tam);
			
			desreducir_matriz(matriz_anid, reducida, n);
			//mostrar_matriz(matriz_anid[n], matriz_anid, n);
			//printf("Seguimos\n");
			
			for (num_perm = 0; num_perm < permutaciones->elementos; num_perm++) {
				perm = get_from_mibuff(permutaciones, num_perm);
				//num_to_signo(numsigno, signos, numpares);
				
				if (perm[0] != 1 || perm[2] != 3) continue; // si las esquinas cambian de posición
				
				permutar_reducidas(perm, reducida, newreducida, n);
				//printf("Reducida nueva: ");
				//mostrar_array(newreducida, tam);
				desreducir_matriz(nueva_anid, newreducida, n);
				
				es_anidada = es_matriz_anidada(nueva_anid, n);
				if (verbose  & !es_anidada) printf("No es una matriz válida\n");
				if (es_anidada || verbose) { // || archivo_perm != NULL
					//numsigno = num_signo(signos, numpares);
					printf("Original:\n");
					mostrar_matriz(matriz_anid[n], matriz_anid, n);
					if (es_anidada) rep_permutaciones[num_perm]++;
					printf("permutación: ");
					mostrar_array(perm, numpares);
					perm_to_ciclos(perm, permciclada, numpares);
					mostrar_ciclos(permciclada);
					printf("Reducida nueva: ");
					mostrar_array(newreducida, tam);
					printf("Matriz:\n");
					mostrar_matriz(nueva_anid[n],nueva_anid, n);
					restar_matrices(matriz_anid, nueva_anid, resta_matrices, n);
					printf("Resta:\n");
					mostrar_matriz(resta_matrices[n],resta_matrices, n);
					if (archivo_perm != NULL) {
						if (!es_anidada) printf("No es matriz anidada\n\n");
						else printf("Es matriz anidada\n\n");
					}
				}
			}
		}
		
		printf("Frecuencias:\n");
		mostrar_array(rep_permutaciones, permutaciones->elementos);
		
		//frec = ord_frecuencias(rep_permutaciones, permutaciones->elementos, numpares);
		
		fprintf(salida, "NumPerm;Ciclos;Frecuencia\n");
		for (num_perm = 0; num_perm < permutaciones->elementos; num_perm++) {
			if (rep_permutaciones[num_perm]) {
				perm = get_from_mibuff(permutaciones, num_perm);
				perm_to_ciclos(perm, permciclada, numpares);
				fprintf(salida, "%ld;%d", num_perm, perm[0]);
				for (i = 1; i < numpares; i++) fprintf(salida, " %d", perm[i]);
				fprintf(salida, ";");
				escribir_ciclos(salida, permciclada, numpares);
				fprintf(salida, ";%d\n", rep_permutaciones[num_perm]);
			}
		}
		return 0;
	} else {
		FILE *salida_univ;
		salida_univ = fopen("permutaciones_universales.csv", "w");
		
		//inicializamos el buffer de las permutaciones universales
		struct mibuffer *permunivs;
		int *perm_univ;
		
		int *reducida, newreducida[tam];
		struct mibuffer buffreducidas;
		buffreducidas.tam = tam;
		buffreducidas.elemxbloque = MAT_X_BLOQUE;
		buffreducidas.elementos = 0;
		buffreducidas.bloques_reservados = 0;
		
		// En vez de generar todas las permutaciones, vamos permutación por permutación permutando todas las matrices.
		perm = malloc(numpares*sizeof(int));
		
		// inicializamos la permutación identidad:
		for (int i = 0; i < numpares; i++) perm[i] = i+1;
		
		int tope = NUM_BLOQUES*MAT_X_BLOQUE;
		tope = 1000;
		for (cont = 0; cont < tope; cont++) {
			reducida = get_from_mibuff(&buffreducidas, cont);
			if(leer_linea_csv(entrada, reducida, tam)) break;
			mostrar_array(reducida, tam);
			if (es_matriz_reducida(reducida, n)) putchar('.');
			else {
				desreducir_matriz(matriz_anid, reducida, n);
				mostrar_matriz(matriz_anid[n], matriz_anid, n);
			}
		}
		putchar('\n');
		buffreducidas.elementos = cont;
		printf("Matrices leídas correctamente (%ld)\n", cont);
		printf("buffreducidas tiene %ld elementos y %d bloques\n", buffreducidas.elementos, buffreducidas.bloques_reservados);
		
		// Como es la identidad no necesitamos ni calcularlo xd
		fprintf(salida, "NumPerm;Pem;Ciclos;Frecuencia\n");
		printf("NumPerm;Pem;Ciclos;Frecuencia\n");
		fprintf(salida, "%d;%d", 0, perm[0]);
		printf("%d;%d", 0, perm[0]);
		for (i = 1; i < tam; i++) {
			fprintf(salida, " %d", perm[i]);
			printf(" %d", perm[i]);
		}
		fprintf(salida, ";();%ld\n", cont);
		printf(";();%ld\n", cont);
		
		permunivs = gen_perm_univs(&buffreducidas, salida_univ);
		printf("%ld permutaciones universales\n", permunivs->elementos);
		
		//for (i = 0; i < permunivs->elementos; i++) escribir_array(salida_univ, get_from_mibuff(permunivs, i), permunivs->tam);
		
		long int frecuencia;
		int pos = numpares - 1;
		for (num_perm = 0; ; num_perm++) {
			if (!avanzar_permutacion(perm, pos, numpares)) {
				if (--pos == -1) break;
				continue;
			} else {
				//mostrar_array(perm, tam);
				pos = numpares - 1;
				if (ya_en_cociente(perm, permunivs)) continue;
				num_perm++;
			}
			
			frecuencia = 0;
			for (cont = 0; cont < buffreducidas.elementos; cont++) {
				reducida = get_from_mibuff(&buffreducidas, cont);
				permutar_reducidas(perm, reducida, newreducida, n);
				if (es_matriz_reducida(newreducida, n)) frecuencia++;
			}
			if (frecuencia > 0) {
				fprintf(salida, "%ld;%d", num_perm, perm[0]);
				printf("%ld;", num_perm);
				printf("%d", perm[0]);
				for (i = 1; i < numpares; i++) {
					fprintf(salida, " %d", perm[i]);
					printf(" %d", perm[i]);
				}
				fprintf(salida, ";");
				putchar(';');
				//perm_to_ciclos(perm, permciclada, numpares);
				//escribir_ciclos(salida, permciclada, numpares);
				//mostrar_ciclos(permciclada);
				fprintf(salida, ";%ld\n", frecuencia);
				printf(";%ld\n", frecuencia);
			}
		}
	}
	return 0;
}
