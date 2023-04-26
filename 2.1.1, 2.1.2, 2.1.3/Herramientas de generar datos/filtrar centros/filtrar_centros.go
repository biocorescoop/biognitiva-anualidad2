package main

import (
	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
	"strconv"
	//"sort"
	//"strings"
)


func main() {
	//var err error
	var entrada_marcos *csv.Reader
	
	cmax := 0
	cmin := 0
	cuantos := 0
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-cmin" :
				cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmax" :
				cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-i" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-cuantos":
				cuantos, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
		
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		matriz := Strings_to_array(linea)
		
		//if ireducida == true { matriz = matanid.Desreducir_marco(matriz, n) }
		
		if cmax != 0 { if matriz[0] >= cmax { continue } }
		if cmin != 0 { if matriz[0] < cmin { continue } }
		
		// si hemos llegado aquí es porque se cumplen las condiciones
		
		fmt.Println(prep_linea(matriz))
		if cuantos > 0 {
			cuantos--
			if cuantos == 0 { break }
		}
	}
}

func prep_linea(array []int) string {
	linea := ""
	for i, x := range(array) {
		if i != 0 { linea = linea + "," }
		linea = linea + strconv.Itoa(x)
	}
	return linea
}

func Strings_to_array(src []string) []int {  
	array := make([]int, len(src))
	for i, val := range src {
		array[i], _ = strconv.Atoi(val)
	}
	return array
}
