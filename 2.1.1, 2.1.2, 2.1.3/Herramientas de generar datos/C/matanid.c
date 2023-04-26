#include "matanid.h"


char *esprimo; // Donde se almacenará la criba de eratostenes

struct mibuffer *matrices_generadas, *matriz_anterior, *matriz_posterior, *buff_filas, *buffsignos;
//int **matriz_anterior, **matriz_posterior;
int *primera, *ultima;

long int *filas_posibles;
long int *num_generadas;
long int *duplicidades;

void inicializar_var_globales(int n) {
	matrices_generadas = calloc(n, sizeof(struct mibuffer));
	buff_filas = calloc(n, sizeof(struct mibuffer));
	buffsignos = calloc(n, sizeof(struct mibuffer));
	//matriz_anterior = calloc(n, sizeof(int *));
	//matriz_posterior = calloc(n, sizeof(int *));
	primera = malloc(n*sizeof(int));
	ultima = malloc(n*sizeof(int));
	
	for (int k = 0; k < n; k++) {
		buff_filas[k].bloques_reservados = 0;
		buffsignos[k].bloques_reservados = 0;
		matrices_generadas[k].bloques_reservados = 0;
		
		buff_filas[k].elemxbloque = MAT_X_BLOQUE;
		buffsignos[k].elemxbloque = MAT_X_BLOQUE;
		matrices_generadas[k].elemxbloque = MAT_X_BLOQUE;
		
		buff_filas[k].elementos = 0;
		buffsignos[k].elementos = 0;
		matrices_generadas[k].elementos = 0;
		
		buff_filas[k].tam = 2*(k+1)+1;
		buffsignos[k].tam = 2*(k+1)+1;
		matrices_generadas[k].tam = 8*(k+1);
	}
}

void inicializar_buff_hilo(struct buffthread *buff_hilo, int n) {
	//buff_hilo = malloc(n, sizeof(struct buffthread));
	
	buff_hilo->n = n;
	buff_hilo->salida = NULL;
	
	inicializar_mibuff(&buff_hilo->buff_filas, 2*n+1, ELEM_X_BLOQUE);
	printf("buff_filas inicializado\n");
	inicializar_mibuff(&buff_hilo->buffsignos, 2*n+1, ELEM_X_BLOQUE);
	printf("buffsignos inicializado\n");
	inicializar_mibuff(&buff_hilo->matrices_generadas, 8*n, ELEM_X_BLOQUE);
	printf("matrices_generadas inicializado\n");
	inicializar_mibuff(&buff_hilo->matriz_anterior, 1, ELEM_X_BLOQUE);
	printf("matriz_anterior inicializado\n");
	inicializar_mibuff(&buff_hilo->matriz_posterior, 1, ELEM_X_BLOQUE);
	printf("matriz_posterior inicializado\n");
	
	buff_hilo->hitos.subhitos = NULL;
	buff_hilo->hitos.dist = 100;
}

// Si el bloque no está reservado, lo reservamos
inline void reservar_from_mibuff(struct mibuffer *mibuff, long int num) {
	while (bloque_actual(mibuff, num) >= mibuff->bloques_reservados) {
		mibuff->buff[mibuff->bloques_reservados] = (int*) malloc(mibuff->elemxbloque*mibuff->tam*sizeof(int));
		if (mibuff->buff[mibuff->bloques_reservados] == NULL) {
			printf("malloc no puede asignar la memoria :(\n");
			exit(1);
		}
		mibuff->bloques_reservados++;
	}
}

// Si el bloque no está reservado, lo reservamos
inline void reservar_from_mibuffptr(struct mibufferptr *mibuff, long int num) {
	while (bloque_actual(mibuff, num) >= mibuff->bloques_reservados) {
		mibuff->buff[mibuff->bloques_reservados] = (void**) malloc(mibuff->elemxbloque*sizeof(void*));
		if (mibuff->buff[mibuff->bloques_reservados] == NULL) {
			printf("malloc no puede asignar la memoria :(\n");
			exit(1);
		}
		mibuff->bloques_reservados++;
	}
}

inline int* get_from_mibuff (struct mibuffer *mibuff, long int num) {
	if (bloque_actual(mibuff, num) >= mibuff->bloques_reservados) reservar_from_mibuff(mibuff, num);
	return &mibuff->buff[bloque_actual(mibuff, num)][elem_actual(mibuff, num)*mibuff->tam];
}

inline void* get_from_mibuffptr(struct mibufferptr *mibuff, long int num) {
	reservar_from_mibuffptr(mibuff, num);
	return mibuff->buff[bloque_actual(mibuff, num)][elem_actual(mibuff, num)];
}

inline void** get_ptr_from_mibuffptr(struct mibufferptr *mibuff, long int num) {
	reservar_from_mibuffptr(mibuff, num);
	return &mibuff->buff[bloque_actual(mibuff, num)][elem_actual(mibuff, num)];
}

inline void colocar_despues (struct buffthread *buff_hilo, int num_actual, int i, int n) {
	*get_from_mibuff(&buff_hilo->matriz_anterior, num_actual) = i;
	*get_from_mibuff(&buff_hilo->matriz_posterior,num_actual) = *get_from_mibuff(&buff_hilo->matriz_posterior, i);
	*get_from_mibuff(&buff_hilo->matriz_posterior, i) = num_actual;
	
	if (*get_from_mibuff(&buff_hilo->matriz_posterior, num_actual) != -1) *get_from_mibuff(&buff_hilo->matriz_anterior, *get_from_mibuff(&buff_hilo->matriz_posterior, num_actual)) = num_actual;
}

inline void colocar_antes (struct buffthread *buff_hilo, int num_actual, int i, int n) {
	*get_from_mibuff(&buff_hilo->matriz_anterior, num_actual) = *get_from_mibuff(&buff_hilo->matriz_anterior, i);
	*get_from_mibuff(&buff_hilo->matriz_posterior, num_actual) = i;
	*get_from_mibuff(&buff_hilo->matriz_anterior, i) = num_actual;
	
	if (*get_from_mibuff(&buff_hilo->matriz_anterior, num_actual) != -1) *get_from_mibuff(&buff_hilo->matriz_posterior, *get_from_mibuff(&buff_hilo->matriz_anterior, num_actual)) = num_actual;
}

/* Utilizamos la Criba de Erastótenes (https://es.wikipedia.org/wiki/Criba_de_Erat%C3%B3stenes)
   para buscar todos los primos hasta el doble del máximo central posible */
