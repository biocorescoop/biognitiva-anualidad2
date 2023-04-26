#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv, sys

numargs = len(sys.argv)
#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv, sys

numargs = len(sys.argv)

fileinput = ""
fileoutput = ""
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

if (fileoutput == ""):
	fileoutput = fileinput + ".tex"

with open(fileinput) as File:
	with open(fileoutput, 'w') as salida:
		eliminadas = 0
		reader = csv.reader(File, delimiter=',')
		writer = csv.writer(salida, delimiter=',')
		for row in reader:
			c = int(row[0])
			if 2*int(row[0])-int(row[3]) == int(row[4]):
				eliminadas += 1
				continue
			writer.writerow(row)
		print("Eliminadas: " + str(eliminadas))
				


fileinput = ""#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv, sys

numargs = len(sys.argv)

fileinput = ""
fileoutput = ""
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

if (fileoutput == ""):
	fileoutput = fileinput + ".tex"

with open(fileinput) as File:
	with open(fileoutput, 'w') as salida:
		eliminadas = 0
		reader = csv.reader(File, delimiter=',')
		writer = csv.writer(salida, delimiter=',')
		for row in reader:
			c = int(row[0])
			if 2*int(row[0])-int(row[3]) == int(row[4]):
				eliminadas += 1
				continue
			writer.writerow(row)
		print("Eliminadas: " + str(eliminadas))
				


fileoutput = ""
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

if (fileoutput == ""):
	fileoutput = fileinput + ".tex"

with open(fileinput) as File:
	with open(fileoutput, 'w') as salida:
		eliminadas = 0
		reader = csv.reader(File, delimiter=',')
		writer = csv.writer(salida, delimiter=',')
		for row in reader:
			c = int(row[0])
			if 2*int(row[0])-int(row[3]) == int(row[4]):
				eliminadas += 1
				continue
			writer.writerow(row)
		print("Eliminadas: " + str(eliminadas))
				

