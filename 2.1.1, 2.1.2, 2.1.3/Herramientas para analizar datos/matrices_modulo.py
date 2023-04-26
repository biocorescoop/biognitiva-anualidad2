# coding=utf-8

import csv

principio = """\documentclass[11pt]{article}

\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\\textheight = 21cm
\\textwidth = 17cm
\oddsidemargin = -1cm
%\\topmargin = -2cm
\parindent = 0mm % Sangría=0mm

    \\title{\\textbf{Matrices mod 3}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}"""

final = """\\end{document}"""

with open('matrices_3_primos.csv') as File:
	with open('matrices_3_modulo.tex', 'w') as salida:
		reader = csv.reader(File, delimiter=';')
		salida.write(principio)
		k = 0
		for row in reader:
			salida.write("""\\begin{tabular}{|c|c|c|}\n\\hline\n""")
			salida.write(row[0] + '&' + row[1] + '&' + row[2] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[3] + '&' + row[4] + '&' + row[5] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[6] + '&' + row[7] + '&' + row[8] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			salida.write('$\\xrightarrow{mod 3}$\n')
			salida.write("""\\begin{tabular}{|c|c|c|}\n\\hline\n""")
			salida.write(str(int(row[0])%3) + '&' + str(int(row[1])%3) + '&' + str(int(row[2])%3) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[3])%3) + '&' + str(int(row[4])%3) + '&' + str(int(row[5])%3) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[6])%3) + '&' + str(int(row[7])%3) + '&' + str(int(row[8])%3) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\\\\\n')
			k=k+1
			if k>=2000:
				break
		salida.write(final)
		print(str(k) + ' matrices')

