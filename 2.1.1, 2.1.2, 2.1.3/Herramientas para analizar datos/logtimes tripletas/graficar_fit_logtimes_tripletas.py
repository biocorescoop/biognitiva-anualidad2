#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import numpy
import math
#import sys
import matplotlib.pyplot as plt
import scipy.optimize


fileinput = "logtimes_3x3_tripletas_0-200000.csv"
#n = -1
ds = []
tripletas = []
matrices = []
tiempo_hasta_d = []
tiempo_medio_por_matriz = []
num_matrices = 0

with open(fileinput) as File:
	#with open(fileoutput, 'w') as salida:
	reader = csv.reader(File, delimiter=',')
	for row in reader:
		if row[3] == "matrices" and row[2] != -1:
			ds.append(int(row[1]))
			matrices.append(int(row[2]))
			num_matrices += matrices[len(matrices)-1]
			tiempo_hasta_d.append(int(row[0]))
			if num_matrices > 0:
				tiempo_medio_por_matriz.append(int(row[0])/num_matrices)
			else:
				tiempo_medio_por_matriz.append(0)


xdata=ds#xdata = num_cen
ydata=tiempo_hasta_d

def func(x,a, b, c):
	x = numpy.float64(x)
	#return a * x**b + c
	return a * numpy.log(x*b + c)

plt.plot(xdata, ydata, '.') #, label='data')
popt, pcov = scipy.optimize.curve_fit(func,  xdata, ydata, p0=[1, 1, 0])
plt.plot(xdata, func(xdata, *popt), 'r-',         label='fit:' )
#plt.yscale("log")
#plt.xscale("log")#plt.xlim(0, 40000)
#plt.ylim(0, 1e6)plt.legend()
plt.show()

print(popt)
from sklearn.metrics import r2_score
y_pred = func(xdata, *popt)
R2=r2_score(ydata, y_pred)
print(popt, R2)

#popt te da los parámetros del ajuste
#pcov es la matriz de covarianza. la incertidumbre de cada parámetro se obtiene elevando#el correspondiente elemeto de la diagonal de pcov al cuadrado
#r2_score da R^2. Su`pongo q con sklearn se pueden obtener otros parametros estadisticos tambien
