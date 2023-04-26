package main

import (
	"fmt"
	"os"
	"io"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
)

func main() {
	//var err error
	var salida *csv.Writer
	var entrada_modp, entrada_marcos *csv.Reader
	//var salida_tipos *os.File
	var p, n int
	nozerofrec := false
	numzeros := 1
	ireducida := true
	//imarcos := false
	otipos := false
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-nozerofrec" :
				nozerofrec = true
			case "-numzeros" :
				numzeros, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-ireducida" : // no va!!
				ireducida = true
				fmt.Println("ireducida = " + strconv.FormatBool(ireducida))
			case "-imarcos" :
				//imarcos = true
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada_marcos = " + os.Args[i+1])
				i++
			case "-imodp" :
				f_modp, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_modp.Close()
				
				entrada_modp = csv.NewReader(f_modp)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada_modp = " + os.Args[i+1])
				i++
			case "-o" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("salida = " + os.Args[i+1])
				i++
			/*
			case "-otipos" :
				otipos = true
				salida_tipos, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida_tipos.Close()
				
				fmt.Println("salida_tipos = " + os.Args[i+1])
				i++
				*/
		}
	}
	fmt.Println("p = " + strconv.Itoa(p) + ", n = " + strconv.Itoa(n) + ", -numzeros = " + strconv.Itoa(numzeros))
	fmt.Println("nozerofrec = ", strconv.FormatBool(nozerofrec) + ", ireducida = " + strconv.FormatBool(ireducida))
	
	//if (imarcos) {
	marcos_modp := leer_matrices(entrada_modp)
	
	fmt.Println(strconv.Itoa(len(marcos_modp)) + " matrices leidas")
	
	frecuencias := make([]int, len(marcos_modp))
	
	//tipos_matriz := make([]int, len(marcos_modp))
	
	//clasificar_marcos(marcos_modp, tipos_matriz)
	//}
	
	var otrosmarcos_modp [][]int
	var otrasfrecuencias []int
	var matriz []int
	
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		if (ireducida == false) {
			matriz = linea_modp(linea, p)
		} else {
			matriz = linea_reducida_modp(linea, p)
		}
		
		//fmt.Println("matriz sin ordenar: ", matanid.Array_to_strings(matriz))
		matanid.Ordenar_marco_modp(matriz[1:], n)
		//fmt.Println("matriz ordenada: ", matanid.Array_to_strings(matriz))
		
		i := buscar_matriz(matriz, marcos_modp)
		
		if i > -1 {
			frecuencias[i]++
		} else {
			i := buscar_otramatriz(matriz, otrosmarcos_modp)
			if i >= 0 { otrasfrecuencias[i]++
			} else {
				fmt.Println("matriz ",linea, " -> ", matanid.Array_to_strings(linea_reducida_modp(linea, p)), " -> ", matanid.Array_to_strings(matriz), " no encontrada en el archivo")
				otrosmarcos_modp = append(otrosmarcos_modp, matriz)
				otrasfrecuencias = append(otrasfrecuencias, 1)
			}
		}
	}
	
	for i, matriz := range marcos_modp {
		if nozerofrec && frecuencias[i] == 0 { continue }
		if matanid.Zerosmatriz(matriz) > numzeros { continue }
		linea := matanid.Array_to_strings(matriz)
		linea = append(linea, strconv.Itoa(frecuencias[i]))
		salida.Write(linea)
	}
	
	if len(otrosmarcos_modp) > 0 {
		salida.Write([]string{"Matrices que no estaban en la lista!!!"})
		
		for i, matriz := range otrosmarcos_modp {
			linea := matanid.Array_to_strings(matriz)
			linea = append(linea, strconv.Itoa(otrasfrecuencias[i]))
			salida.Write(linea)
		}
	}
	salida.Flush()
	
	//datos_tipos := gen_datos_tipos(marcos_modp, frecuencias)
}

func linea_modp(linea []string, p int) []int {
	matriz := matanid.Strings_to_array(linea)
	matriz = matanid.Array_modp(matriz, p)
	
	return matriz
}

func linea_reducida_modp(linea []string, p int) []int {
	n := (len(linea) - 1)/4
	matriz := matanid.Strings_to_array(linea)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	matriz = matanid.Desreducir_marco(matriz, n)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	matriz = matanid.Array_modp(matriz, p)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	return matriz
}

func buscar_matriz(matriz []int, lista [][]int) int { // no está funcionando como debería
	// si no encuentra el elemento devuelve -1
	i := 0
	dist := len(lista)/2
	mov := 1 // empezamos subiendo a 1/2 len
	denom := 2
	
	for dist > 1 {
		i = i + dist*mov
		mov = comp_matrices_busq(matriz, lista[i])
		if mov == 0 { return i }
		
		denom = denom*2
		dist = len(lista)/denom
	}
	
	if mov > 0 {
		tope := len(lista) //i + 5*dist
		for i++; i < tope; i++ {
			mov = comp_matrices_busq(matriz, lista[i])
			if mov == 0 { return i }
			if mov < 0 { return -1}
		}
		return -1
	}
	
	if mov < 0 {
		tope := 0 //i - 5*dist
		for i--; i > tope; i-- {
			mov = comp_matrices_busq(matriz, lista[i])
			if mov == 0 { return i }
			if mov > 0 { return -1}
		}
		return -1
	}
	return -1
}

func comp_matrices_busq (matriz1 []int, matriz2 []int) int {
	n := (len(matriz1)-1)/8
	// comparamos el elemento central
	if matriz1[0] < matriz2[0] { return -1 }
	if matriz1[0] > matriz2[0] { return 1 }
	
	// comparamos las esquinas
	if matriz1[1] < matriz2[1] { return -1 }
	if matriz1[1] > matriz2[1] { return 1 }
	
	if matriz1[2*n+1] < matriz2[2*n+1] { return -1 }
	if matriz1[2*n+1] > matriz2[2*n+1] { return 1 }
	
	if matriz1[6*n] < matriz2[6*n] { return -1 }
	if matriz1[6*n] > matriz2[6*n] { return 1 }
	
	if matriz1[8*n] < matriz2[8*n] { return -1 }
	if matriz1[8*n] > matriz2[8*n] { return 1 }
	
	// comparamos la arista 1
	for i := 2; i < 2*n+1; i++ {
		if matriz1[i] < matriz2[i] { return -1 }
		if matriz1[i] > matriz2[i] { return 1 }
	}
	
	// comparamos la arista 2
	for i := 2*n+2; i < 6*n; i += 2 {
		if matriz1[i] < matriz2[i] { return -1 }
		if matriz1[i] > matriz2[i] { return 1 }
	}
	return 0
}

func buscar_otramatriz(matriz []int, lista [][]int) int {
	for i, matriz2 := range lista {
		if matanid.Comp_matrices(matriz, matriz2) == 0 { return i }
	}
	return -1
}

func leer_matrices(entrada *csv.Reader) [][]int {
	var lista [][]int
	for {
		linea, err := entrada.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		lista = append(lista, matanid.Strings_to_array(linea))
	}
	return lista
}

