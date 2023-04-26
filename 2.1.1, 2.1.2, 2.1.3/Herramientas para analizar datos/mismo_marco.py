#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv
import sys

numargs = len(sys.argv)


n = -1

print("numargs = %d\n", numargs)
i = 0
while i < numargs:
	print("argumento %d\n", i)
	#print(sys.argv[i] + "\n")
	if (sys.argv[i] == "-i"):
		fileinput = sys.argv[i+1]
		i += 2
		continue
	elif (sys.argv[i] == "-o"):
		fileoutput = sys.argv[i+1]
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

marcos = []
oldc = -1
count = 0

with open(fileinput) as File:
	reader = csv.reader(File, delimiter=',')
	k = 0
	for row in reader:
		c = int(row[0])
		if c != oldc:
			print(str(oldc) + " tiene " + str(count) + " marcos repetidos")
			marcos = []
			oldc = c
			count = 0
		
		if row[4*(n-1)+1:4*n] in marcos:
			count += 1
		else:
			marcos.append(row[4*(n-1)+1:4*n])
			
