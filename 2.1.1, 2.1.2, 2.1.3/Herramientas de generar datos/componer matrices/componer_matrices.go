package main

import (
	"fmt"
	"os"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
)

var esprimo []bool
var cmax, cmin, n, cuantas int

type cmarcos struct {
	c int
    //elementos uint64
    marcos [][]int
}

func main() {
	var filename, filename1, filename2 string
	var reducida, ok bool
	canal_matrices := make(chan []int, 10)
	canal_marcos1 := make(chan [][]int,10)
	canal_marcos2 := make(chan [][]int,10)
	terminado := make(chan bool)
	cuantas = -1
	var c1, c2 int
	var bloq1 [][]int
	var bloq2[][]int
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-cmax":
				cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmin":
				cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-i1" :
				filename1 = os.Args[i+1]
				i++
			case "-i2" :
				filename2 = os.Args[i+1]
				i++
			case "-o" :
				filename = os.Args[i+1]
				i++
			case "-n" :
				n, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cuantas" :
				cuantas, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	
	if n == 0 { n = 2 }
	
	if len(filename) == 0 { filename = fmt.Sprintf("matrices_%dx%d.csv", 2*n+1, 2*n+1) }
	
	go Leer_marcos(filename1, canal_marcos1)
	go Leer_marcos(filename2, canal_marcos2)
	go Recibe_matrices(filename, canal_matrices, terminado)
	
	<- terminado
}

func New_contiene(contiene []int, array []int) (int, []int) {
	var newcontiene []int
	cuantos := 0
	
	for _, valor := range contiene {
		rep := Contiene_elem(array, valor)
		if rep > 0 {
			cuantos += rep
		} else {
			newcontiene = append(newcontiene, valor)
		}
	}
}

func Contiene_elem(array []int, valor int) int {
	cuantos := 0
	for _, val := range array { if val == valor { cuantos++ }}
	return cuantos
}


func Rellenar_matriz(marcos [][]int) []int {
	n := len(marcos)-1
	matriz := marcos[0]
	for _, marco := range marcos { matriz = append(matriz, marco) }
	return matriz
}

func Componer_matrices(chan_marcos []chan cmarcos, canal_matrices chan []int) {
	for {
		if marcos1.c < marcos2.c {
			if marcos1, ok <- canal_marcos1; ok == false { break }
			if marcos1.c < cmin { continue }
		} else if marcos1.c > marcos2.c {
			if marcos2, ok <- canal_marcos1; ok == false { break }
			if marcos2.c < cmin { continue }
		} else {
			if marcos1, ok <- canal_marcos1; ok == false { break }
			if marcos2, ok <- canal_marcos1; ok == false { break }
		}
		
		if marcos1.c != marcos2.c { continue }
		
		if marcos1.c < cmin { continue }
		if marcos1.c < cmax { break }
		
		
		marcos[0] = [1]int{ marcos1.c }
		
		for _, marcos[1] = range marcos1.marcos {
			for _, marcos[2] = range marcos2.marcos {
				for _, val1 := range marcos[1] { for _, val1 := range marcos[2] { if val1 == val2 { goto no_compatibles }}}
				
				canal_matrices <- Rellenar_matriz(marcos)
				
				no_compatibles:
				continue
			}
		}
	}
	
}

func Recibe_matrices(filename string, canal_matrices chan []int, terminado chan bool) {
	f_salida, err := os.Create(filename)
	if err != nil { log.Fatal(err) }
	defer f_salida.Close()
	
	salida := csv.NewWriter(f_salida)
	if err != nil { log.Fatal(err) }
	
	for matriz := range canal_matrices {
		salida.Write(matanid.Array_to_strings(matriz))
	}
	salida.Flush()
	terminado <- true
}
