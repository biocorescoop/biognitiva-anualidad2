#!/usr/bin/python 
# -*- coding: utf-8 -*-

import csv
import sys

principio = """\\documentclass[11pt]{article}

\\usepackage[spanish]{babel}
\\usepackage[utf8]{inputenc}

\\textheight = 21cm
\\textwidth = 17cm
\\oddsidemargin = -1cm
%\topmargin = -2cm
\\parindent = 0mm % Sangría=0mm

    \\title{\\textbf{Ejemplos matrices}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
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
			c = int(row[0])
			
			if mode == "simetria" or mode == "":
				for i  in range(len(row)):
					row[i] = (int(row[i])- c)/6
			if mode == "mod":
				for i  in range(len(row)):
					row[i] = (int(row[i])%modbase)
			
			salida.write("""\\begin{tabular}{|c|c|c|}\n\\hline\n""")
			salida.write(str(row[1]) + '&' + str(row[2]) + '&' + str(row[3]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(row[4]) + '&' + str(row[0]) + '&' + str(-row[4]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(-row[3]) + '&' + str(-row[2]) + '&' + str(-row[1]) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			k=k+1
			if k>=500:
				break
		salida.write(final)
		print(str(k) + ' matrices')

