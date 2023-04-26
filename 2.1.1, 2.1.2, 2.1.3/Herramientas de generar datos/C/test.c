
void test_get_from_mibuff(int tam) {
	struct mibuffer buffer;
	inicializar_mibuff(&buffer, tam, ELEM_X_BLOQUE);
	
	int *elemento, array[tam], i;
	
	array[0] = 0;
	for (i = 1; i < tam; i++) array[i] = array[i-1] + 1;
	for (i = 1; i < tam; i = i+2) array[i] = -array[i];
	mostrar_array(array, tam);
	
	printf("Pedir el primer elemento y escribir el array\n");
	elemento = get_from_mibuff(&buffer, 0);
	copiar_array(array, elemento, tam);
	mostrar_array(elemento, tam);
	
	printf("Pedir el último elemento del bloque\n");
	elemento = get_from_mibuff(&buffer, buffer.elemxbloque-1);
	copiar_array(array, elemento, tam);
	mostrar_array(elemento, tam);
	
	printf("Pedir el primer elemento del bloque 2\n");
	elemento = get_from_mibuff(&buffer, buffer.elemxbloque);
	copiar_array(array, elemento, tam);
	mostrar_array(elemento, tam);
	
	printf("Pedir el primer elemento del bloque 10\n");
	elemento = get_from_mibuff(&buffer, 9*buffer.elemxbloque);
	copiar_array(array, elemento, tam);
	mostrar_array(elemento, tam);
	
	printf("Liberar el espacio reservado\n");
	liberar_mibuffer(&buffer);
	//free(&buffer);
}

int test_mibuff_hasta_que_pete(int tam) {
	struct mibuffer buffer;
	inicializar_mibuff(&buffer, tam, ELEM_X_BLOQUE);
	
	for (long int i = 0; ; i++) {
		printf("%ld: ", i);
		printf("buffer[%ld] = %p\n", i, get_from_mibuff(&buffer, i));
	}
}

int test_append(int tam, int num_pruebas) {
	// si num_pruebas = -1, lo hacemos hasta que pete
	struct mibuffer buffer;
	inicializar_mibuff(&buffer, tam, ELEM_X_BLOQUE);
	
	int *elemento;
	
	for (int i = 0; (i < num_pruebas) || (num_pruebas == -1); i++) {
		
	}
}

void test_signos() {
	struct mibuffer buffsignos;
	inicializar_mibuff(&buffsignos, tam, ELEM_X_BLOQUE);
	gen_signos_pa_filas(&buffsignos);
	for (int i = 0; i < buffsignos->elementos; i++) mostrar_array(get_from_mibuff(buffsignos, i), buffsignos->tam);
}