void gen_esprimo(char *esprimo, int cmax) {
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

void mostrar_esprimo(int max) {
	for (int i = 0; i < max; i++) {
		if (esprimo[i]) printf("%d ", i);
	}
	printf("\n");
}

int cuantos_primos(int tope) {
	int k;
	int numprimos = 0;
	for (k = 0; k < tope; k++) {
		numprimos = numprimos + esprimo[k];
	}
	return numprimos;
}

/*void old_gen_primos_posibles (int c, int numeros_posibles[]) {
	// genera una lista de primos en [0, 2c] con tales que p = c (mod 6)
	// los primos posibles se escriben en primos_posibles[2:], que deberá
	// tener tamaño ((c-1)/6)*2 + 1
	// numeros_posibles[0] = cantidad de numeros posibles
	int numero_posible = c-6;
	int countnumpos = 0;
	while (numero_posible > 0) {
		if (esprimo[numero_posible] && esprimo[2*c-numero_posible]) {
			numeros_posibles[countnumpos+1] = numero_posible;
			numeros_posibles[countnumpos+2] = 2*c-numero_posible;
			countnumpos = countnumpos+2;
		}
		numero_posible = numero_posible - 6;
	}
	numeros_posibles[0] = countnumpos;
}*/

void gen_primos_posibles (struct paresposibles *parposib) {
	int c = parposib->c;
	int numero_posible = c-6;
	int countnumpos = 0;
	while (numero_posible > 0) {
		if (esprimo[numero_posible] && esprimo[2*c-numero_posible]) {
			parposib->posibles[countnumpos]= numero_posible;
			//numeros_posibles[countnumpos+2] = 2*c-numero_posible;
			//printf("Par (%d, %d) encontrado\n", parposib->posibles[countnumpos], 2*c - parposib->posibles[countnumpos]);
			countnumpos++;
		}
		numero_posible = numero_posible - 6;
	}
	parposib->cuantos_total = countnumpos;
	//printf("parposib->cuantos_total = %d\n", parposib->cuantos_total);
}

int buscar_elemento(int elemento, int *array, int cuantos) {
	//busca un elemento en un array y devuelve su posición
	for (int i = 0; i < cuantos; i++) {
		if (elemento == array[i]) return i;
	}
	return -1;
}

void elim_primos_usados(int **mat_anid, int n, struct paresposibles *parposib) {
	int i, j, k; // k nivel de anidación, i el elemento de ese nivel de anidación, j el índice de los primos posibles
	
	if (parposib->usados == NULL) parposib->usados = malloc(sizeof(int)* parposib->cuantos_usados);
	
	int indice_usados = 0;
	parposib->cuantos = parposib->cuantos_total;
	for(k = 1; k < n; k++) {
		for (i = 0; i < 8*k; i++) { // hay 8k elementos en el nivel k de anidación
			if (mat_anid[k][i] > parposib->c) continue;
			//printf("Eliminando el elemento %d del nivel %d: %d\n", i, k, mat_anid[k][i]);
			parposib->usados[indice_usados] = mat_anid[k][i];
			for (j = 0; j < parposib->cuantos; j++) {
				if (parposib->posibles[j] == parposib->usados[indice_usados]) {
					parposib->posibles[j] = parposib->posibles[parposib->cuantos-1];
					parposib->posibles[parposib->cuantos-1] = parposib->usados[indice_usados];
					parposib->cuantos--;
					break;
				} else if (j == parposib->cuantos - 1) {
					printf("No se encuentra el primo %d en primos posibles\n", parposib->usados[indice_usados]);
					printf("Lo buscamos otra vez en la posición %d de %d\n", buscar_elemento(parposib->usados[indice_usados], parposib->posibles, parposib->cuantos_total), parposib->cuantos_total);
				}
			}
			indice_usados++;
		}
	}
	
	if (indice_usados != parposib->cuantos_usados) printf("Error: no se han encontrado todos los usados!!\n");
}

int terminar_linea(FILE *entrada) {
	char c;
	for (;;){
		c = getc(entrada);
		if (c == '\n') {
			return 0;
		}
		if (c == EOF) {
			printf("Fin del archivo\n");
			return 1;
		}
	}
}

int leer_anidada_entera(FILE *entrada, int *matriz_anid[], int n) {
	char c;
	char numero[MAX_DIGITOS_PRIMOS+1];
	numero[0] = '\0';
	int pos_num = 0;
	int k= 0; // el nivel de anidación
	int i = 0; // la posición en la anidación
	for (int pos = 0; ; pos++) {
		c = getc(entrada);
		if (c == EOF) {
			printf("Fin del archivo\n");
			return 1;
		}
		if (c == ',' || c == ';') {
			numero[pos_num] = '\0';
			*(matriz_anid[k]+i) = atoi(numero);
			//printf("%s, ", numero);
			pos_num = 0;
			numero[0] = '\0';
			if (++i >= 8*k) {
				//printf("\n");
				if (++k == n) {
					//printf("\n");
					return terminar_linea(entrada);
				}
				i = 0;
			}
			if (c == '\n') {
				return 0; //terminar_linea(entrada);
			}
			continue;
		}
		if (pos_num > MAX_DIGITOS_PRIMOS) {
			printf("Número demasiado grande\n");
			printf("%s\n", numero);
			return 1;
		}
		numero[pos_num] = c;
		pos_num++;
	}
	return 0;
}

int leer_anidada(FILE *entrada, int *matriz_anid[], int n) {
	char c;
	char numero[MAX_DIGITOS_PRIMOS+1];
	numero[0] = '\0';
	int pos_num = 0;
	int k = 0; // el nivel de anidación
	int i = 0; // la posición en la anidación
	//int central;
	for (int pos = 0; ; pos++) {
		c = getc(entrada);
		if (c == EOF) {
			printf("Fin del archivo\n");
			return 1;
		}
		if (c == ',' || c == ';') {
			numero[pos_num] = '\0';
			matriz_anid[k][i] = atoi(numero);
			//printf("[%d][%d] = %d\n", k, i, matriz_anid[k][i]);
			//printf("%s, ", numero);
			pos_num = 0;
			numero[0] = '\0';
			
			if (k == 0) {
				//central = matriz_anid[0][0];
				//printf("Central = %d\n", matriz_anid[0][0]);
				//k++;
			}
			else if (i == 0) {
				matriz_anid[k][8*k-1] = 2*matriz_anid[0][0] - matriz_anid[k][0];
				//printf("[%d][%d] = %d - %d = %d\n", k, 8*k-1, 2*matriz_anid[0][0], matriz_anid[k][i], matriz_anid[k][8*k-1]);
				i++;
			}
			else if (i < 2*k) {
				matriz_anid[k][6*k-1+i] = 2*matriz_anid[0][0] - matriz_anid[k][i];
				//printf("[%d][%d] = %d - %d = %d\n", k, 6*k-1+i, 2*matriz_anid[0][0], matriz_anid[k][i], matriz_anid[k][6*k-1+i]);
				i++;
			}
			else if (i == 2*k) {
				matriz_anid[k][6*k-1] = 2*matriz_anid[0][0] - matriz_anid[k][i];
				//printf("[%d][%d] = %d - %d = %d\n", k, 6*k-1, 2*matriz_anid[0][0], matriz_anid[k][i], matriz_anid[k][6*k-1]);
				i++;
			}
			else if (i > 2*k) {
				matriz_anid[k][i+1] = 2*matriz_anid[0][0] - matriz_anid[k][i];
				//printf("[%d][%d] = %d - %d = %d\n", k, i+1, 2*matriz_anid[0][0], matriz_anid[k][i], matriz_anid[k][i+1]);
				i = i+2;
			}
			
			if (i >= 6*k-1) {
				//printf("Subimos de nivel\n");
				if (++k == n) {
					//printf("Terminar linea\n");
					return terminar_linea(entrada);
				}
				i = 0;
			}
			if (c == '\n') {
				return 0; //terminar_linea(entrada);
			}
			continue;
		}
		if (pos_num > MAX_DIGITOS_PRIMOS) {
			printf("Número demasiado grande\n");
			printf("%s\n", numero);
			return 1;
		}
		numero[pos_num] = c;
		pos_num++;
	}
	return 0;
}

int leer_reducida(FILE *entrada, int *reducida, int n) {
	char c;
	char numero[MAX_DIGITOS_PRIMOS+1];
	numero[0] = '\0';
	int pos_num = 0;
	int i = 0; // la posición en la anidación
	for (int pos = 0; ; pos++) {
		c = getc(entrada);
		if (c == EOF) {
			printf("Fin del archivo\n");
			return 1;
		}
		if (c == ',' || c == ';') {
			numero[pos_num] = '\0';
			reducida[i] = atoi(numero);
			//printf("[%d][%d] = %d\n", k, i, matriz_anid[k][i]);
			//printf("%s, ", numero);
			pos_num = 0;
			numero[0] = '\0';
		}			
		if (c == '\n') {
			return 0; //terminar_linea(entrada);
		}

		if (pos_num > MAX_DIGITOS_PRIMOS) {
			printf("Número demasiado grande\n");
			printf("%s\n", numero);
			return 1;
		}
		numero[pos_num] = c;
		pos_num++;
	}
	return 0;
}

int leer_linea_csv(FILE *entrada, int *array, int tam) {
	char c;
	char numero[MAX_DIGITOS_PRIMOS+1];
	numero[0] = '\0';
	int pos_num = 0;
	int i = 0; // la posición del número
	for (int pos = 0; ; pos++) {
		c = getc(entrada);
		if (c == EOF) {
			printf("Fin del archivo\n");
			return 1;
		}
		if (c == ',' || c == '\n') {
			numero[pos_num] = '\0';
			//printf("(%p, %s)\n", &array[i], numero);
			array[i] = atoi(numero);
			//printf("%s, ", numero);
			pos_num = 0;
			numero[0] = '\0';
			if (c == '\n') {
				return 0; //terminar_linea(entrada);
			}
			if (++i >= tam) {
				return terminar_linea(entrada);
			}
			continue;
		}
		if (pos_num > MAX_DIGITOS_PRIMOS) {
			printf("Número demasiado grande\n");
			printf("%s\n", numero);
			return 1;
		}
		numero[pos_num] = c;
		pos_num++;
	}
	return 0;
}

int escribir_anidada(FILE *salida, int *matriz_anid[], int n) {
	int k, i; // k el nivel de anidación, i la posición dentro del nivel
	// Escribimos el nivel 0
	//printf("Central: %d\n", matriz_anid[0][0]);
	//putchar('.');
	fprintf(salida, "%d,", matriz_anid[0][0]);
	
	for (k = 1; k <= n; k++) {
		for (i = 0; i <= 2*k; i++) {
			fprintf(salida, "%d,", matriz_anid[k][i]);
		}
		for (i = 2*k+1; i < 6*k-3; i=i+2) {
			fprintf(salida, "%d,", matriz_anid[k][i]);
		}
		if (k < n) fprintf(salida, "%d,", matriz_anid[k][i]);
		else fprintf(salida, "%d\n", matriz_anid[k][i]);
	}
	return 0;
}

int escribir_anidada_entera(FILE *salida, int **matriz_anid, int *nueva_anid, int n) {
	int k, i; // k el nivel de anidación, i la posición dentro del nivel
	// Escribimos el nivel 0
	fprintf(salida, "%d,", matriz_anid[0][0]);
	
	for (k = 1; k < n; k++) {
		for (i = 0; i < 8*k; i++) {
			fprintf(salida, "%d,", matriz_anid[k][i]);
		}
	}
	for (i = 0; i < 8*n-1; i++) {
		fprintf(salida, "%d,", nueva_anid[i]);
	}
	fprintf(salida, "%d\n", nueva_anid[i]);
	return 0;
}

int escribir_array(FILE *salida, int *array, int elementos) {
	if (salida == NULL) return 1;
	int k;
	if (elementos == 0) {
		fprintf(salida, "\n");
		return 0;
	}
	for (k = 0; k < elementos-1; k++) {
		fprintf(salida, "%d,", array[k]);
	}
	fprintf(salida, "%d\n", array[k]);
	return 0;
}

int escribir_array_sep(FILE *salida, int *array, int elementos, char *separador, char *final) {
	int k;
	if (elementos == 0) {
		fprintf(salida, final);
		return 0;
	}
	for (k = 0; k < elementos-1; k++) {
		fprintf(salida, "%d%s", array[k], separador);
	}
	fprintf(salida, "%d%s", array[k], final);
	return 0;
}

long int exponencial(int base, int exponente) {
	if (exponente < 0) {
		return 0;
	}
	int resultado = 1;
	int k;
	for (k = 0; k < exponente; k++) {
		resultado = resultado * base;
	}
	//printf("exp(%d,%d) = %d\n", base, exponente, resultado);
	return resultado;
}

void rellenrar_matriz(int matriz [], int c, int generadores[], int n) {
	//printf("El problema está en rellenar matriz");
	int k, i;
	matriz[0] = generadores[0]; // primer elemento
	matriz[8*n-1] = 2*c - matriz[0]; // su opuesto
	
	matriz[2*n-1] = (2*n+1)*c - matriz[0]; // el elemento 2n (penúltimo) se va calculando poco a poco para que la fila valga (2n+1)*c
	
	// Rellenamos la primera fila
	for (k = 1; k < 2*n-1; k++) {
		matriz[k] = generadores[k]; // elemento k de la primera fila
		matriz[6*n+k-1] = 2*c - matriz[k]; //elemento k de la última fila
		matriz[2*n-1] = matriz[2*n-1] - matriz[k]; //el penúltimo  elemento de la primera fila actualizandose
		//mostrar_matriz(matriz, mat_anid, n);
		//printf("\n");
	}
	
	// Rellenamos las columnas
	i = 2*n+1;
	matriz[6*n-1] = (2*n+1)*c - matriz[0];
	for (; k < 4*n-2; k++) {
		matriz[i] = generadores[k];
		matriz[i+1] = 2*c - matriz[i];
		matriz[6*n-1] = matriz[6*n-1] - matriz[i]; //el último de la primera columna actualizandose
		i = i + 2;
		//mostrar_matriz(matriz, mat_anid, n);
		//printf("\n");
	}
	
	// Completado el elem 6n, actualizamos 2n+1, 2n y 6n+1
	matriz[2*n] = 2*c - matriz[6*n-1];
	matriz[2*n-1] = matriz[2*n-1] - matriz[2*n];
	matriz[8*n-2] = 2*c - matriz[2*n-1]; // el opuesto de 2n
	//mostrar_matriz(matriz, mat_anid, n);
	//printf("\n");
}

int ordenar_burbuja(int* array, int elementos) {
	int i, j, aux_elem, movimientos;
	
	movimientos = 0;
	for (int i = 0; i < elementos - 1; i++) {
		for (j = 1; j < elementos; j++) {
			if (array[j] < array[j-1]) {   // si el elemento anterior es mayor, hacemos el cambio
				aux_elem = array[j];
				array[j] = array[j-1];
				array[j-1] = aux_elem;
				movimientos++;
			}
		}
	}
	return movimientos;
}

int es_array_menor(int *matriz1, int *matriz2, int tam) {
	for (int i = 0; i < tam; i++) {
		if (matriz1[i] < matriz2[i] ) {
			return 1;
		}
		if (matriz1[i] > matriz2[i] ) {
			return 0;
		}
	}
	return 0;
}

int es_array_mayor(int *matriz1, int *matriz2, int tam) {
	for (int i = 0; i < tam; i++) {
		if (matriz1[i] > matriz2[i] ) {
			return 1;
		}
		if (matriz1[i] < matriz2[i] ) {
			return 0;
		}
	}
	return 0;
}

int es_array_igual(int *matriz1, int *matriz2, int tam) {
	for (int i = 0; i < tam; i++) {
		if (matriz1[i] != matriz2[i] ) {
			return 0;
		}
	}
	return 1;
}

int comp_arrays(int* array1, int* array2, int elementos) {
	// Devuelve 1 si son iguales y 0 si son distintas
	int k;
	for (k = 0; k < elementos; k++) {
		if (array1[k] != array2[k]) {
			return 0;
		}
	}
	return 1;
}

int es_matriz_prima(int matriz[], int n) {
	int k;
	for (k = 0; k < 8*n; k++) {
		if (matriz[k] < 2) {
			//printf("[%d][%d] = %d < 2\n", n, k, matriz[k]);
			return 0;
		}
		if (esprimo[matriz[k]] == 0) {
			//printf("%d no es primo\n", matriz[k]);
			return 0;
		}
	}
	
	// Vemos si hay elementos repetidos
	int matriz_ordenada[8*n];
	copiar_array(matriz, matriz_ordenada, 8*n);
	ordenar_burbuja(matriz_ordenada, 8*n);
	for (k = 1; k < 8*n; k++) {
		if (matriz_ordenada[k-1] == matriz_ordenada[k]) {
			//printf("Hay elementos repetidos %d %d\n", matriz_ordenada[k-1], matriz_ordenada[k]);
			return 0;
		}
	}
	return 1;
}

int es_matriz_anidada(int **mat_anid, int n) {
	// partimos de que ya está por pares y son primos
	int k, i, fila1, fila2, col1, col2;
	for (k = 1, fila1 = 0, fila2 = 0, col1 = 0, col2 = 0; k <= n; k++) {
		for (i = 0; i < 8*k; i++) {
			if (i < 2*k+1) fila1 = fila1 + mat_anid[k][i];
			else if (i <= 6*k-1 && i%2 == 1) col1 = col1 + mat_anid[k][i];
			else if (i <= 6*k-1 && i%2 == 0) col2 = col2 + mat_anid[k][i];
			else fila2 = fila2 + mat_anid[k][i];
		}
		col1 = col1 + mat_anid[k][0];
		col2 = col2 + mat_anid[k][2*k] + mat_anid[k][8*k-1];
		fila2 = fila2 + mat_anid[k][6*k-1];
		if (fila1 != (2*k+1)*mat_anid[0][0]) {
			//printf("fila 1 = %d\n", fila1);
			return 0;
		}
		if (fila2 != (2*k+1)*mat_anid[0][0]) {
			//printf("fila 2 = %d\n", fila2);
			return 0;
		}
		if (col1 != (2*k+1)*mat_anid[0][0]) {
			//printf("col 1 = %d\n", col1);
			return 0;
		}
		if (col2 != (2*k+1)*mat_anid[0][0]) {
			//printf("col 2 = %d\n", col1);
			return 0;
		}
	}
	return 1;
}

int es_matriz_reducida(int *reducida, int n) {
	int i, j, fila, col, c = reducida[0];
	for (int k = 1; k <= n; k++) {
		i = ((2*k-1)*(2*k-1)-1)/2 + 1;
		fila = reducida[i];
		
		for (j = 1; j < 2*k+1; j++) fila = fila + reducida[i+j];
		
		if (fila != (2*k+1)*c) return 0;
		
		col = reducida[i] + 2*c - reducida[i+2*k];
		i = i + 2*k;
		for (j= 1; j <= 2*k-1; j++) col = col + reducida[i+j];
		
		if (col != (2*k+1)*c) return 0;
	}
	return 1;
}

int esquinas_ordenadas(int matriz[], int n) {
	// poner la esquina menor en la primera posición
	if (matriz[2*n] < matriz[0] && matriz[2*n] < matriz[8*n-1]) {
		// si la segunda esquina es la menor, hacemos una simetría vertical
		return 0;
	}
	else if (matriz[2*n] > matriz[0] && matriz[2*n] > matriz[8*n-1]) {
		// si la segunda esquina es la mayor, entonces la tercera es la menor, y hacemos una simetría horizontal
		return 0;
	}
	else if (matriz[0] > matriz[2*n] && matriz[0] > matriz[8*n-1]) {
		// si la primera esquina es la mayor, entonces la última es la menor, y hacemos una simetría vertical y otra horizontal
		return 0;
	}
	
	if (matriz[2*n] > matriz[6*n-1]) {
		// si la segunda esquina es mayor que la primera hacemos una simetría diagonal.
		return 0;
	}
	return 1;
}

int es_fila_ordenada(int matriz[], int n) {
	for (int j = 2; j < 2*n; j++) {
		if (matriz[j] < matriz [j-1]) {
			return 0;
		}
	}
	return 1;
}

int es_col_ordenada(int matriz[], int n) {
	for (int j = 2*n+3; j < 6*n-1; j = j+2) {
		if (matriz[j] < matriz [j-2]) {
			return 0;
		}
	}
	return 1;
}

int no_repetidos(int **mat_anid, int n) {
	int i, j, k;
	for (k = 1; k < n; k++) {
		for (i = 0; i < 8*k; ++i) {
			for (j = 0; j < 8*n; ++j) if (mat_anid[k][i] == mat_anid[n][j]) return 0;
		}
	}
	return 1;
}

void mostrar_fila(int fila, int *matriz, int *mat_anid[], int n, char *linea) {
	int i;
	if (fila == 0) {
		for (i = 0; i < 2*n+1; i++) {
			sprintf(linea, "%s%d\t", linea, matriz[i]);
		}
		return;
	}
	if (fila == 2*n) {
		for (i = 6*n-1; i < 8*n; i++) {
			sprintf(linea, "%s%d\t", linea, matriz[i]);
		}
		return;
	}
	sprintf(linea, "%s%d\t", linea, matriz[2*n+2*(fila-1)+1]);
	mostrar_fila(fila-1, mat_anid[n-1], mat_anid, n-1, linea);
	sprintf(linea, "%s%d\t", linea, matriz[2*n+2*(fila)]);
}

void mostrar_matriz(int *matriz, int *mat_anid[], int n) {
	char linea[7*n+7];
	for (int fila = 0; fila < 2*n+1; fila++) {
		sprintf(linea, "(%d)\t", fila);
		mostrar_fila(fila, matriz, mat_anid, n, linea);
		strcat(linea, "\n");
		printf(linea);
	}
}

#define mostrar_array(array, elementos) ({\
	for (int karray = 0; karray < elementos; karray++) printf("%d ", array[karray]);\
	printf("\n"); })

