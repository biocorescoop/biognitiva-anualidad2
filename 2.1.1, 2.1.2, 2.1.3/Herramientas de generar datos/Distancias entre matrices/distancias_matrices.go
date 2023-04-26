package main

import (
	"fmt"
	"os"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
	//"sort"
	"strings"
	"distancias"
//	"math"
)

/*
 * Genera para cada matriz la distancia a la matriz mas cercana. Se le
 * puede pedir que las busque sólo en las matrices con las que comparte
 * estrucutura módulo p, que contenga ciertos elementos...
*/

func main() {
	//var err error
	var datos distancias.Datos_leer
	cuantos := -1
	datos.N = 1
	var coef float64 = 0
	datos.Cmin = 59
	he_liberado := false
	restar := false
	
	var matriz_modp []int
	
	//imarcos := false
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-n" :
				datos.N, _= strconv.Atoi(os.Args[i+1])
				i++
			case "-p" :
				datos.P, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-coef" :
				coef, _ = strconv.ParseFloat(os.Args[i+1], 64)
				i++
			case "-cmin" :
				datos.Cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmax" :
				datos.Cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-ireducida" :
				datos.Ireducida = true
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				datos.Entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-imarcos" :
				f_marcos, err := os.Open(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_marcos.Close()
				
				datos.Entrada_marcos = csv.NewReader(f_marcos)
				if err != nil { log.Fatal(err) }
				
				i++
			case "-tipo" :
				datos.Tipo = matanid.Tipos[os.Args[i+1]]
				i++
			case "-matriz_modp":
				datos.Como_modp = matanid.Strings_to_array(strings.Split(os.Args[i+1], ","))
				i++
			case "-contiene":
				datos.Contenido, datos.Esquinas, datos.Aristas, datos.Centros = proc_contiene(os.Args[i+1])
				i++
			case "-cuantos":
				cuantos, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-o" :
				f_salida, err := os.Create(os.Args[i+1])
				if err != nil { log.Fatal(err) }
				defer f_salida.Close()
				
				datos.Salida = csv.NewWriter(f_salida)
				if err != nil { log.Fatal(err) }
				i++
			case "-restar" :
				restar = true
		}
	}
	
	if datos.P != 0 && datos.Tipo == 6 && datos.P < 59 {
		fmt.Println("datos.p != 0 && datos.Tipo == 6 && datos.p < 59")
		return
	}
	
	datos.Matrices.Inicializar(4*datos.N+1)
	
	libre_bloque := datos.Leer_bloque()
	primera_matriz := datos.Matrices.Leer(0)
	ultima_primer_bloque := datos.Matrices.Leer(datos.Matrices.Elementos()-1)
	ultima_matriz := datos.Matrices.Leer(datos.Matrices.Elementos()-1)
	matriz_actual := 0
	
	r := 0
	distmaxcentros := 0 //float64(0)
	datos.Ymin = 0
	
	//fmt.Println("bloque 0 = ", datos.Matrices.Get_bloque(0))
	
	for cont := 0; cont < cuantos || cuantos == -1; cont++ {
		if libre_bloque > 0 { fmt.Println("libre_bloque = ", libre_bloque) }
		
		matriz := datos.Matrices.Leer(matriz_actual)
		if datos.P != 0 { matriz_modp = matanid.Array_modp(matriz, datos.P) }
		
		if coef == 0 {
			if datos.P == 0 {
				r = distancias.Dist0_matrices(matriz, datos.Matrices.Leer(matriz_actual+1), datos.N)
				if (matriz_actual != 0) { r = min(r, distancias.Dist0_matrices(matriz, datos.Matrices.Get(matriz_actual-1), datos.N)) }
			} else {
				elems := datos.Matrices.Elementos()
				for i := 1; i < elems ; i++ {
					if i < elems-matriz_actual {
						otramatriz := datos.Matrices.Leer(matriz_actual + i)
						if matanid.Comp_matrices(matriz_modp, matanid.Array_modp(otramatriz, datos.P)) != 0 {
							r = distancias.Dist0_matrices(matriz, otramatriz, datos.N)
							break
						}
					}
					if i < matriz_actual {
						otramatriz := datos.Matrices.Leer(matriz_actual - i)
						if matanid.Comp_matrices(matriz_modp, matanid.Array_modp(otramatriz, datos.P)) != 0 {
							r = distancias.Dist0_matrices(matriz, otramatriz, datos.N)
							break
						}
					}
				}
			}
			datos.Ymin, datos.Ymax = distancias.Ymin_Ymax(matriz[0], r)
		} else {
			r = int(float64(matriz[0]) * coef)
			datos.Ymin = matriz[0] - r
			datos.Ymax = matriz[0] + r
		}
		
		if primera_matriz[0] > datos.Ymin && datos.Ymin > datos.Cmin && he_liberado { fmt.Println("Tenemo un problemo: min = ", datos.Ymin, " < primera_matriz[0] = ", primera_matriz[0]) }
		
		for ultima_primer_bloque[0] < datos.Ymin/50 {
			he_liberado = true
			datos.Matrices.Free_first_bloques(1)
			matriz_actual -= matanid.ELEM_X_BLOQUE
			primera_matriz = datos.Matrices.Leer(0)
			ultima_primer_bloque = datos.Matrices.Get(matanid.ELEM_X_BLOQUE-1)
		}
		
		for libre_bloque == 0 && datos.Ymax > ultima_matriz[0] {
			libre_bloque = datos.Leer_bloque()
			ultima_matriz = datos.Matrices.Leer(datos.Matrices.Elementos()-1)
			fmt.Println("Elementos = ", datos.Matrices.Elementos())
		}
		
		//fmt.Println(".")
		
		d, matriz_cercana := distancias.Minima_distancia(matriz_actual, datos)
		
		if d == 0 {
			fmt.Println("d = 0, luego no se ha encontrado a la matriz compatible mas cercana")
		}
		
		go fmt.Println("Matriz[", matriz_actual, "]: ", matriz, " -> ", matriz_cercana)
		
		go fmt.Println("r = ", r, ", ymin = ", datos.Ymin, ", ymax = ", datos.Ymax, ", Elementos = ", datos.Matrices.Elementos())
		
		//dist := math.Sqrt(float64(d))
		distcentros := matriz[0] - matriz_cercana[0]
		
		if distmaxcentros < distcentros { distmaxcentros = distcentros }
		
		go fmt.Println("d = ", d, ", d/x_0 = ", float64(d)/float64(matriz[0]), ", (x_0 - y_0) = ", distcentros)
		
		if restar {
			go datos.Escribir_datos(matriz, d, distancias.Restar_matrices(matriz, matriz_cercana))
		} else {
			go datos.Escribir_datos(matriz, d, matriz_cercana)
		}
		
		matriz_actual++
		if matriz_actual >= datos.Matrices.Elementos() { break }
	}
	datos.Salida.Flush()
	
	fmt.Println("Dist max centros = ", distmaxcentros)
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

func min(val1 int, val2 int) int {
	if val1 < val2 { return val1 }
	return val2
}
