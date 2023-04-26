package main

import (
	"fmt"
	"os"
	//"io"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
)

func main() {
	//var err error
	p := 0
	pmax := 0
	n := 1
	cmin := 59
	cmax := 0
	nombre_otipos := "matrices_noprimas"
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-pmax" :
				pmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-otipos" :
				nombre_otipos = os.Args[i+1]
				i++
			case "-cmin" :
				cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmax" :
				cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	fmt.Println("p = " + strconv.Itoa(p) + ", n = " + strconv.Itoa(n))
	
	if pmax % 2 == 1 { pmax++ }
	esprimo := make([]bool, pmax)
	matanid.Gen_esprimo(esprimo, pmax/2)
	primos := matanid.Lista_primos(esprimo)
	
	frecuencias := make([][]int, len(primos))
	salida_tipos := make([][]*csv.Writer, len(primos))
	num_tipo := make([]int, len(primos))
	
	for i, p := range(primos) {
		frecuencias[i] = make([]int, len(matanid.Tipos))
		
		salida_tipos[i] = make([]*csv.Writer, len(matanid.Tipos))
		for nom_tipo, num_tipo := range matanid.Tipos {
			f_salida, err := os.Create("no-primos/" + nom_tipo + "/" + nombre_otipos + "_mod_" + strconv.Itoa(p) + ".csv")
			if err != nil { log.Fatal(err) }
			defer f_salida.Close()
			
			salida_tipos[i][num_tipo] = csv.NewWriter(f_salida)
			if err != nil { log.Fatal(err) }
			
			fmt.Println("archivo de tipo ", num_tipo, " : ", "no-primos/" + nom_tipo + "/" + nombre_otipos + "_mod_" + strconv.Itoa(p) + ".csv")
		}
	}
	
	matriz := make([]int, 9)
	var matriz_modp []int // := make([]int, 9)
	
	dist := 6
	A := []int{ 0, dist, 0, -dist, -2*dist, 2*dist, dist, 0, -dist }
	B := []int{ 0, 0, dist, -dist, -dist, dist, dist, -dist, 0 }
	
	for c := cmin; c < cmax; c += 2 {
		if c % 3 == 0 { continue }
		fmt.Println("c = ", c)
		
		C := []int{ c, c, c, c, c, c, c, c, c}
		
		pasar := false
		for a := 1; a <= c/(2*dist); a++ {
			for b := -c/dist + 2*a; b < c/dist - 2*a; b++ {
				if b == 0 || b == a || b == -a { continue }
				for i, _ := range(matriz) {
					matriz[i] = C[i] + a*A[i] + b*B[i]
					if (matriz[i] % 2)*(matriz[i] % 3) == 0 {
						pasar = true
						break
					}
					//matriz_modp[i] = matriz[i] % p
				}
				if pasar {
					pasar = false
					continue
				}
				
				//fmt.Println(matriz, " = ", C, " + ", a, A, " + ", b, B, "\n")
				
				for i, p := range(primos) {
					matriz_modp = matanid.Array_modp(matriz, p)
					num_tipo[i] = matanid.Tipo_de_matriz(matriz_modp)
					
					if num_tipo[i] == -1 {
						pasar = true
						break
					}
				}
				if pasar {
					pasar = false
					continue
				}
				
				for i, _ := range(primos) {
					salida_tipos[i][num_tipo[i]].Write(matanid.Array_to_strings(matriz))
					frecuencias[i][num_tipo[i]]++
					
					if frecuencias[i][num_tipo[i]] % 100000 == 0 { salida_tipos[i][num_tipo[i]].Flush() }
				}
				
				
			}
		}
	}
	
	for _, salidas_p := range(salida_tipos) {
		for _, salida := range(salidas_p) {
			salida.Flush()
		}
	}
}