void mostrar_primos_posibles(int *primos_posibles) {
	int r = primos_posibles[0];
	printf("Primos posibles: %d\n", r);
	for (int i = 1; i < r; i++) {
		printf("%d, ", primos_posibles[i]);
	}
	printf("%d.\n", primos_posibles[r]);
}

void mostrar_primos_usados(int *primos_usados, int n) {
	int r = (2*n-1)*(2*n-1) - 1;
	int i;
	printf("Primos usados: %d\n", r);
	for (i = 0; i < r-1; i++) {
		printf("%d, ", primos_usados[i]);
	}
	printf("%d.\n", primos_usados[i]);
}



/*void test_get_fila(int num_filas_posibles) {
	int *fila;
	int n = 2;
	printf("\nTest get fila\n");
	for (int i = 0; i < num_filas_posibles; i++) {
		fila = get_fila(i, n);
		printf("(Fila %d) ", i);
		for (int j = 0; j < 2*n+1; j++) {
			printf("%d ", fila[j]);
		}
		printf("\n");
	}
}*/

int avanzar_indices(int *indices, int tope, int tam) {
	// devuelve 0 si no se puede avanzar mas, y 1 en caso contrario
	if (tam == 0) {
		return 0;
	}
	if (indices[tam-1] >= tope || indices[tam-1] < 0) {
		printf("Índice inválido\n");
		mostrar_array(indices, tam);
		exit(1);
	}
	if (++indices[tam-1] == tope) {
		for (;;) {
			if (!avanzar_indices(indices, tope-1, tam-1)) {
				return 0;
			}
			
			indices[tam-1] = indices[tam-2]+1;
			return 1;
		}
	}
	return 1;
}

int avanzar_signos(int *signos, int tam) {
	// devuelve 0 si no se puede avanzar mas, y 1 en caso contrario
	if (tam == 0) {
		return 0;
	}
	if (signos[tam-1] == 0) {
		signos[tam-1] = 1;
		//putchar('-');
		//putchar('\n');
		return 1;
	}
	if (signos[tam-1] == 1) {
		signos[tam-1] = 0;
		//putchar('+');
		return avanzar_signos(signos, tam-1);
	}
	printf("Signo inválido\n");
	exit(1);
}

inline void simetria_vertical(int *matriz, int n) {
	int aux;
	aux = matriz[2*n];
	matriz[2*n] = matriz[0];
	matriz[0] = aux;
	
	aux = matriz[8*n-1];
	matriz[8*n-1] = matriz[6*n-1];
	matriz[6*n-1] = aux;
	
	// intercambiamos el interior de las columnas
	for (int i = 2*n+1; i < 6*n-1; i = i+2) {
		aux = matriz[i];
		matriz[i] = matriz[i+1];
		matriz[i+1] = aux;
	}
}

inline void simetria_horizontal(int *matriz, int n) {
	int aux;
	aux = matriz[6*n-1];
	matriz[6*n-1] = matriz[0];
	matriz[0] = aux;
	
	aux = matriz[2*n];
	matriz[2*n] = matriz[8*n-1];
	matriz[8*n-1] = aux;
	
	// intercambiamos el interior de las filas
	for (int i = 1; i < 2*n; i++) {
		aux = matriz[i];
		matriz[i] = matriz[6*n+i-1];
		matriz[6*n+i-1] = aux;
	}
}

inline void simetria_diagonal(int *matriz, int n) {
	int aux;
	aux = matriz[6*n-1];
	matriz[6*n-1] = matriz[2*n];
	matriz[2*n] = aux;
	
	// intercambiamos filas y columnas
	for (int i = 1; i < 2*n; i++) {
		aux = matriz[i];
		matriz[i] = matriz[2*n+2*i-1];
		matriz[2*n+2*i-1] = aux;
		
		aux = matriz[6*n+i-1];
		matriz[6*n+i-1] = matriz[2*n+2*i];
		matriz[2*n+2*i] = aux;
	}
}

inline void ordenar_filas(int *matriz, int n) {
	int aux;
	for (int i = 1; i < 2*n; i++) {
		for (int j = 2; j < 2*n; j++) {
			if (matriz[j] < matriz [j-1]) {
				aux = matriz[j];
				matriz[j] = matriz[j-1];
				matriz[j-1] = aux;
				
				aux = matriz[6*n+j-2];
				matriz[6*n+j-2] = matriz[6*n+j-1];
				matriz[6*n+j-1] = aux;
			}
		}
	}
}

inline void ordenar_columnas(int *matriz, int n) {
	int aux;
	for (int i = 1; i < 2*n; i++) {
		for (int j = 2*n+3; j < 6*n-1; j = j+2) {
			if (matriz[j] < matriz [j-2]) {
				aux = matriz[j];
				matriz[j] = matriz[j-2];
				matriz[j-2] = aux;
				
				aux = matriz[j-1];
				matriz[j-1] = matriz[j+1];
				matriz[j+1] = aux;
			}
		}
	}
}

inline void ordenar_matriz(int *matriz, int n) {
	// poner la esquina menor en la primera posición
	if (matriz[2*n] < matriz[0] && matriz[2*n] < matriz[8*n-1]) {
		// si la segunda esquina es la menor, hacemos una simetría vertical
		simetria_vertical(matriz, n);
	}
	else if (matriz[2*n] > matriz[0] && matriz[2*n] > matriz[8*n-1]) {
		// si la segunda esquina es la mayor, entonces la tercera es la menor, y hacemos una simetría horizontal
		simetria_horizontal(matriz, n);
	}
	else if (matriz[0] > matriz[2*n] && matriz[0] > matriz[8*n-1]) {
		// si la primera esquina es la mayor, entonces la última es la menor, y hacemos una simetría vertical y otra horizontal
		simetria_horizontal(matriz, n);
		simetria_vertical(matriz, n);
	}
	
	if (matriz[2*n] > matriz[6*n-1]) {
		// si la segunda esquina es mayor que la primera hacemos una simetría diagonal.
		simetria_diagonal(matriz, n);
	}
	
	ordenar_filas(matriz, n);
	ordenar_columnas(matriz, n);
}

void inicializar_filas(int n) {
	//if (buff_filas == NULL) buff_filas = calloc(n, sizeof(struct mibuffer));
	for (int k = 0; k < n; k++) {
		//buff_filas[k] = malloc(sizeof(struct mibuffer));
		buff_filas[k].elemxbloque = ELEM_X_BLOQUE;
		//buff_filas[n-1].tam = tam;
		buff_filas[k].bloques_reservados = 0;
		buff_filas[k].elementos = 0;
	}
}

void mostrar_filas(int n) {
	printf("Hay %ld filas\n", buff_filas[n-1].elementos);
	for (int i = 0; i < buff_filas[n-1].elementos; i++) {
		mostrar_array(get_from_mibuff(&buff_filas[n-1], i), buff_filas[n-1].tam);
	}
}

void inicializar_signos(int n) {
	for (int k = 0; k < n; k++) {
		buffsignos[k].bloques_reservados = 0;
		buffsignos[k].elementos = 0;
		buffsignos[k].elemxbloque = MAT_X_BLOQUE;
		buffsignos[k].tam = buff_filas[n-1].tam;
	}
}

void gen_signos_pa_filas(struct mibuffer *buffsignos) {
	buffsignos->elementos = 0;
	int *signos = get_from_mibuff(buffsignos, 0);
	for (int k = 0; k < buffsignos->tam; k++) signos[k] = 0; // inicializamos los signos
		
	do {
		buffsignos->elementos++;
		signos = get_from_mibuff(buffsignos, buffsignos->elementos);
		copiar_array(get_from_mibuff(buffsignos, buffsignos->elementos-1), signos, buffsignos->tam);
	} while (avanzar_signos(signos, buffsignos->tam));
}

int gen_filas(int c, struct paresposibles *parposib, int valor, int n) {
	//inicializar_filas(n);
	buff_filas[n-1].elementos = 0;
	int *fila, i, k, suma, num_signo;
	//printf("buff_filas[n-1].tam = %d\n", buff_filas[n-1].tam);
	int indices[buff_filas[n-1].tam];
	int *signos; //[buff_filas[n-1].tam];
	
	//printf("Inicializamos los índices\n");
	for (k = 0; k < buff_filas[n-1].tam; k++) {
		indices[k] = k;
		//signos[k] = 0;
	}
	//mostrar_array(indices, buff_filas[n-1].tam);
	
	fila = get_from_mibuff(&buff_filas[n-1], buff_filas[n-1].elementos);
	do {
		for (num_signo = 0; num_signo < buffsignos[n-1].elementos; num_signo++) {
			signos = get_from_mibuff(&buffsignos[n-1], num_signo);
			//mostrar_array(signos, buff_filas[n-1].tam);
			//putchar('\t');
			suma = 0;
			for (i = 0; i < buff_filas[n-1].tam; i++) {
				if (signos[i] == 0) {
					suma = suma + parposib->posibles[indices[i]];
				} else {
					suma = suma + 2*c - parposib->posibles[indices[i]];
				}
				if (suma > valor) {
					break;
				}
			}
			if (suma != valor) {
				continue;
			}
			
			for (k = 0; k < buff_filas[n-1].tam; k++) {
				if (signos[k] == 0) {
					fila[k] = parposib->posibles[indices[k]];
				} else {
					fila[k] = 2*c - parposib->posibles[indices[k]];
				}
			}
			ordenar_burbuja(fila, buff_filas[n-1].tam);
			//mostrar_array(fila, buff_filas[n-1].tam);
			buff_filas[n-1].elementos++;
			fila = get_from_mibuff(&buff_filas[n-1], buff_filas[n-1].elementos);
		} //while (avanzar_signos(signos, buff_filas[n-1].tam));
	} while (avanzar_indices(indices, parposib->cuantos, buff_filas[n-1].tam));
	return buff_filas[n-1].elementos;
}

int gen_filas_hilo(struct buffthread *buff_hilo, int valor) {
	int c = buff_hilo->c;
	
	//inicializar_filas(n);
	buff_hilo->buff_filas.elementos = 0;
	int *fila, i, k, suma, num_signo;
	//printf("buff_filas[n-1].tam = %d\n", buff_filas[n-1].tam);
	int indices[buff_hilo->buff_filas.tam];
	int *signos; //[buff_filas[n-1].tam];
	
	//printf("Inicializamos los índices\n");
	for (k = 0; k < buff_hilo->buff_filas.tam; k++) {
		indices[k] = k;
		//signos[k] = 0;
	}
	//mostrar_array(indices, buff_filas[n-1].tam);
	
	fila = get_from_mibuff(&buff_hilo->buff_filas, buff_hilo->buff_filas.elementos);
	do {
		for (num_signo = 0; num_signo < buff_hilo->buffsignos.elementos; num_signo++) {
			signos = get_from_mibuff(&buff_hilo->buffsignos, num_signo);
			//mostrar_array(signos, buff_filas[n-1].tam);
			//putchar('\t');
			suma = 0;
			for (i = 0; i < buff_hilo->buff_filas.tam; i++) {
				if (signos[i] == 0) {
					suma = suma + buff_hilo->parposib->posibles[indices[i]];
				} else {
					suma = suma + 2*c - buff_hilo->parposib->posibles[indices[i]];
				}
				if (suma > valor) {
					break;
				}
			}
			if (suma != valor) {
				continue;
			}
			
			for (k = 0; k < buff_hilo->buff_filas.tam; k++) {
				if (signos[k] == 0) {
					fila[k] = buff_hilo->parposib->posibles[indices[k]];
				} else {
					fila[k] = 2*c - buff_hilo->parposib->posibles[indices[k]];
				}
			}
			ordenar_burbuja(fila, buff_hilo->buff_filas.tam);
			//mostrar_array(fila, buff_hilo->buff_filas.tam);
			buff_hilo->buff_filas.elementos++;
			fila = get_from_mibuff(&buff_hilo->buff_filas, buff_hilo->buff_filas.elementos);
		} //while (avanzar_signos(signos, buff_hilo->buff_filas.tam));
	} while (avanzar_indices(indices, buff_hilo->parposib->cuantos, buff_hilo->buff_filas.tam));
	return buff_hilo->buff_filas.elementos;
}

int gen_filas_3_hilo(struct buffthread *buff_hilo, int valor) {
	int c = buff_hilo->c;
	
	//inicializar_filas(n);
	buff_hilo->buff_filas.elementos = 0;
	int *fila, i, suma, aux;
	//printf("buff_filas[n-1].tam = %d\n", buff_filas[n-1].tam);
	int indices[3] = {0, 1, 2};
	
	fila = get_from_mibuff(&buff_hilo->buff_filas, buff_hilo->buff_filas.elementos);
	do {
		for (i = 0; i < 3; ++i) {
			fila[0] = buff_hilo->parposib->posibles[indices[0]];
			fila[1] = 2*c - buff_hilo->parposib->posibles[indices[1]];
			fila[2] = buff_hilo->parposib->posibles[indices[2]];
			
			aux = indices[2];
			indices[2] = indices[1];
			indices[1] = indices[0];
			indices[0] = aux;
			
			suma = fila[0] + fila[1] + fila[2];
			if (suma != valor) continue;
			
			aux = fila[0];
			fila[0] = (aux < fila[2])*fila[0] + (aux > fila[2])*fila[2];
			fila[2] = (aux < fila[2])*fila[2] + (aux > fila[2])*fila[0];
			
			buff_hilo->buff_filas.elementos++;
			fila = get_from_mibuff(&buff_hilo->buff_filas, buff_hilo->buff_filas.elementos);
		}
	} while (avanzar_indices(indices, buff_hilo->parposib->cuantos, buff_hilo->buff_filas.tam));
	return buff_hilo->buff_filas.elementos;
}

