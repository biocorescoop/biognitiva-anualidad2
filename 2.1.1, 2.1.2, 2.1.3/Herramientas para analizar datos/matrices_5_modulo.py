# coding=utf-8
import csv

principio = """\documentclass[11pt]{article}

\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\\textheight = 24cm
\\textwidth = 18cm
\oddsidemargin = -1cm
\\evensidemargin = -1cm
%\\topmargin = -2cm
\parindent = 0mm % Sangría=0mm
    \\title{\\textbf{Matrices $5\times 5$ módulo}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}"""

final = """\\end{document}"""

with open('matrices_5_primos.csv') as File:
	with open('matrices_5_modulo.tex', 'w') as salida:
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
			salida.write('$\\xrightarrow{mod 5}$\n')
			salida.write("""\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n""")
			salida.write(str(int(row[0])%5) + '&' + str(int(row[1])%5) + '&' + str(int(row[2])%5) + '&' + str(int(row[3])%5) + '&' + str(int(row[4])%5) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[5])%5) + '&' + str(int(row[6])%5) + '&' + str(int(row[7])%5) + '&' + str(int(row[8])%5) + '&' + str(int(row[9])%5) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[10])%5) + '&' + str(int(row[11])%5) + '&' + str(int(row[12])%5) + '&' + str(int(row[13])%5) + '&' + str(int(row[14])%5) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[15])%5) + '&' + str(int(row[16])%5) + '&' + str(int(row[17])%5) + '&' + str(int(row[18])%5) + '&' + str(int(row[19])%5) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[20])%5) + '&' + str(int(row[21])%5) + '&' + str(int(row[22])%5) + '&' + str(int(row[23])%5) + '&' + str(int(row[24])%5) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			salida.write('$\\xrightarrow{mod '+ row[12] + ' }\n$')
			salida.write("""\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n""")
			salida.write(str(int(row[0])%int(row[12])) + '&' + str(int(row[1])%int(row[12])) + '&' + str(int(row[2])%int(row[12])) + '&' + str(int(row[3])%int(row[12])) + '&' + str(int(row[4])%int(row[12])) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[5])%int(row[12])) + '&' + str(int(row[6])%int(row[12])) + '&' + str(int(row[7])%int(row[12])) + '&' + str(int(row[8])%int(row[12])) + '&' + str(int(row[9])%int(row[12])) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[10])%int(row[12])) + '&' + str(int(row[11])%int(row[12])) + '&' + str(int(row[12])%int(row[12])) + '&' + str(int(row[13])%int(row[12])) + '&' + str(int(row[14])%int(row[12])) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[15])%int(row[12])) + '&' + str(int(row[16])%int(row[12])) + '&' + str(int(row[17])%int(row[12])) + '&' + str(int(row[18])%int(row[12])) + '&' + str(int(row[19])%int(row[12])) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[20])%int(row[12])) + '&' + str(int(row[21])%int(row[12])) + '&' + str(int(row[22])%int(row[12])) + '&' + str(int(row[23])%int(row[12])) + '&' + str(int(row[24])%int(row[12])) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\\\\\n')
			k=k+1
			if k>=500:
				break
		salida.write(final)
		print(str(k) + ' matrices')

