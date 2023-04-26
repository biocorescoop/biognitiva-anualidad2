package main

import (
//	"fmt"
	"os"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
)

var p = 3
var modc = false
var numzeros = 1

var niveles = []int{1, 2, 3}

var ppio_archivo = "marcos"

func main() {
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-modc" :
				modc = true
			case "-niveles" :
				niveles = calc_niveles(os.Args[i+1])
				i++
			case "-n" :
				n, _ := strconv.Atoi(os.Args[i+1])
				niveles = []int{n}
				i++
			case "-p" :
				p, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-numzeros" :
				numzeros, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	
	hilos_modp := make([]matanid.Mihilo, len(niveles))
	hilos_modc := make([]matanid.Mihilo, len(niveles))
	
	
	for k := 0; k < len(niveles); k++ {
		ppio_archivo_k := ppio_archivo + "_" + strconv.Itoa(2*niveles[k]+1) + "x" + strconv.Itoa(2*niveles[k]+1)
		if modc {
			hilos_modc[k].Inicializar(niveles[k], 8*niveles[k])
			f, err := os.Create(ppio_archivo_k + "_modc.csv")
			if err != nil {
				log.Fatal(err)
				return
			}
			hilos_modc[k].Salida = csv.NewWriter(f)
			
			defer f.Close()
		}
		if p > 0 {
			hilos_modp[k].Inicializar(niveles[k], 8*niveles[k]+1)
			f, err := os.Create(ppio_archivo_k + "_mod_" + strconv.Itoa(p) + ".csv")
			if err != nil {
				log.Fatal(err)
				return
			}
			defer f.Close()
			hilos_modp[k].Salida = csv.NewWriter(f)
		}
	}
	
	if p > 0 {
		for k := 0; k < len(niveles); k++ {
			hilos_modp[k].Gen_marcos_modp(p, numzeros)
			hilos_modp[k].WriteBuffer()
		}
	}
	
}

func calc_niveles(argumento string) []int {
	return nil
}