void reset_hitos(struct buffthread *buff_hilo) {
	int cont, num_matriz = buff_hilo->primera, niveles = 0, k;
	buff_hilo->hitos.dist = 100;
	for (cont = buff_hilo->matrices_generadas.elementos/100; (cont = cont/10) > 0; ++niveles) buff_hilo->hitos.dist = buff_hilo->hitos.dist*10;
	
	int indices[niveles];
	struct hitos_busqueda  *hitos[niveles];
	for (cont = 0; cont < niveles; ++cont) indices[cont] = 0;
	
	hitos[0] = &buff_hilo->hitos;
	for (k = 1; k < niveles; ++k) {
		if (hitos[k-1]->subhitos == NULL) {
			hitos[k-1]->subhitos = malloc(sizeof(struct hitos_busqueda)*10);
			hitos[k-1]->subhitos->subhitos = NULL;
		}
		hitos[k] = hitos[k-1]->subhitos;
		hitos[k]->dist = hitos[k-1]->dist/10;
	}
	
	for (cont = 0; cont < buff_hilo->matrices_generadas.elementos; ++cont) {
		if (cont %100 == 0) for (k = 0; k < niveles; ++k) if (cont % hitos[k]->dist) hitos[k]->hitos[indices[k]++] = num_matriz;
	}
}

int append_matriz(int num_actual, struct buffthread *buff_hilo) {
	// devuelve 1 si se añade la matriz y 0 si no se añade (ya estaba)
	//printf("Append matriz\n");
	
	int n = buff_hilo->n, i, k;
	if (num_actual == 0) {
		//printf("num_actual == 0\n");
		*get_from_mibuff(&buff_hilo->matriz_anterior, num_actual) = -1;
		*get_from_mibuff(&buff_hilo->matriz_posterior, num_actual) = -1;
		buff_hilo->primera = num_actual;
		buff_hilo->ultima = num_actual;
		//reset_busqueda(buff_hilo, 1, c);
		buff_hilo->hitos.dist = 100;
		//printf("Hemos terminado\n");
		return 1;
	}
	//int i = num_actual-1; // empezamos desde el anterior que se añadió
	int *matriz_actual;
	matriz_actual = get_from_mibuff(&buff_hilo->matrices_generadas, num_actual);
	//int c = buff_hilo->c;
	
	i = buff_hilo->primera;
	if (num_actual > 1000) {
		struct hitos_busqueda *hitos = &buff_hilo->hitos;
		busqueda_hitos:
		for (k = 0; (k < 10); k++) {
			if (es_matriz_menor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, hitos->hitos[k]), n)) break;
			else i = hitos->hitos[k];
		}
		if (hitos->subhitos != NULL) {
			hitos = hitos->subhitos;
			//printf("goto\n");
			goto busqueda_hitos;
		}
	}
	//printf("Empezamos a buscar por la matriz %d\n", i);
	int sentido = 0; // si vamos hacia abajo o arriba
	//int *mat_anid[1];
	//mat_anid[0] = &c;
	while(1) {
		if (sentido < 0) { // estamos bajando
			if (es_matriz_mayor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				// ya no podemos bajar mas
				//printf("La colocamos antes de %d\n", i);
				colocar_despues(buff_hilo, num_actual, i, n);
				return 1;
			}
			if (es_matriz_menor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				if (*get_from_mibuff(&buff_hilo->matriz_anterior, i) == -1) {
					// es la primera
					//printf("Es la primera\nLa colocamos antes de %d\n", i);
					colocar_antes(buff_hilo, num_actual, i, n);
					buff_hilo->primera = num_actual;
					return 1;
				}
				i = *get_from_mibuff(&buff_hilo->matriz_anterior, i);
				//printf("Pasamos a la matriz %d\n", i);
				continue;
			}
			// si hemos llegado hasta aquí es porque son iguales
			return 0;
		}
		if (sentido > 0) { // estamos subiendo
			if (es_matriz_menor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				// ya no podemos bajar mas
				//printf("La colocamos antes de %d\n", i);
				colocar_antes(buff_hilo, num_actual, i, n);
				return 1;
			}
			if (es_matriz_mayor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				// es la última
				if (*get_from_mibuff(&buff_hilo->matriz_posterior, i) == -1) {
					//printf("Es la última\nLa colocamos después de %d\n", i);
					colocar_despues(buff_hilo, num_actual, i, n);
					buff_hilo->ultima = num_actual;
					return 1;
				}
				i = *get_from_mibuff(&buff_hilo->matriz_posterior, i);
				//printf("Pasamos a la matriz %d\n", i);
				continue;
			}
			// si hemos llegado hasta aquí es porque son iguales
			return 0;
		}
		if (sentido == 0) {
			if (es_matriz_menor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				if (*get_from_mibuff(&buff_hilo->matriz_anterior, i) == -1) {
					// es la primera
					//printf("Es la primera\nLa colocamos antes de %d\n", i);
					colocar_antes(buff_hilo, num_actual, i, n);
					buff_hilo->primera = num_actual;
					return 1;
				}
				sentido = -1; //baja
				//printf("Bajamos\n");
				i = *get_from_mibuff(&buff_hilo->matriz_anterior, i);
				//printf("Pasamos a la matriz %d\n", i);
				continue;
			}
			if (es_matriz_mayor(matriz_actual, get_from_mibuff(&buff_hilo->matrices_generadas, i), n)) {
				if (*get_from_mibuff(&buff_hilo->matriz_posterior, i) == -1) {
					// es la última
					//printf("Es la última\nLa colocamos después de %d\n", i);
					colocar_despues(buff_hilo, num_actual, i, n);
					buff_hilo->ultima = num_actual;
					return 1;
				}
				sentido = 1; //sube
				//printf("Subimos\n");
				i = *get_from_mibuff(&buff_hilo->matriz_posterior,i);
				//printf("Pasamos a la matriz %d\n", i);
				continue;
			}
			// si hemos llegado hasta aquí es porque son iguales
			//printf("Hemos terminado y son iguales\n");
			return 0;
		}
	}
}

int ceros_fila(int *fila, int c, int p, int tam) {
	int ceros = 0;
	for (int i = 0; i < tam; i++) {
		if (fila[i] == 0) ceros++;
		if ((2*c - fila[i]) % p == 0) ceros++;
	}
	return ceros;
}

int ceros_array(int *array, int p, int tam) {
	int ceros = 0;
	for (int i = 0; i < tam; i++) if (array[i] == 0) ceros++;
	return ceros;
}

void gen_marcos_3_mod_p(struct buffthread *hilo_modulo, int p) {
	int *fila, *mat_actual, i, sum, valor, num_fila, n = hilo_modulo->n;
	for(int c = 0; c < p; c++) {
		hilo_modulo->c = c;
		valor = (3*c) % p;
		
		fila = get_from_mibuff(&hilo_modulo->buff_filas, (hilo_modulo->buff_filas.elementos = 0));
		
		for (i = 0; i < 3; i++) fila[i] = 0;
		
		while (1) {
			// Los elementos estarán ordenados de menor a mayor y podrán repetirse.
			if (ceros_fila(fila, c, p, 3) < 2) {
				sum = 0;
				for (i = 0; i < 3; i++) sum = sum + fila[i];
				
				if ((sum = sum % p) == valor) {
					copiar_array(fila, get_from_mibuff(&hilo_modulo->buff_filas, ++hilo_modulo->buff_filas.elementos), hilo_modulo->buff_filas.tam);
					fila = get_from_mibuff(&hilo_modulo->buff_filas, hilo_modulo->buff_filas.elementos);
				}
			}
			
			i = hilo_modulo->buff_filas.tam-1;
			fila[i] = fila[i] + valor;
			if (fila[i] >= p) for (--i; i >= 0; --i) if (++fila[i] >= p)  break;
			if (i < 0) break;
			else for (; i < 2*n; i++) fila[i+1] = fila[i];
		}
		
		hilo_modulo->matrices_generadas.elementos = 0;
		mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, 0);
		
		for (num_fila = 0; num_fila < hilo_modulo->buff_filas.elementos; num_fila++) {
			fila = get_from_mibuff(&hilo_modulo->buff_filas, num_fila);
			mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos);
			
			mat_actual[0] = c;
			mat_actual[1] = fila[0];
			mat_actual[2] = fila[1];
			mat_actual[3] = fila[2];
			mat_actual[6] = 2*c - mat_actual[3];
			mat_actual[7] = 2*c - mat_actual[2];
			mat_actual[8] = 2*c - mat_actual[1];
			mat_actual[4] = 3*c - mat_actual[1] - mat_actual[5];
			mat_actual[5] = 2*c - mat_actual[4];
			
			for (i = 6; i < 9; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
			
			ordenar_matriz(mat_actual + 1, 1);
			if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
				escribir_array(hilo_modulo->salida, mat_actual, 9);
				hilo_modulo->matrices_generadas.elementos++;
			}
			
			mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos);
			
			mat_actual[0] = c;
			mat_actual[1] = fila[0];
			mat_actual[2] = fila[1];
			mat_actual[3] = fila[2];
			mat_actual[6] = 2*c - mat_actual[3];
			mat_actual[7] = 2*c - mat_actual[2];
			mat_actual[8] = 2*c - mat_actual[1];
			mat_actual[4] = 3*c - mat_actual[1] - mat_actual[5];
			mat_actual[5] = 2*c - mat_actual[4];
			
			for (i = 6; i < 9; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
			
			ordenar_matriz(mat_actual + 1, 1);
			if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
				escribir_array(hilo_modulo->salida, mat_actual, 9);
				hilo_modulo->matrices_generadas.elementos++;
			}
			
			mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos++);
			
			mat_actual[0] = c;
			mat_actual[1] = fila[0];
			mat_actual[2] = fila[1];
			mat_actual[3] = fila[2];
			mat_actual[6] = 2*c - mat_actual[3];
			mat_actual[7] = 2*c - mat_actual[2];
			mat_actual[8] = 2*c - mat_actual[1];
			mat_actual[4] = 3*c - mat_actual[1] - mat_actual[5];
			mat_actual[5] = 2*c - mat_actual[4];
			
			for (i = 6; i < 9; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
			
			ordenar_matriz(mat_actual + 1, 1);
			if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
				escribir_array(hilo_modulo->salida, mat_actual, 9);
				hilo_modulo->matrices_generadas.elementos++;
			}
		}
	}
}

void gen_marcos_3_mod_c(struct buffthread *hilo_modulo, int c, int p) {
	hilo_modulo->c = c;
	
	int *fila = get_from_mibuff(&hilo_modulo->buff_filas, (hilo_modulo->buff_filas.elementos = 0));
	int i, sum, valor = (3*c) % p, n = hilo_modulo->n;
	for (i = 0; i < 3; i++) fila[i] = 0;
	
	while (1) {
		// Los elementos estarán ordenados de menor a mayor y podrán repetirse.
		
		if (ceros_fila(fila, c, p, 3) < 2) {
			sum = 0;
			for (i = 0; i < 3; i++) sum = sum + fila[i];
			
			if ((sum = sum % p) == valor) {
				copiar_array(get_from_mibuff(&hilo_modulo->buff_filas, ++hilo_modulo->buff_filas.elementos), fila, hilo_modulo->buff_filas.tam);
				fila = get_from_mibuff(&hilo_modulo->buff_filas, hilo_modulo->buff_filas.elementos);
			}
		}
		
		for (i = hilo_modulo->buff_filas.tam-1; i >= 0; --i) {
			if (++fila[i] >= p)  break;
		}
		if (i < 0) break;
		else for (; i < 2*n; i++) fila[i+1] = fila[i];
	}
	
	int num_fila; //, num_col, esquina[2], otraesquina[2], *mat_actual;
	
	hilo_modulo->matrices_generadas.elementos = 0;
	int *mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, 0);
	
	for (num_fila = 0; num_fila < hilo_modulo->buff_filas.elementos; num_fila++) {
		fila = get_from_mibuff(&hilo_modulo->buff_filas, num_fila);
		mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos);
		
		mat_actual[0] = fila[0];
		mat_actual[1] = fila[1];
		mat_actual[2] = fila[2];
		mat_actual[5] = 2*c - mat_actual[2];
		mat_actual[6] = 2*c - mat_actual[1];
		mat_actual[7] = 2*c - mat_actual[0];
		mat_actual[3] = 3*c - mat_actual[0] - mat_actual[5];
		mat_actual[4] = 2*c - mat_actual[3];
		
		for (i = 5; i < 8; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
		
		ordenar_matriz(mat_actual, 1);
		if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
			escribir_array(hilo_modulo->salida, mat_actual, 8);
			hilo_modulo->matrices_generadas.elementos++;
		}
		
		mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos);
		
		mat_actual[0] = fila[1];
		mat_actual[1] = fila[0];
		mat_actual[2] = fila[2];
		mat_actual[5] = 2*c - mat_actual[2];
		mat_actual[6] = 2*c - mat_actual[1];
		mat_actual[7] = 2*c - mat_actual[0];
		mat_actual[3] = 3*c - mat_actual[0] - mat_actual[5];
		mat_actual[4] = 2*c - mat_actual[3];
		
		for (i = 5; i < 8; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
		
		ordenar_matriz(mat_actual, 1);
		if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
			escribir_array(hilo_modulo->salida, mat_actual, 8);
			hilo_modulo->matrices_generadas.elementos++;
		}
		
		mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos++);
		
		mat_actual[0] = fila[0];
		mat_actual[1] = fila[2];
		mat_actual[2] = fila[1];
		mat_actual[5] = 2*c - mat_actual[2];
		mat_actual[6] = 2*c - mat_actual[1];
		mat_actual[7] = 2*c - mat_actual[0];
		mat_actual[3] = 3*c - mat_actual[0] - mat_actual[5];
		mat_actual[4] = 2*c - mat_actual[3];
		
		for (i = 5; i < 8; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
		
		ordenar_matriz(mat_actual, 1);
		if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
			escribir_array(hilo_modulo->salida, mat_actual, 8);
			hilo_modulo->matrices_generadas.elementos++;
		}
	}
}

