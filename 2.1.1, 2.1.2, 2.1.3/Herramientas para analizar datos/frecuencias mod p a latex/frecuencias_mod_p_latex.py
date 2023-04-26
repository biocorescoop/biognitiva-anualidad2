# -*- coding: utf-8 -*-

import csv

principio = """\\documentclass[11pt]{article}

\\usepackage[spanish]{babel}
\\usepackage[utf8]{inputenc}
%\usepackage{multicol}

\\textheight = 21cm
\\textwidth = 17cm
\\oddsidemargin = -1cm
%\\topmargin = -2cm
\\parindent = 0mm % Sangría=0mm

    \\title{\\textbf{Distribucion en las matrices mod p}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}

"""

final = """
\\end{document}"""

modulos = [19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

with open('frec_marcos_3x3_mod_p.tex', 'w') as salida:
	salida.write(principio)
	for p in modulos:
		with open('frec_marcos_3x3_mod_' + str(p) + '.csv') as File:
			reader = csv.reader(File, delimiter=',')
			ordenadas = []
			k = 0
			for row in reader:
				if len(ordenadas) == 0:
					ordenadas.append(row)
				else:
					if len(row) <= 1:
						continue
					
					for i in range(len(ordenadas)):
						if int(row[len(row)-1]) > int(ordenadas[i][len(row)-1]):
							ordenadas.insert(i, row)
							break
						elif i == len(ordenadas)-1:
							ordenadas.append(row)
				
			salida.write('\\section{matrices mod ' + str(p) + '}\n')
			for row in ordenadas:
				salida.write("""\\begin{tabular}{c}\n\\begin{tabular}{|c|c|c|}\n\\hline\n""")
				salida.write(row[1] + '&' + row[2] + '&' + row[3] + '\\\\\n')
				salida.write('\\hline\n')
				salida.write(row[4] + '&' + row[0] + '&' + row[5] + '\\\\\n')
				salida.write('\\hline\n')
				salida.write(row[6] + '&' + row[7] + '&' + row[8] + '\\\\\n')
				salida.write('\\hline\n')
				salida.write('\\end{tabular}\\\\\n')
				salida.write(row[len(row)-1] + '\\\\\n\\end{tabular}\n')
				
	salida.write(final)
