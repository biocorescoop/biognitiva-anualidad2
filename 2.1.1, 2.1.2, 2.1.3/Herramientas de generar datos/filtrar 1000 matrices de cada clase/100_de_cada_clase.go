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
	salida_tipos := make([]*csv.Writer, len(matanid.Tipos))
	var entrada_marcos *csv.Reader
	var esprimo []bool
	p := 0
	n := 1
	pmax := 0
	nozerofrec := false
	numzeros := 1
	ireducida := true
	//imarcos := false
	nombre_otipos := "matrices"
	cuantas := 1000
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				n, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-pmax" :
				pmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-nozerofrec" :
				nozerofrec = true
			case "-numzeros" :
				numzeros, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-ireducida" : // no va!!
				ireducida = true
				fmt.Println("ireducida = " + strconv.FormatBool(ireducida))
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada_marcos reducida = " + os.Args[i+1])
				i++
			case "-imarcos" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("entrada_marcos = " + os.Args[i+1])
				i++
			case "-otipos" :
				nombre_otipos = os.Args[i+1]
				i++
			case "-cuantas" :
				cuantas = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	fmt.Println("p = " + strconv.Itoa(p) + ", n = " + strconv.Itoa(n) + ", -numzeros = " + strconv.Itoa(numzeros))
	fmt.Println("nozerofrec = ", strconv.FormatBool(nozerofrec) + ", ireducida = " + strconv.FormatBool(ireducida))
	fmt.Println("cuantas = " + strconv.Itoa(cuantas))
	
	if pmax == 0 {
		nombre_otipos = nombre_otipos + "_mod_" + strconv.Itoa(p)
		for nom_tipo, num_tipo := range matanid.Tipos {
			f_salida, err := os.Create("primos/" + nom_tipo + "/" + ".csv")
			if err != nil { log.Fatal(err) }
			defer f_salida.Close()
			
			salida_tipos[num_tipo] = csv.NewWriter(f_salida)
			if err != nil { log.Fatal(err) }
			
			fmt.Println("archivo de tipo ", num_tipo, " : ", nombre_otipos + "_" + nom_tipo + ".csv")
		}
	}
	
	if pmax > 0 {
		if pmax % 2 == 1 { pmax++ }
		esprimo = make([]bool, pmax)
		matanid.Gen_esprimo(esprimo, pmax/2)
		primos := matanid.Lista_primos(esprimo)
		for i, p := range(primos) {
			for nom_tipo, num_tipo := range matanid.Tipos {
				nombre := "primos/" + nom_tipo + "/" + nombre_otipos + "_mod_" + strconv.Itoa(p) + ".csv"
				f_salida, err := os.Create(nombre)
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				salida_tipos[i][num_tipo] = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				
				fmt.Println("archivo de tipo ", num_tipo, " : ", nombre)
			}
		}
	}
	
	frecuencias := make([]int, len(matanid.Tipos))
	
	var matriz, matriz_modp []int
	
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		if (ireducida == false) {
			matriz, matriz_modp = linea_modp(linea, p)
		} else {
			matriz, matriz_modp = linea_reducida_modp(linea, p)
		}
		
		num_tipo := matanid.Tipo_de_matriz(matriz_modp)
		frecuencias[num_tipo]++
		if frecuencias[num_tipo] < cuantas {
			salida_tipos[num_tipo].Write(matanid.Array_to_strings(matriz))
		} else {
			if frecuencias[num_tipo] == cuantas { salida_tipos[num_tipo].Flush() }
		}
	}
	
	for num_tipo, frec := range(frecuencias) {
		if frec < cuantas {
			salida_tipos[num_tipo].Flush()
		}
	}
}

func linea_modp(linea []string, p int) ([]int, []int) {
	matriz := matanid.Strings_to_array(linea)
	matriz_modp := matanid.Array_modp(matriz, p)
	
	return matriz, matriz_modp
}

func linea_reducida_modp(linea []string, p int) ([]int, []int) {
	n := (len(linea) - 1)/4
	matriz := matanid.Strings_to_array(linea)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	matriz = matanid.Desreducir_marco(matriz, n)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	matriz_modp := matanid.Array_modp(matriz, p)
	//fmt.Println(matanid.Array_to_strings(matriz))
	
	return matriz, matriz_modp
}
