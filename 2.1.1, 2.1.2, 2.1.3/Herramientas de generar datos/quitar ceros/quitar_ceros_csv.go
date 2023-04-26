package main

import (
//	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
//	"strconv"
//	"matanid"
)

func main() {
	f1, err := os.Open(os.Args[1])
	if err != nil { log.Fatal(err) }
	
	f2, err := os.Create(os.Args[2])
	if err != nil { log.Fatal(err) }
	
	defer f1.Close()
	defer f2.Close()
	
	entrada := csv.NewReader(f1)
	salida := csv.NewWriter(f2)
	
	defer salida.Flush()
	
	for {
		matriz, err := entrada.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		if hay_ceros(matriz) { continue }
		
		err = salida.Write(matriz)
		if err != nil { log.Fatal(err) }
	}
}

func hay_ceros(array []string) bool {
	for _, val := range array {
		if val == "0" { return true }
	}
	return false
}
