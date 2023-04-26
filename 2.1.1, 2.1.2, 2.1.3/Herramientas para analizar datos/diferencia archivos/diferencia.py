#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv, sys

numargs = len(sys.argv)
		
if (numargs != 3):
	print("Faltan archivos de entrada\n")
	exit(0)


file1 = sys.argv[1]
file2 = sys.argv[2]

primos1 = []
primos2 = []

with open(file1) as File:
	reader = csv.reader(File, delimiter=',')
	for row in reader:
		primos1.append(int(row[0]))

with open(file2) as File:
	reader = csv.reader(File, delimiter=',')
	for row in reader:
		primos2.append(int(row[0]))

print("Primos del primer arvhivo que no estan en el segundo:")
print(list(filter(lambda x:x not in primos2, primos1)))
#print([x for x in primos1 if x not in primos2])

print("Primos del segundo arvhivo que no estan en el primer:")
print(list(filter(lambda x:x not in primos1, primos2)))

#print([x for x in primos2 if x not in primos1])
