package main

import (
	"fmt"
	"matanid"
	"strconv"
	"os"
	"log"
	"encoding/csv"
	//"time"
)

var n = 1
var tope = 18
var nombre_salida = "marcos_"

func main() {
	esprimo := make([]bool, tope)
	matanid.Gen_esprimo(esprimo, tope/2)
	primos := matanid.Lista_primos(esprimo)
	
	hilos_modp := make([]matanid.Mihilo, len(primos))
	N := 1
	for i, p := range(primos) {
		if i < len(primos)-1 {
			go make_hilo(hilos_modp[i], p)
		} else {
			go make_last_hilo(hilos_modp[i], p)
		}
		N = N*p
	}
	
	f, err := os.Create(nombre_salida + strconv.Itoa(N) + "x" + strconv.Itoa(N) + "_chino.csv")
	if err != nil {
		log.Fatal(err)
		return
	}
	defer f.Close()
	salida := csv.NewWriter(f)
	
	fmt.Println("Generamos los coeficientes del Teorema Chino de los Restos")
	coefs_chinos := matanid.CoefsChinese(primos)
	cota_criba := primos[len(primos)-1]*primos[len(primos)-1]
	
	fmt.Println("Generamos los índices")
	tam := make([]int, len(hilos_modp))
	for i, hilo := range(hilos_modp) {
		<-hilo.Done
		tam[i] = hilo.Elementos()
		fmt.Println("Se han generado ", tam[i], " matrices mod ", primos[i])
	}
	indices := matanid.Combinar_indices(tam)
	
	for num := 0; num < indices.Elementos(); num++ {
		variaciones_matriz := make([][][]int, len(primos))
		matriz := matanid.Get_comb_hilos(hilos_modp, indices.Get(num))
		
		salida.Write(matanid.Array_to_strings(matanid.Componer_matriz_coefs(coefs_chinos, N, matriz, cota_criba)))
		
		salida.Flush()
		
		if num % 1000 == 0 {fmt.Println(num, " matrices generadas. Vamos por el indice ", indices.Get(num)) }
	}
}

func make_hilo(hilo matanid.Mihilo, p int) {
	hilo.N = n
	
	f, err := os.Create(nombre_salida + strconv.Itoa(n) + "x" + strconv.Itoa(n) + "_mod_" + strconv.Itoa(p) + ".csv")
	if err != nil {
		log.Fatal(err)
		return
	}
	defer f.Close()
	hilo.Salida = csv.NewWriter(f)
	
	hilo.Gen_all_marcos_modp(p, 1)
	hilo.WriteBuffer()
}

func make_last_hilo(hilo matanid.Mihilo, p int) {
	hilo.N = n
	
	f, err := os.Create(nombre_salida + strconv.Itoa(n) + "x" + strconv.Itoa(n) + "_mod_" + strconv.Itoa(p) + ".csv")
	if err != nil {
		log.Fatal(err)
		return
	}
	defer f.Close()
	hilo.Salida = csv.NewWriter(f)
	
	hilo.Gen_marcos_modp(p, 1)
	hilo.WriteBuffer()
}
