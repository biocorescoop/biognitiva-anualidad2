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
    \\title{\\textbf{Matrices $7\\times 7$ módulo}}
    \\author{}
    \\date{}
    
    \\addtolength{\\topmargin}{-3cm}
    \\addtolength{\\textheight}{3cm}
\\begin{document}

\\maketitle
\\thispagestyle{empty}"""

final = """\\end{document}"""

with open('matrices_7_primos.csv') as File:
	with open('matrices_7_modulo.tex', 'w') as salida:
		reader = csv.reader(File, delimiter=';')
		salida.write(principio)
		k = 0
		for row in reader:
			salida.write("""\\begin{tabular}{|c|c|c|c|c|c|c|}\n\\hline\n""")
			salida.write(row[0] + '&' + row[1] + '&' + row[2] + '&' + row[3] + '&' + row[4] + '&' + row[5] + '&' + row[6] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[7] + '&' + row[8] + '&' + row[9] + '&' + row[10] + '&' + row[11] + '&' + row[12] + '&' + row[13] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[14] + '&' + row[15] + '&' + row[16] + '&' + row[17] + '&' + row[18] + '&' + row[19] + '&' + row[20] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[21] + '&' + row[22] + '&' + row[23] + '&' + row[24] + '&' + row[25] + '&' + row[26] + '&' + row[27] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[28] + '&' + row[29] + '&' + row[30] + '&' + row[31] + '&' + row[32] + '&' + row[33] + '&' + row[34] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[35] + '&' + row[36] + '&' + row[37] + '&' + row[38] + '&' + row[39] + '&' + row[40] + '&' + row[41] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(row[42] + '&' + row[43] + '&' + row[44] + '&' + row[45] + '&' + row[46] + '&' + row[47] + '&' + row[48] + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\n')
			salida.write('$\\xrightarrow{mod 7}$\n')
			salida.write("""\\begin{tabular}{|c|c|c|c|c|c|c|}\n\\hline\n""")
			salida.write(str(int(row[0])%7) + '&' + str(int(row[1])%7) + '&' + str(int(row[2])%7) + '&' + str(int(row[3])%7) + '&' + str(int(row[4])%7) + '&' + str(int(row[5])%7) + '&' + str(int(row[6])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[7])%7) + '&' + str(int(row[8])%7) + '&' + str(int(row[9])%7) + '&' + str(int(row[10])%7) + '&' + str(int(row[11])%7) + '&' + str(int(row[12])%7) + '&' + str(int(row[13])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[14])%7) + '&' + str(int(row[15])%7) + '&' + str(int(row[16])%7) + '&' + str(int(row[17])%7) + '&' + str(int(row[18])%7) + '&' + str(int(row[19])%7) + '&' + str(int(row[20])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[21])%7) + '&' + str(int(row[22])%7) + '&' + str(int(row[23])%7) + '&' + str(int(row[24])%7) + '&' + str(int(row[25])%7) + '&' + str(int(row[26])%7) + '&' + str(int(row[27])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[28])%7) + '&' + str(int(row[29])%7) + '&' + str(int(row[30])%7) + '&' + str(int(row[31])%7) + '&' + str(int(row[32])%7) + '&' + str(int(row[33])%7) + '&' + str(int(row[34])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[35])%7) + '&' + str(int(row[36])%7) + '&' + str(int(row[37])%7) + '&' + str(int(row[38])%7) + '&' + str(int(row[39])%7) + '&' + str(int(row[40])%7) + '&' + str(int(row[41])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write(str(int(row[42])%7) + '&' + str(int(row[43])%7) + '&' + str(int(row[44])%7) + '&' + str(int(row[45])%7) + '&' + str(int(row[46])%7) + '&' + str(int(row[47])%7) + '&' + str(int(row[48])%7) + '\\\\\n')
			salida.write('\\hline\n')
			salida.write('\\end{tabular}\\\\\n')
			k=k+1
			if k>=500:
				break
		salida.write(final)
		print(str(k) + ' matrices')
