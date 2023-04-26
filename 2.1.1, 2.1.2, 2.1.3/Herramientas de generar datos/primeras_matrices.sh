#!/bin/bash

echo "primeras matrices de cada tipo:"

for tipo in "Libre_de_c" "Linea_de_c" "Constante_c" "0_en_arista_y_libre_de_c" "0_en_arista_y_linea_de_c" "0_en_esquina" "0_central"
do
	for i in {3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113}
	do
		echo $tipo mod $i : `./filtrar_matrices -ireducida 1000\ cada\ clase/matrices_3x3_100k.csv -p $i -tipo $tipo -cuantos 1`
	done
    echo ""
done
