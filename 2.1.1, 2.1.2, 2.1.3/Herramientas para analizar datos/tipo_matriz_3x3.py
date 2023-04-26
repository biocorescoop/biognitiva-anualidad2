#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv, sys

numargs = len(sys.argv)

fileinput = ""
n = -1

print("numargs = %d\n", numargs)
i = 0
while i < numargs:
	print("argumento", i, "\n")
	#print(sys.argv[i] + "\n")
	if (sys.argv[i] == "-i"):
		fileinput = sys.argv[i+1]
		i += 2
		continue
	elif (sys.argv[i] == "-n"):
		n = int(sys.argv[i+1])
		i += 2
		continue
	else:
		i += 1

if (fileinput == ""):
	print("No hay archivo de entrada\n")
	exit(0)


with open(fileinput) as File:
	reader = csv.reader(File, delimiter=',')
	k = 0
	tipo1 = 0
	tipo2 = 0
	otras = 0
	for row in reader:
		c = int(row[0])
		for i  in range(len(row)):
			row[i] = int(row[i])
		
		if 2*c-row[2] < row[1] < row[3] < 2*c-row[4]:
			tipo1 += 1
		elif 2*c-row[2] < row[1] < 2*c-row[4] < row[3]:
			tipo2 += 1
		else:
			otras += 1
			#print(row)
		k=k+1
		if k%50000 == 0:
			print()
			print(str(tipo1) + " matrices de tipo 1 (" + str(int(float(tipo1)/k*1000)) + "/1000)\n")
			print(str(tipo2) + " matrices de tipo 2 (" + str(int(float(tipo2)/k*1000)) + "/1000)\n")
			#print(str(otras) + " matrices de otro tipo (" + str(int(float(otras)/k*100)) + "%)\n")
	print(str(k) + ' matrices')

