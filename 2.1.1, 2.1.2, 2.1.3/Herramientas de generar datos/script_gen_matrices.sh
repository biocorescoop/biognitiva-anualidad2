#!/bin/bash

n=1
cmax=50000

for i in {1..3}
do
	for j in {1..3}
	do
		for k in {1..3}
		do 
			echo "n = $n, cmax = $cmax, paral = $i,$j,$k"
			./gen_marcos_hilos -n ${n} -cmax ${cmax} -hilos ${i},${j},${k} --logtimes
			echo ""
		done
	done
done
