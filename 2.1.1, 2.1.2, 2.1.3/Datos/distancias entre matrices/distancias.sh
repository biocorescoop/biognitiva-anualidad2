#!/bin/bash

echo "primeras matrices de cada tipo:"

for tipo in "Libre_de_c" "Linea_de_c" "Constante_c" #"0_en_arista_y_libre_de_c" "0_en_arista_y_linea_de_c" "0_en_esquina" "0_central"
do
	for i in {3,5,7,11,13,17,19,23} #,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113}
	do
		echo $tipo mod $i
        ./distancias_matrices -ireducida ./matrices_3x3_100k.csv -o distancias_res_${tipo}_${i}.csv -cmax 20000 -n 1 -p $i -tipo $tipo -restar
	done
    echo ""
done
