package main

import (
	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
	//"strconv"
	"matanid"
)

func main() {
	var salida *csv.Writer
	var entrada *csv.Reader
	//var p, n int
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-i" :
				//imarcos = true
				f_entrada, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_entrada.Close()
				
				entrada = csv.NewReader(f_entrada)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada = " + os.Args[i+1])
				i++
			case "-o" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("salida = " + os.Args[i+1])
				i++
		}
	}
	
	var marcos_frec [][]int
	
	for {
		linea, err := entrada.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		marcos_frec = append(marcos_frec, matanid.Strings_to_array(linea))
	}
	
	//datos := matanid.Gen_datos_tipos(marcos_frec)
	//matanid.Escribir_datos(salida, datos)
	
	matanid.Escribir_datos(salida, matanid.Gen_datos_tipos(marcos_frec))
	
	salida.Flush()
}
