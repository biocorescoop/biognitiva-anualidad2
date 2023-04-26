#!/bin/bash

step = 500
max=10000
out="time_tripletas_${max}.csv"

echo "max, t real, t user, t sys" > out

for (( num=step; num<=max; num=num+step ))
do
	time --append -f "${num},%E real,%U user,%S sys" -o ${out} ./gen_matrices_con_tripletas -max ${num}
done
