package main

import (
	"fmt"
	"matanid"
	"strconv"
	"os"
	"io"
	"log"
	"encoding/csv"
	"time"
)

func main() {
	var entrada *csv.Reader
	var salida *csv.Writer
	
	p := 0
	n := 1
	cuantas := 10000
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				fmt.Println("n = " + os.Args[i+1])
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				fmt.Println("p = " + os.Args[i+1])
				i++
				
			case "-i" :
				f_entrada, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_entrada.Close()
				
				entrada = csv.NewReader(f_entrada)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada_= " + os.Args[i+1])
				i++
			case "-o" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("salida = " + os.Args[i+1])
				i++
			case "-cuantas" :
				cuantas, _ = strconv.Atoi(os.Args[i+1])
				fmt.Println("cuantas = " + os.Args[i+1])
				i++
		}
	}
	
	linea, err := entrada.Read()
	if err != nil { log.Fatal(err) }
	
	matriz := matanid.Strings_to_array(linea)
	matriz_modp := matanid.Array_modp(matriz, p)
	num_tipo := matanid.Tipo_de_matriz(matriz_modp)
	
	max := maximo_matriz(matriz)
	cmin := matriz[0]
	cmax := matriz[0]
	//numzeros := matanid.Zerosmatriz(matriz)
	
	for {
		linea, err := entrada.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		matriz := matanid.Strings_to_array(linea)
		
		max_linea := maximo_matriz(matriz)
		
		if max_linea > max { max = max_linea }
		if matriz[0] < cmin { cmin = matriz[0] }
		if matriz[0] > cmax { cmax = matriz[0] }
	}
	fmt.Println("pmax = ", max)
	
	esprimo := make([]bool, 2*max)
	matanid.Gen_esprimo(esprimo, max)
	
	var q int
	for num, val := range(esprimo) {
		if num < max/p { continue }
		if val == true {
			q = num
			fmt.Println("q = ", q)
			break
		} else {
			fmt.Println(num, " no es primo")
		}
	}
	primos := []int{p, q}
	N := p*q
	
	fmt.Println("p = ", p, ", q = ", q, ", N = pq = ", N)
	coefs_chinos := matanid.CoefsChinese(primos)
	fmt.Println("coefs_chinos = ", coefs_chinos)
	
	var centros []int
	for c := 0; c < q; c++ {
		centro := coefs_chinos[0]*1+coefs_chinos[1]*c
		if cmin <= centro && cmax >= centro && (centro % 2)*(centro % 3) != 0 {
			centros = append(centros, c)
		}
	}
	fmt.Println("centros = ", centros)
	
	var hilos[2] matanid.Mihilo
	hilos[0].Inicializar(n, 8*n+1)
	hilos[1].Inicializar(n, 8*n+1)
	
	hilos[0].Gen_all_marcos_modp(p, num_tipo, 0)
	go hilos[1].Gen_marcos_tipo_modp(centros, -1, q, cmin)
	
	time.Sleep(5*time.Second)
	
	matrices := make([][]int, 2)
	for j := 0; j < hilos[1].Elementos() || hilos[1].Procesando > 0; j++ {
		for j == hilos[1].Elementos() && hilos[1].Procesando > 0 { time.Sleep(time.Second) }
		
		if j == hilos[1].Elementos() && (hilos[1].Procesando <= 0) { break }
		
		matrices[1] = hilos[1].Get(j)
		
		for i := 0; i < hilos[0].Elementos(); i++ {
			matrices[0] = hilos[0].Get(i)
			matriz := matanid.Componer_matriz_coefs(coefs_chinos, N, matrices)
			
			if hay_unos(matriz) { continue }
			if multiplos_de_p(matriz, 2) != 0 { continue }
			if multiplos_de_p(matriz, 3) != 0 { continue }
			
			salida.Write(matanid.Array_to_strings(matriz))
			if cuantas != -1 {
				cuantas--
				if cuantas == 0 {
					salida.Flush()
					return
				}
			}
		}
		salida.Flush()
		
		if hilos[1].Fin_de_bloque(j) { hilos[1].Free_bloque(j) }
	}
}

func maximo_matriz(matriz []int) int {
	max := 0
	for _, x := range(matriz) { if x > max { max = x } }
	
	return max
}

func multiplos_de_p(matriz []int, p int) int {
	mult := 0
	for _, x := range(matriz) {
		if x % p == 0 { mult ++ }
	}
	return mult
}

func hay_unos(matriz []int) bool {
	for _, x := range(matriz) {
		if x == 1 { return true }
	}
	return false
}
