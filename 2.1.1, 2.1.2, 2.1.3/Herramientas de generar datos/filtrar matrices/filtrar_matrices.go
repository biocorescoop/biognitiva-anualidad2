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
	"strings"
)


func main() {
	//var err error
	var entrada_marcos *csv.Reader
	var contenido, esquinas, aristas, centros, como_modp []int
	p := 0
	cmax := 0
	cmin := 0
	n := 1
	tipo := -1
	cuantos := -1
	
	todos := true
	ireducida := true
	//imarcos := false
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmin" :
				cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmax" :
				cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-ireducida" : // no va!!
				ireducida = true
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-imarcos" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-tipo" :
				tipo = matanid.Tipos[os.Args[i+1]]
				i++
			case "-matriz_modp":
				como_modp = matanid.Strings_to_array(strings.Split(os.Args[i+1], ","))
				i++
			case "-contiene":
				contenido, esquinas, aristas, centros = proc_contiene(os.Args[i+1])
				i++
			case "-todos" :
				todos = true
			case "-cuantos":
				cuantos, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	//fmt.Println("p = " + strconv.Itoa(p) + ", n = " + strconv.Itoa(n))
	//fmt.Println("ireducida = " + strconv.FormatBool(ireducida))
	
	if p != 0 && tipo == 6 && p < 59 { return }
		
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		matriz := matanid.Strings_to_array(linea)
		
		if ireducida == true { matriz = matanid.Desreducir_marco(matriz, n) }
		
		if cmax != 0 { if matriz[0] >= cmax { break } }
		if cmin != 0 { if matriz[0] < cmin { continue } }
		
		if p != 0 {
			matriz_modp := matanid.Array_modp(matriz, p)
			if tipo != -1 {
				numtipo := matanid.Tipo_de_matriz(matriz_modp)
				if numtipo != tipo { continue }
			} else if len(como_modp) > 0 {
				if matanid.Comp_matrices(matriz_modp, como_modp) != 0 { continue }
			}
		}
		
		if len(contenido) > 0 {
			aparece := 0
			for _, x := range(matriz) { for _, valor := range(contenido) {
				if valor == x { aparece ++ }
			}}
			if aparece == 0 { continue }
			if todos { if aparece != len(contenido) { continue } }
		}
		
		if len(esquinas) > 0 {
			aparece := 0
			for _, x := range(matriz) { for _, valor := range(contenido) {
				if valor == x { aparece ++ }
			}}
			if aparece == 0 { continue }
		}
		
		if len(aristas) > 0 {
			aparece := 0
			for _, x := range(matriz) { for _, valor := range(contenido) {
				if valor == x { aparece ++ }
			}}
			if aparece == 0 { continue }
		}
		
		if len(centros) > 0 {
			aparece := 0
			for _, x := range(matriz) { for _, valor := range(contenido) {
				if valor == x { aparece ++ }
			}}
			if aparece == 0 { continue }
		}
		
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

func proc_contiene(linea string) ([]int, []int, []int, []int) {
	var contenido []int
	var esquinas []int
	var aristas []int
	var centros []int
	
	for _, cosa := range(strings.Split(linea, ",")) {
		cont := strings.Split(cosa, "-")
		primo, _ := strconv.Atoi(cont[0])
		if len(cont) == 1 {
			contenido = append(contenido, primo)
		} else if cont[1] == "esquina" {
			esquinas = append(esquinas, primo)
		} else if cont[1] == "arista" {
			aristas = append(aristas, primo)
		} else if cont[1] == "centro" {
			centros = append(centros, primo)
		}
	}
	return contenido, esquinas, aristas, centros
}
