#ifndef _LIBMATANID
#define _LIBMATANID

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

#define MAX_DIGITOS_PRIMOS 10
#define NUM_BLOQUES 100000
#define MAT_X_BLOQUE 1024
#define ELEM_X_BLOQUE 1024

#define CUANDO_SUBDIV 1000

#define bloque_actual(mibuff, num) (num/mibuff->elemxbloque)
#define elem_actual(mibuff, num) (num%mibuff->elemxbloque)

#define get_fila(num, n) get_from_mibuff(&buff_filas, num)

#define liberar_mibuffer(mibuff) ({for (int ifree = 0; ifree < (mibuff)->bloques_reservados; ++ifree) free((mibuff)->buff[ifree]);})

#define copiar_array(entrada, salida, elementos) ({for (int karr = 0; karr < elementos; karr++) (salida)[karr] = (entrada)[karr];})

#define es_matriz_menor(matriz1, matriz2, n) es_array_menor(matriz1, matriz2, 8*n)
#define es_matriz_mayor(matriz1, matriz2, n) es_array_mayor(matriz1, matriz2, 8*n)
#define es_matriz_igual(matriz1, matriz2, n) es_array_igual(matriz1, matriz2, 8*n)

#define inicializar_mibuff(mibuff, tamano, elemporbloque) ({\
	(mibuff)->tam = tamano;\
	(mibuff)->elemxbloque = elemporbloque;\
	(mibuff)->elementos = 0;\
	(mibuff)->bloques_reservados = 0;})

// Actúa por la derecha
#define componer_perm(perm1, perm2, rescomp, tamcompperm) for (int icomp = 0; icomp < tamcompperm; icomp++) rescomp[icomp] = perm1[perm2[icomp]-1]

#define valor_mod_p(variable, valor, p) ({\
	variable = valor;\
	if (variable < 0) variable = (variable - (variable/p - 1)*p) % p;\
	else variable = variable % p;})

struct frecperm {
	int num_perm;
	int* perm;
	int tam;
	long int frec;
};

struct mibuffer {
	int* buff[NUM_BLOQUES];
	int tam;
	int elemxbloque;
	int bloques_reservados;
	long int elementos;
};

struct mibufferptr {
	void** buff[NUM_BLOQUES];
	int elemxbloque;
	int bloques_reservados;
	long int elementos;
};

struct hitos_busqueda {
	int hitos[10];
	struct hitos_busqueda *subhitos;
	int dist;
};

struct buffthread {
	int n;
	int c;
	struct paresposibles *parposib;
	struct mibuffer buff_filas;
	struct mibuffer buffsignos;
	struct mibuffer matrices_generadas;
	struct mibuffer matriz_anterior;
	struct mibuffer matriz_posterior;
	struct hitos_busqueda hitos;
	int primera, ultima;
	FILE *salida;
};

struct bufffrecperm {
	struct frecperm* buff[NUM_BLOQUES];
	int tam;
	int elemxbloque;
	int bloques_reservados;
	long int elementos;
};

struct paresposibles {
	int *posibles;
	int *usados;
	int cuantos_total; // contando los usados
	int cuantos;
	int cuantos_usados;
	int c;
};

/*struct busqueda_indice {
	int nivel;
	int rango;
	int primer;
	int primer_primo;
	int primera_matriz;
	int cuantos;
	struct busqueda_indice *subbusqueda;
};*/

/*struct permut {
	int *ciclo;
	int long_ciclo;
	int *libres; // van por pares
	int cont_libres;
	struct permut *perm_sig;
	int cont_perm_sig;
	int primer;
}*/

inline void reservar_from_mibuff(struct mibuffer *mibuff, long int num) __attribute__((always_inline));

inline void reservar_from_mibuffptr(struct mibufferptr *mibuff, long int num) __attribute__((always_inline));

inline int* get_from_mibuff (struct mibuffer *mibuff, long int num) __attribute__((always_inline));

inline void* get_from_mibuffptr(struct mibufferptr *mibuff, long int num) __attribute__((always_inline));

inline void** get_ptr_from_mibuffptr(struct mibufferptr *mibuff, long int num) __attribute__((always_inline));

inline void colocar_despues (struct buffthread *buff_hilo, int num_actual, int i, int n) __attribute__((always_inline));

inline void colocar_antes (struct buffthread *buff_hilo, int num_actual, int i, int n) __attribute__((always_inline));

void gen_eratostenes(char *eratostenes, int cmax);

int cuantos_primos(int elementos);

void old_gen_primos_posibles (int c, int numeros_posibles[]);

void gen_primos_posibles (struct paresposibles *parposib);

void gen_primos_usados(int *mat_anid[], int n, int primos_usados[]);

int old_elim_primos_usados(int *primos_posibles, int *primos_usados, int n);

void elim_primos_usados(int *mat_anid[], int n, struct paresposibles *parposib);

int terminar_linea(FILE *entrada);

int leer_anidada(FILE *entrada, int *matriz_anid[], int n);

int escribir_anidada(FILE *salida, int **matriz_anid, int n);

int escribir_array(FILE *salida, int *array, int elementos);

long int exponencial(int base, int exponente);

void rellenrar_matriz(int matriz [], int c, int generadores[], int n);

int ordenar_burbuja(int* array, int elementos);

int es_array_menor(int *matriz1, int *matriz2, int n);

int es_array_igual(int *matriz1, int *matriz2, int n);

int ordenar_ind_matrices(int* ind_matrices[], int num_matrices, int n);

//void copiar_array(int* entrada, int* salida, int pos, int elementos);

int comp_arrays(int* array1, int* array2, int elementos);

int es_matriz_prima(int matriz[], int n);

int esquinas_ordenadas(int matriz[], int n);

int es_fila_ordenada(int matriz[], int n);

int es_col_ordenada(int matriz[], int n);

void mostrar_fila(int fila, int *matriz, int *mat_anid[], int n, char *linea);

void mostrar_matriz(int *matriz, int *mat_anid[], int n);

void mostrar_array(int *array, int elementos);

void mostrar_primos_posibles(int *primos_posibles);

void mostrar_primos_usados(int *primos_usados, int n);

//int* get_fila(int num_fila, int n);

//void test_get_fila(int num_filas_posibles);

int avanzar_indices(int *indices, int tope, int tam);

int avanzar_signos(int *signos, int tam);

int gen_filas_posibles(int c, int *primos_posibles, int n);

void mostrar_ind_matrices(int **mat_anid, int num_matrices, int n);

inline void simetria_vertical(int *matriz, int n) __attribute__((always_inline));

inline void simetria_horizontal(int *matriz, int n) __attribute__((always_inline));

inline void simetria_diagonal(int *matriz, int n) __attribute__((always_inline));

inline void ordenar_filas(int *matriz, int n) __attribute__((always_inline));

inline void ordenar_columnas(int *matriz, int n) __attribute__((always_inline));

inline void ordenar_matriz(int *matriz, int n) __attribute__((always_inline));

void inicializar_filas();

int gen_filas(int c, struct paresposibles *parposib, int valor, int n);

int append_matriz(int num_actual, struct buffthread *buff_hilo);

int* get_matriz_generada(int **matrices_generadas, int num_matriz, int n);

int gen_nuevas_anid(struct paresposibles *parposib, int c, int n);

int escribir_generadas(FILE * salida, int **mat_anid, int n);

int avanzar_permutacion(int *perm, int pos, int tam);

struct mibuffer *gen_permutaciones(int n);

void permutar_matriz(int *perm, int *signos, int **mat_anid, int **new_anid, int n);



#include "matanid.c"

//#include "test.c"
#endif
