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
	//"strings"
)


func main() {
	//var err error
	var entrada *csv.Reader
	var salida *csv.Writer
	
	reducir := false
	desreducir := false
	n := -1
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-i" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-o" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-reducir" :
				reducir = true
				i++
			case "-desreducir" :
				desreducir = true
				i++
		}
	}
	
	if reducir && desreducir {
		fmt.Println("Error, no puedes reducir y desreducir")
		return
	}
		
	for {
		linea, err := entrada.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		if reducir == true { linea = linea[:4*n+1] }
		
		if desreducir == true {
			matriz := matanid.Strings_to_array(linea)
			matriz = matanid.Desreducir_marco(matriz, n)
			linea = matanid.Array_to_strings(matriz)
		}
		
		salida.Write(linea)
	}
}
