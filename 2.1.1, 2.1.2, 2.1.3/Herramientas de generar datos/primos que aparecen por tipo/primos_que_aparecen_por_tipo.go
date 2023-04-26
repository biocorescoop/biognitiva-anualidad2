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
)

type dicfrecuencias map[int][]int

func main() {
	//var err error
	var entrada_marcos *csv.Reader
	var esprimo []bool
	p := 0
	cmax := 100
	cmin := 59
	n := 1
	base := 0
	dist := 0
	intervalos := 0
	ireducida := true
	//imarcos := false
	nombre_otipos := "frec_primos"
	
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
			case "-log" :
				base, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-dist" :
				dist, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-intervalos" :
				intervalos, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	fmt.Println("p = " + strconv.Itoa(p) + ", n = " + strconv.Itoa(n))
	fmt.Println("ireducida = " + strconv.FormatBool(ireducida))
	
	if intervalos > 0 {
		dist = cmax / intervalos
	}
	if dist <= 0 && base <= 0 {
		base = 10
		fmt.Println("base = ", base)
	}
	
	esprimo = make([]bool, 2*cmax)
	matanid.Gen_esprimo(esprimo, cmax)
	
	frecuencias := make([]dicfrecuencias, len(matanid.Tipos))
	salida_tipos := make([]*csv.Writer, len(matanid.Tipos))
	
	var numfrec, escala, logmin int
	if base > 0 {
		logmin = log_base(cmin, base)
		fmt.Println("logmin = ", logmin)
		numfrec = log_base(cmax-1, base) - logmin + 1
		fmt.Print("escalas: ")
		for escala := 0; escala < numfrec; escala++ {
			fmt.Print(exp(base, escala + logmin), " ")
		}
		fmt.Println()
	} else {
		numfrec = cmax/dist
	}
	
	for nom_tipo, num_tipo := range matanid.Tipos {
		frecuencias[num_tipo] = gen_dicc_primos(esprimo, numfrec)
		
		nombre := "frec_primos/" + nom_tipo + "/" + nombre_otipos + "_mod_" + strconv.Itoa(p)
		if base > 0 {
			nombre = nombre + "_log" + strconv.Itoa(base) + ".csv"
		} else {
			nombre = nombre + "_lineal" + strconv.Itoa(dist) + ".csv"
		}
		
		f_salida, err := os.Create(nombre)
		if err != nil { log.Fatal(err) }
		defer f_salida.Close()
		
		salida_tipos[num_tipo] = csv.NewWriter(f_salida)
		if err != nil { log.Fatal(err) }
		
		fmt.Println("archivo de tipo ", num_tipo, " : ", nombre)
	}
	
	primos := gen_primos(esprimo)
		
	for {
		linea, err := entrada_marcos.Read()
		
		if err == io.EOF { break }
		if err != nil { log.Fatal(err) }
		
		matriz := matanid.Strings_to_array(linea)
		
		if ireducida == true {
			matriz = matanid.Desreducir_marco(matriz, n)
		}
		
		matriz_modp := matanid.Array_modp(matriz, p)
		num_tipo := matanid.Tipo_de_matriz(matriz_modp)
		
		if matriz[0] >= cmax { break }
		if matriz[0] < cmin { continue }
		
		if base > 0 {
			escala = log_base(matriz[0], base) - logmin
			//fmt.Println("c = ", matriz[0], " escala = ", escala)
		} else {
			escala = matriz[0]/dist
			//fmt.Println("c = ", matriz[0], " escala = ", escala)
		}
		
		for _, i := range(matriz) {
			frecuencias[num_tipo][i][escala]++
			//fmt.Println("frecuencias[", num_tipo, "][", i, "][", escala, "] = ", frecuencias[num_tipo][i][escala])
		}
	}
		
	for _, num_tipo := range(matanid.Tipos) {
		//for i, frec := range(frecuencias[num_tipo]) {
		for _, i := range(primos) {
			frec := frecuencias[num_tipo][i]
			
			//if num_tipo == 2 { fmt.Println(i, frec) }
			
			array_salida := make([]string, len(frec)+1)
			array_salida[0] = strconv.Itoa(i)
			for j, val := range(frec) {
				array_salida[j+1] = strconv.Itoa(val)
			}
			//fmt.Println(array_salida)
			salida_tipos[num_tipo].Write(append(array_salida))
		}
		
		salida_tipos[num_tipo].Flush()
	}
}

func gen_dicc_primos(esprimo []bool, numfrecs int) dicfrecuencias {
	diccionario := make(dicfrecuencias)
	
	for p, val := range(esprimo) {
		if val == true {
			diccionario[p] = make([]int, numfrecs)
		}
	}
	return diccionario
}

func gen_primos(esprimo []bool) []int {
	var primos []int
	for p, val := range(esprimo) {
		if val == true { primos = append(primos, p) }
	}
	return primos
}

func log_base(val int, base int) int {
	log := 0
	for val > base { 
		val = val/base
		log++
	}
	return log
}

func exp(base int, exponente int) int {
	res := 1
	for i := 0; i < exponente; i++ { 
		res = res*base
	}
	return res
}
