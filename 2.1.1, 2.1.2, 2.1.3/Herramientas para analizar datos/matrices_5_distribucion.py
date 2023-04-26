# coding=utf-8
import csv

dismod3 = [0]*3
dismod5=[0]*5


with open('matrices_5_primos.csv') as File:
	reader = csv.reader(File, delimiter=';')
	for row in reader:
		mod3 = int(row[12])%3
		mod5 = int(row[12])%5
		dismod3[mod3] = dismod3[mod3]+1
		dismod5[mod5] = dismod5[mod5]+1

print(dismod3)
print(dismod5)
