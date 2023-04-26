package main

import (
	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
	"matanid"
)

func main() {
	var entrada_marcos *csv.Reader
	ireducida := true
	var p int
	var nombre_archivo string
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-ireducida" : // no va!!
				ireducida = true
				nombre_archivo = os.Args[i+1]
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-i" :
				//imarcos = true
				nombre_archivo = os.Args[i+1]
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
		}
	}
	
	max := 0
	var max_linea int
	
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		if (ireducida == false) { max_linea = maximo_linea(linea, p)
		} else { max_linea = maximo_linea_reducida(linea, p) }
		
		if max_linea > max { max = max_linea }
	}
	fmt.Println("Elemento maximo de ", nombre_archivo, " = ", max)
}

func maximo_linea(linea []string, p int) int {
	matriz := matanid.Strings_to_array(linea)
	
	max := 0
	for _, x := range(matriz) { if x > max { max = x } }
	
	return max
}

func maximo_linea_reducida(linea []string, p int) int {
	n := (len(linea) - 1)/4
	
	matriz := matanid.Strings_to_array(linea)
	matriz = matanid.Desreducir_marco(matriz, n)
	
	max := 0
	for _, x := range(matriz) { if x > max { max = x } }
	
	return max
}