void gen_filas_mod_p(struct mibuffer *bufilas, int valor, int p, int cerosposibles) {
	int tam = bufilas->tam;
	int fila[tam];
	int i = 0;
	if (cerosposibles == 1) {
		fila[0] = 0;
		i++;
	}
	for (; i < tam-1; i++) {
		fila[i] = 1;
		fila[tam-1]++;
	}
	if (fila[tam-1] <= valorfila) fila[tam-1] = (valorfila - fila[tam-1]) % p;
	else fila[tam-1] = (valorfila - fila[tam-1] - ((valorfila - fila[tam-1])/p-1)*p) % p;
	
	if (fila[tam-1] == 0) {
		if (valorfila != 0) fila[tam-1] = valorfila;
		else {
			fila[tam-1] = p-1;
			fila[tam-2]++;
		}
	}
	
	cerosposibles = mat_actual[1] != 0;
	while (1) {
		if (ceros_fila(fila, c, p, tam) <= cerosposibles) {
			sum = 0;
			for (i = 0; i < tam; i++) sum = sum + fila[i];
			
			if ((sum = sum % p) == valorfila) {
				for (i = 0; i < tam-1; ++i) printf("%d + ", fila[i]);
				printf("%d = %d\n", fila[i], sum);
				copiar_array(fila, get_from_mibuff(bufilas, bufilas->elementos), bufilas->tam);
				//mostrar_array(get_from_mibuff(&hilo_modulo_p->buff_filas, hilo_modulo_p->buff_filas.elementos), hilo_modulo_p->buff_filas.tam);
				bufilas->elementos++;
			}
		}
		
		for (i = tam-1; i >= 0; --i) {
			if (++fila[i] < p) break;
		}
		if (i < 0) break;
		else for (; i < tam-1; i++) fila[i+1] = fila[i];
	}
}

