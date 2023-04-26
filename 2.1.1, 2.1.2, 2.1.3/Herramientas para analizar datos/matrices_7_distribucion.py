# coding=utf-8
import csv

dismod3 = [0]*3
dismod5=[0]*5
dismod7=[0]*7

with open('matrices_7_primos.csv') as File:
	reader = csv.reader(File, delimiter=';')
	for row in reader:
		print(row)
		mod3 = int(row[24])%3
		mod5 = int(row[24])%5
		mod7 = int(row[24])%7
		dismod3[mod3] = dismod3[mod3]+1
		dismod5[mod5] = dismod5[mod5]+1
		dismod7[mod7] = dismod7[mod7]+1

print(dismod3)
print(dismod5)
print(dismod7)
