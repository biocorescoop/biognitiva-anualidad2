#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv
import sys

principio = """\\documentclass[11pt]{article}

\\usepackage[spanish]{babel}
\\usepackage[utf8]{inputenc}

\\textheight = 21cm
\\textwidth = 17cm
\\oddsidemargin = -2cm
%\topmargin = -2cm
\\parindent = 0mm % Sangría=0mm

    \\title{\\textbf{Matrices Similares}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{4cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}"""

final = """\\end{document}"""

numargs = len(sys.argv)

fileinput = ""
fileoutput = ""
mode = ""
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
	elif (sys.argv[i] == "mod"):
		modbase = int(sys.argv[i+1])
		i += 2
		continue
	elif (sys.argv[i] == "-simetria"):
		mode = "simetria"
		i += 1
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
		reader = csv.reader(File, delimiter=',')
		salida.write(principio)
		k = 0
		for row in reader:
			if len(row) == 0:
				salida.write("\\\\\n\n")
				if k>=500:
					break
				continue
			
			c = int(row[0])
			
			if mode == "simetria":
				for i  in range(len(row)):
					row[i] = (int(row[i])- c)/6
			elif mode == "mod":
				for i  in range(len(row)):
					row[i] = (int(row[i])%modbase)
			elif mode == "":
				for i  in range(len(row)):
					row[i] = (int(row[i]))
			
			salida.write("""\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n""")
			salida.write(str(row[9]) + '&' + str(row[10]) + '&' + str(row[11]) + '&' + str(row[12]) + '&' + str(row[13]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(row[14]) + '&' + str(row[1]) + '&' + str(row[2]) + '&' + str(row[3]) + '&' + str(row[15]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(row[16]) + '&' + str(row[4]) + '&' + str(row[0]) + '&' + str(row[5]) + '&' + str(row[17]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(row[18]) + '&' + str(row[6]) + '&' + str(row[7]) + '&' + str(row[8]) + '&' + str(row[19]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(row[20]) + '&' + str(row[21]) + '&' + str(row[22]) + '&' + str(row[23]) + '&' + str(row[24]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			k=k+1
		salida.write(final)
		print(str(k) + ' matrices')