void rellenar_aristas_marco(int *mat_actual, int *fila, int *col, int n) {
	int i, j;
	for (i = 0; i < 2*n-1; ++i) {
		mat_actual[2+i] = fila[i];
		mat_actual[6*n+i+1] = 2*c - fila[i];
		j++;
	}
	for (i = 0; i < 2*n-1; ++i) {
		mat_actual[2*n+2+2*i] = col[i];
		mat_actual[2*n+2+2*i+1] = 2*c - col[i];
	}
	
	for (i = 2*n+2; i < 8*n+1; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
}

void gen_marcos_3_mod_p(struct buffthread *hilo_modulo_p, int p) {
	//int n = hilo_modulo_p->n;
	for (int c = 0; c < p; c++) {
		mat_actual = get_from_mibuff(&hilo_modulo_p->matrices_generadas, hilo_modulo_p->matrices_generadas.elementos);
		mat_actual[0] = c;
		for (mat_actual[1] = 0; mat_actual[1] < p; ++mat_actual[1]) {
			valor_mod_p(mat_actual[8], 2*c - mat_actual[1], p);
			
			if (mat_actual[8] < mat_actual[1]) continue; // ya lo habremos calculado
			
			for (mat_actual[3] = mat_actual[1] + (mat_actual[1] == 0); mat_actual[3] < p; ++mat_actual[3]) {
				valor_mod_p(mat_actual[6], 2*c - mat_actual[3], p);
				
				if (mat_actual[6*n] < mat_actual[2*n+1]) continue; // ya lo habremos calculado
				
				valor_mod_p(mat_actual[6], 3*c - mat_actual[1] - mat_actual[3], p);
				valor_mod_p(mat_actual[6], 3*c - mat_actual[1] - mat_actual[6], p);
				
			}
		}
	}
}

void gen_marcos_mod_p(struct buffthread *hilo_modulo_p, int p, int n) {
	if (n == 1) {
		gen_marcos_3_mod_p(hilo_modulo_p, p);
		return;
	}
	
	int *fila, *col, i, j, sum, valorfila, valorcol, mat_actual[8*n+1], cerosposibles, last_fila, num_fila, num_col;
	
	if (hilo_modulo_p->buff_filas.tam != 2*n-1) {
		printf("hilo_modulo_p->buff_filas.tam = %d != 2*n-1\n", hilo_modulo_p->buff_filas.tam);
		exit(1);
	}
	
	for (int c = 0; c < p; c++) {
		mat_actual[0] = c;
		for (mat_actual[1] = 0; mat_actual[1] < p; ++mat_actual[1]) {
			mat_actual[8*n] = 2*c - mat_actual[1];
			if (mat_actual[8*n] < 0) mat_actual[8*n] = (mat_actual[8*n] - (mat_actual[8*n]/p - 1)*p) % p;
			else mat_actual[8*n] = mat_actual[8*n] % p;
			
			if (mat_actual[8*n] < mat_actual[1]) continue; // ya lo habremos calculado
			
			for (mat_actual[2*n+1] = mat_actual[1] + (mat_actual[1] == 0); mat_actual[2*n+1] < p; ++mat_actual[2*n+1]) {
				mat_actual[6*n] = 2*c - mat_actual[2*n+1];
				if (mat_actual[6*n] < 0) mat_actual[6*n] = (mat_actual[6*n] - (mat_actual[6*n]/p - 1)*p) % p;
				else mat_actual[6*n] = mat_actual[6*n] % p;
				
				if (mat_actual[6*n] < mat_actual[2*n+1]) continue; // ya lo habremos calculado
				
				valorfila = ((2*n+1)*c - mat_actual[1] - mat_actual[2*n+1]) % p;
				valorcol = ((2*n+1)*c - mat_actual[1] - mat_actual[6*n]) % p;
				
				hilo_modulo_p->buff_filas.elementos = 0;
				
				gen_filas_mod_p(&hilo_modulo_p->buff_filas , valorfila, p, cerosposibles);
				last_fila = hilo_modulo_p->buff_filas.elementos;
				
				if (valorfila != valorcol) gen_filas_mod_p(&hilo_modulo_p->buff_filas , valorfila, p, cerosposibles);
				
				for (num_fila = 0; num_fila < last_fila; num_fila++) {
					fila = get_from_mibuff(&hilo_modulo_p->buff_filas, num_fila);
					
					if (valorfila != valorcol) num_col = last_fila;
					else num_col = num_fila + 1;
					
					for (; num_col < hilo_modulo_p->buff_filas.elementos; num_col++) {
						col = get_from_mibuff(&hilo_modulo_p->buff_filas, num_col);
						
						rellenar_aristas_marco(mat_actual, fila, col, n);
						copiar_array(mat_actual, get_from_mibuff(&hilo_modulo_p->matrices_generadas, hilo_modulo_p->matrices_generadas.elementos), 8*n+1);
						
						//ordenar_matriz(mat_actual+1, n);
						if (append_matriz(hilo_modulo_p->matrices_generadas.elementos, hilo_modulo_p)) {
							hilo_modulo_p->matrices_generadas.elementos++;
							escribir_array(hilo_modulo_p->salida, mat_actual, hilo_modulo_p->matrices_generadas.tam);
						}
					}
				}
			}
		}
	}
}

void old_gen_marcos_mod_p(struct buffthread *hilo_modulo_p, int p, int n) {
	if (n == 1) {
		gen_marcos_3_mod_p(hilo_modulo_p, p);
		return;
	}
	
	int *fila, *col, i, j, sum, valor;
	int num_fila, num_col, esquina[2], otraesquina[2], *mat_actual;
	for (int c = 0; c < p; c++) {
		hilo_modulo_p->c = c;
		hilo_modulo_p->buff_filas.elementos = 0;
		valor = ((2*n+1)*c) % p;
		
		// Los elementos estarán ordenados de menor a mayor y podrán repetirse (salvo el 0, que podrá estar como maximo una vez).
		fila = malloc(sizeof(int)*(2*n+1));
		fila[0] = 0;
		for (i = 1; i < 2*n+1; i++) fila[i] = 1;
		
		while (1) {
			if (ceros_fila(fila, c, p, 2*n+1) < 2) {
				sum = 0;
				for (i = 0; i < 2*n+1; i++) sum = sum + fila[i];
				
				if ((sum = sum % p) == valor) {
					for (i = 0; i < 2*n; ++i) printf("%d + ", fila[i]);
					printf("%d = %d\n", fila[i], sum);
					copiar_array(fila, get_from_mibuff(&hilo_modulo_p->buff_filas, hilo_modulo_p->buff_filas.elementos), hilo_modulo_p->buff_filas.tam);
					//mostrar_array(get_from_mibuff(&hilo_modulo_p->buff_filas, hilo_modulo_p->buff_filas.elementos), hilo_modulo_p->buff_filas.tam);
					hilo_modulo_p->buff_filas.elementos++;
				}
			}
			
			for (i = 2*n; i >= 0; --i) {
				if (++fila[i] < p)  break;
			}
			if (i < 0) break;
			else for (; i < 2*n; i++) fila[i+1] = fila[i];
		}
		free(fila);
		
		printf("%ld filas generadas para el valor %d\n", hilo_modulo_p->buff_filas.elementos, valor);
		
		//hilo_modulo_p->matrices_generadas.elementos = 0;
		
		for (num_fila = 0; num_fila < hilo_modulo_p->buff_filas.elementos; num_fila++) {
			fila = get_from_mibuff(&hilo_modulo_p->buff_filas, num_fila);
			
			//if (ceros_fila(fila, c, p, 2*n+1) > 1) continue;
			for (num_col = num_fila+1; num_col < hilo_modulo_p->buff_filas.elementos; num_col++) {
				printf("fila %d, columna %d\r", num_fila, num_col);
				
				col = get_from_mibuff(&hilo_modulo_p->buff_filas, num_col);
				//if (ceros_fila(fila, c, p, 2*n+1)) continue;
				
				for (esquina[0] = 0; esquina[0] < hilo_modulo_p->buff_filas.tam; esquina[0]++) for (esquina[1] = 0; esquina[1] < hilo_modulo_p->buff_filas.tam; esquina[1]++) {
					if (col[esquina[1]] > fila[esquina[0]]) break;
					if (col[esquina[1]] < fila[esquina[0]]) continue;
					
					for (otraesquina[0] = 0; otraesquina[0] < hilo_modulo_p->buff_filas.tam; otraesquina[0]++) for (otraesquina[1] = 0; otraesquina[1] < hilo_modulo_p->buff_filas.tam; otraesquina[1]++) {
						if (otraesquina[0] == esquina[0]) break;
						if (otraesquina[1] == esquina[1]) continue;
						
						valor = (2*c - fila[otraesquina[0]])%p;
						
						if (col[otraesquina[1]] > valor) break;
						if (col[otraesquina[1]] < valor) continue;
						
						mat_actual = get_from_mibuff(&hilo_modulo_p->matrices_generadas, hilo_modulo_p->matrices_generadas.elementos);
						mat_actual[0] = c;
						mat_actual[1] = fila[esquina[0]];
						mat_actual[2*n+1] = fila[otraesquina[0]];
						mat_actual[6*n] = col[otraesquina[1]];
						mat_actual[8*n] = (2*c - fila[esquina[0]]);
						j = 2;
						for (i = 0; i < 2*n+1; ++i) {
							if (i == esquina[0] || i == otraesquina[0]) continue;
							mat_actual[j] = fila[i];
							mat_actual[6*n-1+j] = 2*c - fila[i];
							j++;
						}
						j = 2*n+2;
						for (i = 0; i < 2*n+1; ++i) {
							if (i == esquina[1] || i == otraesquina[1]) continue;
							mat_actual[j++] = col[i];
							mat_actual[j++] = 2*c - col[i];
						}
						
						for (i = 1; i < 8*n+1; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
						
						ordenar_matriz(mat_actual+1, n);
						if (append_matriz(hilo_modulo_p->matrices_generadas.elementos, hilo_modulo_p)) {
							hilo_modulo_p->matrices_generadas.elementos++;
							escribir_array(hilo_modulo_p->salida, mat_actual, hilo_modulo_p->matrices_generadas.tam);
						}
						
						// Ahora evitamos que se repita otraesquina[1] y se genere la misma matriz
						for (; otraesquina[1] < hilo_modulo_p->buff_filas.tam - 1; otraesquina[1]++) {
							if (col[otraesquina[1]] != col[otraesquina[1]+1]) break;
						}
						if (otraesquina[1] < hilo_modulo_p->buff_filas.tam) continue;
						
						// si hemos llegado al final comprobamos que no se repita otraesquina[0]
						for (; otraesquina[0] < hilo_modulo_p->buff_filas.tam - 1; otraesquina[0]++) {
							if (col[otraesquina[0]] != col[otraesquina[0]+1]) break;
						}
						if (otraesquina[0] < hilo_modulo_p->buff_filas.tam) continue;
						
						// si hemos llegado al final comprobamos que no se repita esquina[1]
						for (; esquina[1] < hilo_modulo_p->buff_filas.tam - 1; esquina[1]++) {
							if (col[esquina[1]] != col[esquina[1]+1]) break;
						}
						if (esquina[1] < hilo_modulo_p->buff_filas.tam) continue;
						
						// si hemos llegado al final comprobamos que no se repita esquina[0]
						for (; esquina[0] < hilo_modulo_p->buff_filas.tam - 1; esquina[0]++) {
							if (col[esquina[0]] != col[esquina[0]+1]) break;
						}
						if (esquina[0] < hilo_modulo_p->buff_filas.tam) continue;
					}
				}
				
			}
		}
		printf("%ld matrices generadas hasta el central %d modulo %d\n", hilo_modulo_p->matrices_generadas.elementos, c, p);
	}
}

void gen_marcos_mod_c(struct buffthread *hilo_modulo, int c, int p, int n) {
	if (n == 1) {
		gen_marcos_3_mod_c(hilo_modulo, c, p);
		return;
	}
	
	hilo_modulo->c = c;
	
	int *fila = get_from_mibuff(&hilo_modulo->buff_filas, (hilo_modulo->buff_filas.elementos = 0));
	int *col, i, j, sum, valor = ((2*n+1)*c)%p;
	for (i = 0; i < 2*n+1; i++) fila[i] = 0;
	
	while (1) {
		// Los elementos estarán ordenados de menor a mayor y podrán repetirse.
		if (ceros_fila(fila, c, p, 2*n+1) < 2) {
			sum = 0;
			for (i = 0; i < 2*n+1; i++) sum = sum + fila[i];
			
			if ((sum = sum % p) == valor) {
				copiar_array(get_from_mibuff(&hilo_modulo->buff_filas, ++hilo_modulo->buff_filas.elementos), fila, hilo_modulo->buff_filas.tam);
				fila = get_from_mibuff(&hilo_modulo->buff_filas, hilo_modulo->buff_filas.elementos);
			}
		}
		
		for (i = hilo_modulo->buff_filas.tam-1; i >= 0; --i) {
			if (++fila[i] >= p)  break;
		}
		if (i < 0) break;
		else for (; i < 2*n; i++) fila[i+1] = fila[i];
	}
	
	int num_fila, num_col, esquina[2], otraesquina[2], *mat_actual;
	
	hilo_modulo->matrices_generadas.elementos = 0;
	
	for (num_fila = 0; num_fila < hilo_modulo->buff_filas.elementos; num_fila++) {
		fila = get_from_mibuff(&hilo_modulo->buff_filas, num_fila);
		for (num_col = num_fila+1; num_col < hilo_modulo->buff_filas.elementos; num_col++) {
			col = get_from_mibuff(&hilo_modulo->buff_filas, num_col);
			
			for (esquina[0] = 0; esquina[0] < hilo_modulo->buff_filas.tam; esquina[0]++) for (esquina[1] = 0; esquina[1] < hilo_modulo->buff_filas.tam; esquina[1]++) {
				if (col[esquina[1]] > fila[esquina[0]]) break;
				if (col[esquina[1]] < fila[esquina[0]]) continue;
				
				for (otraesquina[0] = 0; otraesquina[0] < hilo_modulo->buff_filas.tam; otraesquina[0]++) for (otraesquina[1] = 0; otraesquina[1] < hilo_modulo->buff_filas.tam; otraesquina[1]++) {
					if (otraesquina[0] == esquina[0]) break;
					if (otraesquina[1] == esquina[1]) continue;
					
					valor = (2*c - fila[otraesquina[0]])%p;
					
					if (col[otraesquina[1]] > valor) break;
					if (col[otraesquina[1]] < valor) continue;
					
					mat_actual = get_from_mibuff(&hilo_modulo->matrices_generadas, hilo_modulo->matrices_generadas.elementos);
					mat_actual[0] = esquina[0];
					mat_actual[2*n] = otraesquina[0];
					mat_actual[6*n-1] = otraesquina[1];
					mat_actual[8*n-1] = (2*c - fila[esquina[0]]);
					j = 1;
					for (i = 0; i < 2*n+1; ++i) {
						if (i == esquina[0] || i == otraesquina[0]) continue;
						mat_actual[j] = fila[i];
						mat_actual[6*n-1+j] = (2*c - fila[i]);
						j++;
					}
					j = 2*n+1;
					for (i = 0; i < 2*n+1; ++i) {
						if (i == esquina[1] || i == otraesquina[1]) continue;
						mat_actual[j++] = col[i];
						mat_actual[j++] = (2*c - col[i]);
					}
					
					for (i = 1; i < 8*n; i++) if (mat_actual[i] < 0) mat_actual[i] = (mat_actual[i] - (mat_actual[i]/p - 1)*p) % p;
					
					ordenar_matriz(mat_actual, n);
					if (append_matriz(hilo_modulo->matrices_generadas.elementos, hilo_modulo)) {
						hilo_modulo->matrices_generadas.elementos++;
						escribir_array(hilo_modulo->salida, mat_actual, hilo_modulo->matrices_generadas.tam);
					}
					
					// Ahora evitamos que se repita otraesquina[1] y se genere la misma matriz
					for (; otraesquina[1] < hilo_modulo->buff_filas.tam - 1; otraesquina[1]++) {
						if (col[otraesquina[1]] != col[otraesquina[1]+1]) break;
					}
					if (otraesquina[1] < hilo_modulo->buff_filas.tam) continue;
					
					// si hemos llegado al final comprobamos que no se repita otraesquina[0]
					for (; otraesquina[0] < hilo_modulo->buff_filas.tam - 1; otraesquina[0]++) {
						if (col[otraesquina[0]] != col[otraesquina[0]+1]) break;
					}
					if (otraesquina[0] < hilo_modulo->buff_filas.tam) continue;
					
					// si hemos llegado al final comprobamos que no se repita esquina[1]
					for (; esquina[1] < hilo_modulo->buff_filas.tam - 1; esquina[1]++) {
						if (col[esquina[1]] != col[esquina[1]+1]) break;
					}
					if (esquina[1] < hilo_modulo->buff_filas.tam) continue;
					
					// si hemos llegado al final comprobamos que no se repita esquina[0]
					for (; esquina[0] < hilo_modulo->buff_filas.tam - 1; esquina[0]++) {
						if (col[esquina[0]] != col[esquina[0]+1]) break;
					}
					if (esquina[0] < hilo_modulo->buff_filas.tam) continue;
				}
			}
			
		}
	}
}

int buscar_matriz(int *matriz, struct buffthread *buff_hilo) {
	for (long int i = 0; i < buff_hilo->matrices_generadas.elementos; i++) {
		if (comp_arrays(matriz, get_from_mibuff(&buff_hilo->matrices_generadas, i), buff_hilo->matrices_generadas.tam)) return i;
	}
	return -1;
}

void clasificar_mod_p(struct mibuffer *matrices_generadas, struct buffthread *buff_hilo_mod_p, long int *elems_por_clase, int p) {
	int matriz_mod_p[matrices_generadas->tam], num_matriz, num_clase, n = buff_hilo_mod_p->n;
	
	for (num_matriz = 0; num_matriz < matrices_generadas->elementos; num_matriz++) {
		copiar_array(get_from_mibuff(matrices_generadas, num_matriz), matriz_mod_p, matrices_generadas->tam);
		for (int i = 0; i < 8*n; i++) matriz_mod_p[i] = matriz_mod_p[i] % p;
		ordenar_matriz(matriz_mod_p, buff_hilo_mod_p->n);
		
		num_clase = buscar_matriz(matriz_mod_p, buff_hilo_mod_p);
		
		if (num_clase < 0) {
			printf("Error, la matriz modulo %d ", p);
			mostrar_array(matriz_mod_p, matrices_generadas->tam);
			printf(" no está entre las matrices calculadas\n");
		} else elems_por_clase[num_clase]++;
	}
}

int gen_marcos_anid_3(struct buffthread *buff_hilo, int c) {
	int n = 1;
	printf("Calculando los marcos del nivel 1\n");
	int *matriz_actual = NULL, *fila;
	int aux, i;
	
	buff_hilo->matrices_generadas.elementos = 0;
	buff_hilo->hitos.dist = 100;
	
	for (i = 0; i < buff_hilo->buff_filas.elementos; i++) { // cada fila determina una matriz
		fila = get_from_mibuff(&buff_hilo->buff_filas, i);
		
		matriz_actual = get_from_mibuff(&buff_hilo->matrices_generadas, buff_hilo->matrices_generadas.elementos);
		
		// El elemento fila[2] será el del medio porque es el mayor
		matriz_actual[0] = fila[0];
		matriz_actual[1] = fila[1];
		matriz_actual[2] = fila[2];
		
		aux = c - matriz_actual[0] + matriz_actual[2]; // el  elemento (2,1)
		if (aux <= 0 || 2*c-aux <= 0) continue; //printf("Negativo!!\n");
		else if (!esprimo[aux]) continue; //printf("%d no es primo!!\n", aux);
		else if (!esprimo[2*c-aux]) continue; //printf("%d no es primo!!\n", 2*c-aux);
		
		matriz_actual[3] = aux;
		matriz_actual[5] = 2*c - matriz_actual[2];
		
		if (matriz_actual[3] == matriz_actual[5]) continue; // si los elementos (1,2) y (1,3) son iguales
		
		matriz_actual[4] = 2*c - aux;
		matriz_actual[6] = 2*c - matriz_actual[1];
		matriz_actual[7] = 2*c - matriz_actual[0];
		
		ordenar_matriz(matriz_actual, n);
		
		if (append_matriz(buff_hilo->matrices_generadas.elementos, buff_hilo)) {
			fprintf(buff_hilo->salida, "%d,", c);
			escribir_array(buff_hilo->salida, matriz_actual, 8*n);
			buff_hilo->matrices_generadas.elementos++;
			
			if (buff_hilo->matrices_generadas.elementos / buff_hilo->hitos.dist == 10) reset_hitos(buff_hilo);
		} else duplicidades[1]++;
	}
	
	printf("%ld matrices generadas en el nivel %d\n", buff_hilo->matrices_generadas.elementos, n);
		
	return buff_hilo->matrices_generadas.elementos;
}

int gen_marcos_anid_n(struct buffthread *buff_hilo, int c, int n) {
	printf("Calculando los marcos del nivel %d\n", n);
	
	int numgen = 4*n-2;
	int generadores[numgen]; // serán los índices de los generadores en primos_posibles
	int *matriz_actual = NULL;
	
	buff_hilo->matrices_generadas.elementos = 0;
	buff_hilo->hitos.dist = 100;
	
	int num_filas_posibles, num_fila, num_col, i, j, k, elem_iguales, elem_pares;
	int *fila, *col;
	int esquina[2], otraesquina[2];
	
	//num_filas_posibles = gen_filas(c, parposib, (2*n+1)*c, n);
	//mostrar_filas();
	num_filas_posibles = buff_hilo->buff_filas.elementos;
	
	filas_posibles[n+1] = num_filas_posibles;
	
	for (num_fila = 0; num_fila < num_filas_posibles-1; num_fila++) {
		fila = get_from_mibuff(&buff_hilo->buff_filas, num_fila);
		for (num_col = num_fila+1; num_col < num_filas_posibles; num_col++) {
			col = get_from_mibuff(&buff_hilo->buff_filas, num_col);
			elem_iguales = 0;
			elem_pares = 0;
			for (i = 0; i < buff_hilo->buff_filas.tam; i++) {
				for (j = 0; j < buff_hilo->buff_filas.tam; j++) {
					if (fila[i] == col[j]) {
						esquina[0] = i;
						esquina[1] = j;
						elem_iguales++;
					} else if (fila[i] == 2*c - col[j]) {
						otraesquina[0] = i;
						otraesquina[1] = j;
						elem_pares++;
					}
				}
			}
			
			if (elem_iguales != 1 || elem_pares != 1) continue;
			
			if (fila[esquina[0]] > c) continue;
			
			if (fila[otraesquina[0]] < fila[esquina[0]] || 2*c - col[otraesquina[1]] < fila[esquina[0]]) continue;
			
			// Rellenamos la primera fila
			generadores[0] = fila[esquina[0]]; // la esquina
			i = 0; // el elemento de la fila
			for (k = 1; k < 2*n-1; i++) {
				if (i == esquina[0]) continue;
				
				if (i == otraesquina[0]) continue;
				
				generadores[k] = fila[i]; // elemento k de la primera fila
				k++;
			}
			i = 0;
			for (; k < numgen; k++) {
				if (i == esquina[1]) i++;
				if (i == otraesquina[1]) i++;
				generadores[k] = col[i]; // elemento k de la primera columna
				i++;
			}
			
			matriz_actual = get_from_mibuff(&buff_hilo->matrices_generadas, buff_hilo->matrices_generadas.elementos);
			rellenrar_matriz(matriz_actual, c, generadores, n);
			
			if (es_matriz_prima(matriz_actual, n) == 0) continue;
			
			ordenar_matriz(matriz_actual, n);
			//mostrar_array(matriz_actual, 8*n);
			
			if (append_matriz(buff_hilo->matrices_generadas.elementos, buff_hilo)) {
				fprintf(buff_hilo->salida, "%d,", c);
				escribir_array(buff_hilo->salida, matriz_actual, 8*n); // matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
				buff_hilo->matrices_generadas.elementos++;
			} else duplicidades[n]++;
		}
	}
	
	printf("%ld matrices generadas en el nivel %d\n", buff_hilo->matrices_generadas.elementos, n);
		
	return buff_hilo->matrices_generadas.elementos;
}

/*int gen_marcos_anid(FILE **salida, struct paresposibles *parposib, int c, int n) {
	printf("Calculando los marcos del nivel %d\n", n);
	
	int numgen = 4*n-2;
	int r = parposib->cuantos_total;
	if (r < 4*n) {
		printf("No hay suficientes primos\n");
		return 0;
	}
	
	int tamano = 2*n+1;
	matrices_generadas[n-1].elementos = 0;
	buff_filas[n-1].tam = 2*n+1;
		
	int generadores[numgen]; // serán los índices de los generadores en primos_posibles
	int *matriz_actual = NULL;
	int aux, i, j, k;
	
	// Matrices 3x3
	if (n == 1) {
		//int *mat_anid[1];
		//mat_anid[0] = &c;
		int* fila;
		
		gen_filas(c, parposib, 3*c, n);
		printf("%ld filas generadas en el nivel %d\n", buff_filas[n-1].elementos, n);
		filas_posibles[n] = buff_filas[n-1].elementos;
		//mostrar_filas();
		for (i = 0; i < buff_filas[n-1].elementos; i++) { // cada fila determina una matriz
			fila = get_from_mibuff(&buff_filas[n-1], i);
			
			// Hacemos grupos de 2 esquinas
			for (j = 0; j < 3; j++) { // el elemento del centro de la primera fila
				matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
				matriz_actual[1] = fila[j];
				if (j == 0) {
					matriz_actual[0] = fila[1];
					matriz_actual[2] = fila[2];
				}
				else if (j == 1) {
					matriz_actual[0] = fila[0];
					matriz_actual[2] = fila[2];
				} else {
					matriz_actual[0] = fila[0];
					matriz_actual[2] = fila[1];
				}
				aux = c - matriz_actual[0] + matriz_actual[2]; // el  elemento (2,1)
				if (aux <= 0 || 2*c-aux <= 0) continue; //printf("Negativo!!\n");
				else if (!esprimo[aux]) continue; //printf("%d no es primo!!\n", aux);
				else if (!esprimo[2*c-aux]) continue; //printf("%d no es primo!!\n", 2*c-aux);
				
				matriz_actual[3] = aux;
				matriz_actual[5] = 2*c - matriz_actual[2];
				
				if (matriz_actual[3] == matriz_actual[5]) continue; // si los elementos (1,2) y (1,3) son iguales
				
				matriz_actual[4] = 2*c - aux;
				matriz_actual[6] = 2*c - matriz_actual[1];
				matriz_actual[7] = 2*c - matriz_actual[0];
				
				
				ordenar_matriz(matriz_actual, n);
				
				if (append_matriz(matrices_generadas[n-1].elementos, n)) {
					fprintf(salida[n-1], "%d,", c);
					escribir_array(salida[n-1], matriz_actual, 8*n);
					matrices_generadas[n-1].elementos++;
					//mostrar_matriz(matriz_actual, mat_anid, n);
				}
			}
		}
	}
	// Cuando la matriz no es 3x3
	else {
		int num_filas_posibles, num_fila, num_col, i, j, k, elem_iguales;
		int *fila, *col;
		int esquina[2], otraesquina[2];
		
		num_filas_posibles = gen_filas(c, parposib, (2*n+1)*c, n);
		//mostrar_filas();
		
		printf("%d filas posibles\n", num_filas_posibles);
		filas_posibles[n] = num_filas_posibles;
		
		for (num_fila = 0; num_fila < num_filas_posibles-1; num_fila++) {
			//fila = get_fila(num_fila, n);
			fila = get_from_mibuff(&buff_filas[n-1], num_fila);
			for (num_col = num_fila+1; num_col < num_filas_posibles; num_col++) {
				//col = get_fila(num_col, n);
				col = get_from_mibuff(&buff_filas[n-1], num_col);
				elem_iguales = 0;
				for (i = 0; i < tamano; i++) {
					for (j = 0; j < tamano; j++) {
						if (fila[i] == col[j]) {
							esquina[0] = i;
							esquina[1] = j;
							elem_iguales++;
						}
					}
				}
				if (elem_iguales != 1) {
					continue;
				}
				
				//printf("\nEsquina %d encontrada\n", fila[esquina[0]]);
				for (otraesquina[0] = 0; otraesquina[0] < tamano; otraesquina[0]++) {
					if (otraesquina[0] == esquina[0]) {
						continue;
					}
					for (otraesquina[1] = 0; otraesquina[1] < tamano; otraesquina[1]++) {
						if (otraesquina[1] == esquina[1]) {
							continue;
						}
						if (fila[otraesquina[0]] != 2*c - col[otraesquina[1]]) {
							continue;
						}
						
						// Rellenamos la primera fila
						generadores[0] = fila[esquina[0]]; // la esquina
						i = 0; // el elemento de la fila
						for (k = 1; k < 2*n-1; k++) {
							if (i == esquina[0]) {
								i++;
							}
							if (i == otraesquina[0]) {
								i++;
							}
							generadores[k] = fila[i]; // elemento k de la primera fila
							i++;
						}
						i = 0;
						for (; k < numgen; k++) {
							if (i == esquina[1]) {
								i++;
							}
							if (i == otraesquina[1]) {
								i++;
							}
							generadores[k] = col[i]; // elemento k de la primera columna
							i++;
						}
						
						matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
						rellenrar_matriz(matriz_actual, c, generadores, n);
						
						if (es_matriz_prima(matriz_actual, n) == 0) continue;
						
						ordenar_matriz(matriz_actual, n);
						//mostrar_array(matriz_actual, 8*n);
						
						if (append_matriz(matrices_generadas[n-1].elementos, n)) {
							fprintf(salida[n-1], "%d,", c);
							escribir_array(salida[n-1], matriz_actual, 8*n); // matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
							matrices_generadas[n-1].elementos++;
						}
						//else putchar('-');
					}
				}
			}
		}
	}
	
	printf("%ld matrices generadas en el nivel %d\n", matrices_generadas[n-1].elementos, n);
		
	return matrices_generadas[n-1].elementos;
}*/

/*int gen_nuevas_anid(struct paresposibles *parposib, int c, int n) {
	// recibe una matriz anidada hasta el nivel n-1 y escribe el nivel n
	// es demasiado a fuerza bruta, mirar el python para mejorar :)
	// devuelve el numero de matrices generadas
	
	int numgen = 4*n-2;
	int r = parposib->cuantos;
	if (r < 4*n) {
		printf("No hay suficientes primos\n");
		return 0;
	}
	
	int tamano = 2*n+1;
	matrices_generadas[n-1].elementos = 0;
	buff_filas[n-1].tam = 2*n+1;
		
	int generadores[numgen]; // serán los índices de los generadores en primos_posibles
	int *matriz_actual = NULL;
	int aux, i, j, k;
	
	// Matrices 3x3
	if (n == 1) {
		int *mat_anid[1];
		mat_anid[0] = &c;
		int* fila;
		
		gen_filas(c, parposib, 3*c, n);
		printf("%ld filas generadas\n", buff_filas[n-1].elementos);
		//mostrar_filas();
		for (i = 0; i < buff_filas[n-1].elementos; i++) { // cada fila determina una matriz
			fila = get_from_mibuff(&buff_filas[n-1], i);
			
			// Hacemos grupos de 2 esquinas
			for (j = 0; j < 3; j++) { // el elemento del centro de la primera fila
				matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
				matriz_actual[1] = fila[j];
				if (j == 0) {
					matriz_actual[0] = fila[1];
					matriz_actual[2] = fila[2];
				}
				else if (j == 1) {
					matriz_actual[0] = fila[0];
					matriz_actual[2] = fila[2];
				} else {
					matriz_actual[0] = fila[0];
					matriz_actual[2] = fila[1];
				}
				aux = c - matriz_actual[0] + matriz_actual[2]; // el  elemento (2,1)
				if (aux <= 0 || 2*c-aux <= 0) continue; //printf("Negativo!!\n");
				else if (!esprimo[aux]) continue; //printf("%d no es primo!!\n", aux);
				else if (!esprimo[2*c-aux]) continue; //printf("%d no es primo!!\n", 2*c-aux);
				
				matriz_actual[3] = aux;
				matriz_actual[5] = 2*c - matriz_actual[2];
				
				if (matriz_actual[3] == matriz_actual[5]) continue; // si los elementos (1,2) y (1,3) son iguales
				
				matriz_actual[4] = 2*c - aux;
				matriz_actual[6] = 2*c - matriz_actual[1];
				matriz_actual[7] = 2*c - matriz_actual[0];
				
				ordenar_matriz(matriz_actual, n);
				
				if (append_matriz(matrices_generadas[n-1].elementos, n)) {
					printf("Matriz añadida\n");
					matrices_generadas[n-1].elementos++;
					mostrar_matriz(matriz_actual, mat_anid, n);
					putchar('\n');
				}
			}
		}
	}
	// Cuando la matriz no es 3x3
	else {
		//int primos_usados[tamano*tamano];
		int num_filas_posibles, num_fila, num_col, i, j, k, elem_iguales;
		int *fila, *col;
		int esquina[2], otraesquina[2];
		
		num_filas_posibles = gen_filas(c, parposib, (2*n+1)*c, n);
		//mostrar_filas();
		
		printf("%d filas posibles\n", num_filas_posibles);
		
		for (num_fila = 0; num_fila < num_filas_posibles-1; num_fila++) {
			//fila = get_fila(num_fila, n);
			fila = get_from_mibuff(&buff_filas[n-1], num_fila);
			for (num_col = num_fila+1; num_col < num_filas_posibles; num_col++) {
				//col = get_fila(num_col, n);
				col = get_from_mibuff(&buff_filas[n-1], num_col);
				elem_iguales = 0;
				for (i = 0; i < tamano; i++) {
					for (j = 0; j < tamano; j++) {
						if (fila[i] == col[j]) {
							esquina[0] = i;
							esquina[1] = j;
							elem_iguales++;
						}
					}
				}
				if (elem_iguales != 1) {
					continue;
				}
				
				//printf("\nEsquina %d encontrada\n", fila[esquina[0]]);
				for (otraesquina[0] = 0; otraesquina[0] < tamano; otraesquina[0]++) {
					if (otraesquina[0] == esquina[0]) {
						continue;
					}
					for (otraesquina[1] = 0; otraesquina[1] < tamano; otraesquina[1]++) {
						if (otraesquina[1] == esquina[1]) {
							continue;
						}
						if (fila[otraesquina[0]] != 2*c - col[otraesquina[1]]) {
							continue;
						}
						
						// Rellenamos la primera fila
						generadores[0] = fila[esquina[0]]; // la esquina
						i = 0; // el elemento de la fila
						for (k = 1; k < 2*n-1; k++) {
							if (i == esquina[0]) {
								i++;
							}
							if (i == otraesquina[0]) {
								i++;
							}
							generadores[k] = fila[i]; // elemento k de la primera fila
							i++;
						}
						i = 0;
						for (; k < numgen; k++) {
							if (i == esquina[1]) {
								i++;
							}
							if (i == otraesquina[1]) {
								i++;
							}
							generadores[k] = col[i]; // elemento k de la primera columna
							i++;
						}
						
						matriz_actual = get_from_mibuff(&matrices_generadas[n-1], matrices_generadas[n-1].elementos);
						rellenrar_matriz(matriz_actual, c, generadores, n);
						
						if (es_matriz_prima(matriz_actual, n) == 0) continue;
						
						ordenar_matriz(matriz_actual, n);
						//mostrar_array(matriz_actual, 8*n);
						
						if (append_matriz(matrices_generadas[n-1].elementos, n)) matrices_generadas[n-1].elementos++;
						//else putchar('-');
					}
				}
			}
		}
	}
	
	if (matrices_generadas[n-1].elementos == 0) {
		return 0;
	}
	
	//printf("%ld matrices generadas\n", matrices_generadas.elementos);
		
	return matrices_generadas[n-1].elementos;
}*/

void ensamblar_y_escribir(FILE **salida, int c, int n) {
	int j, indice_ensamb[n];
	for (j = 0; j < n; ++j) indice_ensamb[j] = 0;
	
	int *mat_anid[n+1];
	mat_anid[0] = &c;
	
	j = 0;
	while(1) {
		printf("indices de ensamblado = ");
		mostrar_array(indice_ensamb, n);
		
		mat_anid[j+1] = get_from_mibuff(&matrices_generadas[j], indice_ensamb[j]);
		
		if (no_repetidos(mat_anid, n)) {
			escribir_anidada(salida[j], mat_anid, j+1);
			++num_generadas[j+1];
		}
		
		if (j < n-1) indice_ensamb[++j] = 0;
		
		else if (++indice_ensamb[j] == matrices_generadas[j].elementos) do {
			if (j <= 0) return;
			indice_ensamb[j] = 0;
			} while (++indice_ensamb[--j] == matrices_generadas[j].elementos);
	}
}

/*int escribir_generadas(FILE * salida, int **mat_anid, int n) {
	int cont = 0;
	for (int i = primera[n-1]; i != -1; i = matriz_posterior[n-1][i]) {
		mat_anid[n] = get_from_mibuff(&matrices_generadas[n-1], i);
		escribir_anidada(salida, mat_anid, n);
		++cont;
		if (matrices_generadas[n-1].elementos < cont) printf("Estamos escribiendo mas matrices de las que hay!!\n");
	}
	return cont;
}*/

int avanzar_permutacion(int *perm, int pos, int tam) {
	signed int i, j;
	if (perm[pos] > 0) {
		perm[pos] = -perm[pos];
		//printf("perm[%d] = - perm[%d]= %d;\n", pos, pos, perm[pos]);
	} else {
		if (pos == tam-1) return 0;
		perm[pos] = -perm[pos]+1;
		//emp_de_nuevo:
		if (perm[pos] > tam) return 0; //no se puede avanzar mas en esa posición
		
		// comprobamos que no este cogida, y si lo está empezamos de nuevo
		for (i = 0; i < pos; i++) {
			if (perm[i] == perm[pos] || perm[i] == - perm[pos]) {
				//printf(".perm[pos] = perm[%d] = perm[i] = perm[%d]\n", pos, i);
				if (++perm[pos] > tam) return 0;
				i = -1;
			}
		}
	}
	pos++;
	
	// y rellenamos el resto de posiciones por orden
	i = 1;
	while (pos < tam) {
		for (j = 0; j < pos;) {
			if (perm[j] == i || perm[j] == -i) {
				//printf("perm[j] = perm[%d] == i == %d\n", j, i);
				i++;
				j = 0;
			} else {
				j++;
			}
		}
		//printf("Fijamos perm[pos] = perm[%d] = %d\n", pos, i);
		perm[pos] = i;
		i++;
		pos++;
	}
	return 1;
}

int avanzar_signo(int *signo, int tam) {
	for (int i = 0; i < tam; i++) {
		if (++signo[i] == 1) return 1;
		signo[i] = 0;
	}
	return 0;
}

struct mibuffer *gen_permutaciones(int n) {
	struct mibuffer *permutaciones;
	permutaciones = malloc(sizeof(struct mibuffer));
	permutaciones->tam = 2*n*(n+1); // = ((2*n+1)*(2*n+1)-1)/2, el número total de pares (el central lo quitamos)
	//printf("%d pares\n", permutaciones->tam);
	permutaciones->bloques_reservados = 0;
	permutaciones->elementos = 0;
	permutaciones->elemxbloque = ELEM_X_BLOQUE;
	//printf("Inicializamos struct mibuffer permutaciones\n");
	
	int *perm_actual, *nueva_perm;
	perm_actual = get_from_mibuff(permutaciones, permutaciones->elementos++);
	//printf("Construimos la perm identidad\n");
	for (int i = 0; i < permutaciones->tam; i++) perm_actual[i] = i+1; // empezamos con la identidad
	
	int pos = permutaciones->tam - 1;
	
	for (;;) {
		nueva_perm = get_from_mibuff(permutaciones, permutaciones->elementos);
		copiar_array(perm_actual, nueva_perm, permutaciones->tam);
		//printf("avanzar_permutacion(nueva_perm, %d, %d)\n", pos, permutaciones->tam);
		if (!avanzar_permutacion(nueva_perm, pos, permutaciones->tam)) {
			if (--pos == -1) return permutaciones;
		} else {
			perm_actual = nueva_perm;
			mostrar_array(perm_actual, permutaciones->tam);
			pos = permutaciones->tam - 1;
			permutaciones->elementos++;
		}
	}
}

struct mibuffer* leer_permutaciones(FILE *entrada_perm, int n) {
	struct mibuffer *permutaciones;
	permutaciones = malloc(sizeof(struct mibuffer));
	permutaciones->tam = ((2*n+1)*(2*n+1)-1)/2; // el número total de pares (el central lo quitamos)
	//printf("%d pares\n", permutaciones->tam);
	permutaciones->bloques_reservados = 0;
	permutaciones->elementos = 0;
	permutaciones->elemxbloque = ELEM_X_BLOQUE;
	//printf("Inicializamos struct mibuffer permutaciones\n");
	
	while (!leer_linea_csv(entrada_perm, get_from_mibuff(permutaciones, permutaciones->elementos), permutaciones->tam)) {
		mostrar_array(get_from_mibuff(permutaciones, permutaciones->elementos), permutaciones->tam);
		permutaciones->elementos++;
	}
	
	return permutaciones;
}

/*void old_permutar_reducidas(int *perm, int *signos, int *red, int *newred, int n) {
	int par = 0, c = red[0];
	int num_pares = 1+2*n*(n+1); // 1 + sum(4*k) = 1 + 4*n*(n+1)/2
	
	newred[0] = red[0];
	for (par = 0; par < num_pares-1; par++) {
		if (signos[par] == 0) newred[par+1] = red[perm[par]+1];
		else newred[par+1] = 2*c - red[perm[par]+1];
	}
}*/

void permutar_reducidas(int *perm, int *red, int *newred, int n) {
	int par = 0, c = red[0];
	int num_pares = 1+2*n*(n+1); // 1 + sum(4*k) = 1 + 4*n*(n+1)/2
	
	newred[0] = red[0];
	for (par = 0; par < num_pares-1; par++) {
		if (perm[par] > 0) newred[par+1] = red[perm[par]];
		else newred[par+1] = 2*c - red[-perm[par]];
	}
}

int perm_menor(int *perm1, int *perm2, int tam) {
	for (int i = 0; i < tam; i++) {
		if (abs(perm1[i]) < abs(perm2[i])) return 1;
		if (abs(perm1[i]) > abs(perm2[i])) return 0;
		if (perm1[i] < perm2[i]) return 0; // perm1[i] = -perm2[i]
	}
	return 0; // son iguales
}

int ya_en_cociente(int *perm, struct mibuffer *permuniv) {
	// No es lo mas fino, porque habría que encontrar cuales son los generadores
	int i, aux = 0, *perm_univ, resultado[permuniv->tam];
	for (long int num_perm = 0; num_perm < permuniv->elementos; num_perm++) {
		perm_univ = get_from_mibuff(permuniv, num_perm);
		//comp_arrays(perm, perm_univ, permuniv->tam);
		for (i = 0; i < permuniv->tam; i++) {
			if (perm[i] != perm_univ[i]) {
				aux = 1;
				break;
			}
		}
		if (aux == 1) return 0;
		componer_perm(perm, perm_univ, resultado, permuniv->tam);
		if (perm_menor(resultado, perm, permuniv->tam)) return 0;
	}
	return 1;
}

void gen_seccion(int *perm, struct mibuffer *subgrupo, struct mibuffer *seccion) {
	int i;
	for (i = 0; i < subgrupo->elementos; i++) {
		componer_perm(perm, get_from_mibuff(subgrupo, i), get_from_mibuff(seccion, i), subgrupo->tam);
		copiar_array(perm, get_from_mibuff(seccion, i), subgrupo->tam);
	}
	seccion->elementos = i;
}

struct mibuffer* gen_perm_univs(struct mibuffer *buffreducidas, FILE * salida_univ) {
	int tam = buffreducidas->tam;
	int numpares = tam-1;
	int n;
	for (n = 1; tam > 1+2*n*(n+1); n++) continue;
	
	struct mibuffer *permunivs;
	permunivs = malloc(sizeof(struct mibuffer));
	permunivs->tam = numpares; // el número total de pares (el central lo quitamos)
	permunivs->bloques_reservados = 0;
	permunivs->elementos = 0;
	permunivs->elemxbloque = ELEM_X_BLOQUE;
	
	int *reducida, newreducida[tam];
	int perm[numpares], *perm_univ;
	
	int esuniv;
	printf("Tamos redy\n");
	
	for (int i = 0; i < numpares; i++) perm[i] = i+1;
	
	int pos = numpares - 1;
	for (int num_perm = 0; ; num_perm++) {
		if (!avanzar_permutacion(perm, pos, numpares)) {
			if (--pos == -1) break;
			continue;
		} else {
			//mostrar_array(perm, tam1);
			pos = numpares - 1;
			//if (ya_en_cociente(perm, permunivs)) continue;
			num_perm++;
		}
		if (num_perm%10000 == 0) putchar('.');
		esuniv = 1;
		
		for (int cont = 0; cont < buffreducidas->elementos; cont++) {
			//if (cont%100 == 0 || cont >= 225000) putchar('.'); //printf("%ld < %ld\n", cont, buffreducidas.elementos);
			reducida = get_from_mibuff(buffreducidas, cont);
			permutar_reducidas(perm, reducida, newreducida, n);
			if (!es_matriz_reducida(newreducida, n)) {
				esuniv = 0;
				break;
			}
		}
		if (esuniv) {
			perm_univ = get_from_mibuff(permunivs, permunivs->elementos++);
			copiar_array(perm, perm_univ, numpares);
			escribir_array(salida_univ, perm_univ, permunivs->tam);
			mostrar_array(perm_univ, permunivs->tam);
		}
		//putchar('\n');
	}
	return permunivs;
}

struct sumas {
	int tam;
	int valor;
	int *indices;
};

struct permciclos {
	int *tam; // los tamaños de cada ciclo
	int **ciclos;
	int numciclos;
};

void perm_to_ciclos(int *perm, struct permciclos *ciclos, int tam) {
	int i, ppio = 0, sig, cop_perm[tam];
	for (i = 0; i < tam; i++) cop_perm[i] = 1;
	ciclos->numciclos = 0;	
	ciclos->tam[0] = 0;
	
	//printf("ciclo[0][0] = 1\n");
	ciclos->ciclos[0][0] = 1;
	cop_perm[0] = 0;
	ciclos->tam[ciclos->numciclos] = 1;
	ciclos->ciclos[0][1] = perm[0];
	//printf("ciclo[0][1] = perm[0] = %d\n", perm[0]);
	
	for (i = 0; i < tam; i++) {
		if ((sig = ciclos->ciclos[ciclos->numciclos][ciclos->tam[ciclos->numciclos]]) < 0) sig = -sig;
		sig = sig - 1;
		//printf("sig = %d\n", sig);
		
		if (sig == ppio) {
			//printf("Fin del ciclo\n");
			
			// si el primer elemento es negativo le cambiamos de signo
			ciclos->ciclos[ciclos->numciclos][0] = ciclos->ciclos[ciclos->numciclos][ciclos->tam[ciclos->numciclos]];
			//printf("ciclo[%d][0] = %d\n", ciclos->numciclos, ciclos->ciclos[ciclos->numciclos][0]);
			
			// si es un ciclo de mas de 1 elemento ó es de un elemento pero cambia de signo consideramos el ciclo como válido
			if (ciclos->tam[ciclos->numciclos] > 1 || ciclos->ciclos[ciclos->numciclos][0] < 0) ciclos->numciclos++;
			
			// buscamos el primer elemento del ciclo siguiente
			for (++ppio; ppio < tam; ppio++) if (cop_perm[ppio] == 1) break;
			
			if (ppio == tam) break;
			ciclos->ciclos[ciclos->numciclos][0] = ppio+1;
			//printf("ciclo[%d][0] = perm[sig] = %d\n", ciclos->numciclos, ppio+1);
			cop_perm[ppio] = 0;
			ciclos->tam[ciclos->numciclos] = 1;
			ciclos->ciclos[ciclos->numciclos][1] = perm[ppio];
			//printf("ciclo[%d][1] = perm[ppio] = %d\n", ciclos->numciclos, perm[ppio]);
		}
		else {
			cop_perm[sig] = 0;
			ciclos->tam[ciclos->numciclos]++;
			ciclos->ciclos[ciclos->numciclos][ciclos->tam[ciclos->numciclos]] = perm[sig];
			//printf("ciclo[%d][%d] = perm[sig] = %d\n", ciclos->numciclos, ciclos->tam[ciclos->numciclos], perm[sig]);
		}
	}
}

void mostrar_ciclos(struct permciclos *perciclada) {
	int i, k;
	printf("%d ciclos de tamaño ", perciclada->numciclos);
	mostrar_array(perciclada->tam, perciclada->numciclos);
	for (k = 0; k < perciclada->numciclos; k++) {
		putchar('(');
		for (i = 0; i < perciclada->tam[k]-1; i++) {
			printf("%d ", perciclada->ciclos[k][i]);
		}
		printf("%d)", perciclada->ciclos[k][i]);
	}
	putchar('\n');
}

void escribir_ciclos(FILE *salida, struct permciclos *perciclada, int tam) {
	int i, k;
	//fprintf(salida, "%d ciclos de tamaño ", perciclada->numciclos);
	//mostrar_array(perciclada->tam, perciclada->numciclos);
	for (k = 0; k < perciclada->numciclos; k++) {
		fprintf(salida, "(");
		for (i = 0; i < perciclada->tam[k]-1; i++) fprintf(salida, "%d ", perciclada->ciclos[k][i]);
		fprintf(salida, "%d)", perciclada->ciclos[k][i]);
	}
}

void reducir_matriz(int *matriz_anid[], int *reducida, int n) {
	int k, i, j = 0; // k el nivel de anidación, i la posición dentro del nivel
	
	reducida[j++] = matriz_anid[0][0];
	
	for (k = 1; k <= n; k++) {
		for (i = 0; i <= 2*k; i++) {
			reducida[j++] = matriz_anid[k][i];
		}
		for (i = 2*k+1; i < 6*k-2; i=i+2) {
			reducida[j++] = matriz_anid[k][i];
		}
	}
}

void desreducir_matriz(int *matriz_anid[], int *reducida, int n) {
	int k = 0, i = 0; // k el nivel de anidación, i la posición dentro del nivel
	int num_pares = 1+2*n*(n+1); // 1 + sum(4*k) = 1 + 4*n*(n+1)/2
	
	for (int j = 0; j < num_pares; j++) {
		matriz_anid[k][i] =	reducida[j];
		if (k == 0) {
			//central = matriz_anid[0][0];
		}
		else if (i == 0) {
			matriz_anid[k][8*k-1] = 2*matriz_anid[0][0] - matriz_anid[k][0];
			i++;
		}
		else if (i < 2*k) {
			matriz_anid[k][6*k-1+i] = 2*matriz_anid[0][0] - matriz_anid[k][i];
			i++;
		}
		else if (i == 2*k) {
			matriz_anid[k][6*k-1] = 2*matriz_anid[0][0] - matriz_anid[k][i];
			i++;
		}
		else if (i > 2*k) {
			matriz_anid[k][i+1] = 2*matriz_anid[0][0] - matriz_anid[k][i];
			i = i+2;
		}
		if (i >= 6*k-1) {
			if (++k > n) {
				return;
			}
			i = 0;
		}
	}
}

void desreducir_array(int *array_anid, int *reducida, int n) {
	int k = 0, i = 0; // k el nivel de anidación, i la posición dentro del nivel
	int num_pares = 1 + 2*n*(n+1); // 1 + sum(4*k) = 1 + 4*n*(n+1)/2
	int suelo = 0;
	
	for (int j = 0; j < num_pares; j++) {
		array_anid[suelo+i] = reducida[j];
		if (k == 0) {
			//central = array_anid[0][0];
		}
		else if (i == 0) {
			array_anid[suelo + 8*k-1] = 2*array_anid[0] - array_anid[suelo];
			i++;
		}
		else if (i < 2*k) {
			array_anid[suelo + 6*k-1+i] = 2*array_anid[0] - array_anid[suelo + i];
			i++;
		}
		else if (i == 2*k) {
			array_anid[suelo + 6*k-1] = 2*array_anid[0] - array_anid[suelo + i];
			i++;
		}
		else if (i > 2*k) {
			array_anid[suelo + i+1] = 2*array_anid[0] - array_anid[suelo + i];
			i = i+2;
		}
		if (i >= 6*k-1) {
			if (++k > n) {
				return;
			}
			i = 0;
			suelo = (2*k-1)*(2*k-1);
		}
	}
}

void restar_matrices(int **mat1, int **mat2, int **resultado, int n) {
	int i, k;
	resultado[0][0] = mat1[0][0] - mat2[0][0];
	for (k = 1; k <= n; k++) for (i = 0; i < 8*k; i++) resultado[k][i] = mat1[k][i] - mat2[k][i];
}

/*struct frecperm *ord_frecuencias(int **rep_perm, int cuantos, int tam) {
	int i, j;
	struct frecperm *ordenado, aux_elem;
	ordenado = malloc(sizeof(struct frecperm)*cuantos*tam);
	for (i = 0; i < cuantos*tam; i++) {
		ordenado[i].num_perm = i/tam;
		ordenado[i].num_signo = i%tam;
		ordenado[i].frec = rep_perm[ordenado[i].num_perm][ordenado[i].num_signo];
	}
	
	for (i = 0; i < cuantos - 1; i++) {
		for (j = 1; j < cuantos; j++) {
			if (ordenado[j].frec < ordenado[j-1].frec) {   // si el elemento anterior es mayor, hacemos el cambio
				aux_elem = ordenado[j];
				ordenado[j] = ordenado[j-1];
				ordenado[j-1] = aux_elem;
			}
		}
	}
	return ordenado;
}*/

int num_signo(int *signos, int tam) {
	int i, j, sumar, resultado = 0;
	for (i = 0; i < tam; i++) {
		if (signos == 0) continue;
		sumar = 1;
		for (j = 0; j < i; j++) sumar = sumar*2;
		resultado = resultado + sumar;
	}
	return resultado;
}

void num_to_signo(int num, int *signos, int tam) {
	int i, ind = 2;
	for (i = 0; i < tam; i++) {
		signos[i] = num %ind;
		ind = ind*2;
	}
}

int cual_permutacion(int *array1, int *array2, int *perm, int tam) {
	// es necesario que no haya elementos repetidos
	int i, j;
	for (i = 0; i < tam; i++) {
		for (j = 0; j < tam; j++) {
			if (array1[i] == array2[j]) {
				perm[i] = j+1;
				break;
			}
		}
		if (j == tam) return 1; // el elementos buscado no está en array2
	}
	return 0;
}
