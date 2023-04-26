package main

import (
	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
	//"sort"
	//"time"
)

//var escribiendo bool
//var salida *csv.Writer
var esprimo []bool
var pares [4][2]int

func main() {
	var max, n int
	ireducida := false
	var entrada_marcos *csv.Reader
	var salida_malas, salida_buenas *csv.Writer
	pares = [4][2]int{
		[2]int{1,8},
		[2]int{2,7},
		[2]int{3,6},
		[2]int{4,5},
	}
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-max":
				max, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-omalas" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida_malas = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-obuenas" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida_buenas = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-ireducida" : // no va!!
				ireducida = true
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-i" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			
		}
	}
	
	//escribiendo = false
	esprimo = make([]bool, max)
	matanid.Gen_esprimo(esprimo)
	numprimos := matanid.Num_primos(esprimo)
	fmt.Println("Tenemos", numprimos, "primos menores que", max)
	
	var matriz []int
	var anidada, prima bool
	//var obs string
	
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		matriz = matanid.Strings_to_array(linea)
		
		if ireducida == true { matriz = matanid.Desreducir_marco(matriz, n) }
		
		no_primos := Es_prima(matriz)
		no_pares := Son_pares(matriz)
		//es_magica := Es_magica(matriz)
		prima = (len(no_primos) == 0)
		anidada = (len(no_pares) == 0)
		repes := No_repes(matriz)
		norepe := (len(repes) == 0)
		
		if prima && anidada && norepe {
			salida_buenas.Write(matanid.Array_to_strings(matriz))
			continue
		}
		/*if !prima && anidada{
			obs = "no prima"
		} else if !anidada && anidada{
			obs = "no anidada"
		} else {
			obs = "no prima y no anidada"
		}*/
		
		salida_malas.Write(append(append(matanid.Array_to_strings(matriz), fmt.Sprint(no_primos)), fmt.Sprint(no_pares)))
	}
	salida_malas.Flush()
	salida_buenas.Flush()
}

func Es_prima(matriz []int) []int {
	var no_primos []int
	for _, p := range matriz {
		if esprimo[p] == false { no_primos = append(no_primos, p) }
	}
	return no_primos
}

func Son_pares(matriz []int) [][2]int {
	var no_pares [][2]int
	if tam := len(matriz); tam != 9 {
		fmt.Println("Error, la matriz tiene tamaño", tam)
		fmt.Println(matriz)
	}
	c := matriz[0]
	for _, par := range(pares) {
		if matriz[par[0]] + matriz[par[1]] != 2*c {
			no_pares = append(no_pares, [2]int{matriz[par[0]], matriz[par[1]]})
		}
	}
	return no_pares
}

/*
func Es_magica(matriz []int) bool {
	return true
}*/

func No_repes(matriz []int) []int {
	var repes []int
	
	tam := len(matriz)
	if tam < 2 { return repes }
	
	for i, p := range matriz[:len(matriz)-1] { for _, q := range matriz[i+1:] { if p == q { repes = append(repes, p) } } }
	
	return repes
}
