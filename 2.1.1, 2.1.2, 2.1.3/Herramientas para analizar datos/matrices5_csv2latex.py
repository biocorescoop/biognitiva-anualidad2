# coding=utf-8
import csv

principio = """\documentclass[11pt]{article}

\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}

\\textheight = 30cm
\\textwidth = 24cm
\oddsidemargin = -1cm
\\evensidemargin = -1cm
%\\topmargin = -2cm
\parindent = 0mm % Sangría=0mm
    \\title{\\textbf{Ejemplos matrices}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}"""

final = """\\end{document}"""

with open('matrices_5_primos.csv') as File:
	with open('matrices_5_primos.tex', 'w') as salida:
		reader = csv.reader(File, delimiter=';')
		salida.write(principio)
		k = 0
		for row in reader:
			salida.write("""\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n""")
			salida.write(row[0] + '&' + row[1] + '&' + row[2] + '&' + row[3] + '&' + row[4] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[5] + '&' + row[6] + '&' + row[7] + '&' + row[8] + '&' + row[9] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[10] + '&' + row[11] + '&' + row[12] + '&' + row[13] + '&' + row[14] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[15] + '&' + row[16] + '&' + row[17] + '&' + row[18] + '&' + row[19] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[20] + '&' + row[21] + '&' + row[22] + '&' + row[23] + '&' + row[24] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			k=k+1
			if k>=1000:
				break
		salida.write(final)
		print(str(k) + ' matrices')

