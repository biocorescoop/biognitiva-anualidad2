package main

import (
	"fmt"
	"os"
	//"io"
	"log"
	"encoding/csv"
	"strconv"
	//"eratostenes"
	//"sort"
	"time"
)

var esprimo []bool
var t0 time.Time

type Logtimes struct {
	c int
	cantidad int // -1 es que comienza la función
	n int
	time time.Duration
	unidad string
}

type Canales struct {
	Datos chan []int
	Terminado chan bool
}

func main() {
	var max, dmin, dmax, steps, long int
	var filename, file_logtimes string
	var logtimes bool
	
	var logterminado chan bool
	var canal_logtimes chan Logtimes
	
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-dmin":
				dmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-dmax":
				dmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-max":
				max, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-o" :
				filename = os.Args[i+1]
				i++
			case "-logtimes" :
				logtimes = true
			case "-steps":
				steps, _ = strconv.Atoi(os.Args[i+1])
				i++
		}
	}
	
	if steps > 0 {
		file_logtimes = fmt.Sprintf("timesteps_3x3_tripletas_0-%d-%d.csv", max, steps)
		canal_logtimes, logterminado = New_logtimes(file_logtimes, 5)
		filename = "/dev/null"
		long = max/steps
		max = long
		logtimes = false
		steps--
	}
	
	if logtimes {
		file_logtimes = fmt.Sprintf("logtimes_3x3_tripletas_0-%d.csv", max)
		canal_logtimes, logterminado = New_logtimes(file_logtimes, 5)
	}
	
	Inicio:
	
	canal_matrices := Crear_canales()
	if len(filename) == 0 { filename = fmt.Sprintf("matrices_3x3_tripletas_0-%d.csv", max) }
	go Recibe_matrices(filename, canal_matrices)
	
	fmt.Println("max = ", max, "steps =", steps)
	t0 = time.Now()
	
	esprimo = make([]bool, max)
	Gen_esprimo(esprimo)
	numprimos := Num_primos(esprimo)
	primos := Array_primos(esprimo, numprimos)
	totalmatrices := 0
	
	if dmax == 0 { dmax = max/3 }
	if dmin == 0 { dmin = 4 }
	if dmin % 2 == 1 { dmin++ }
	
	for d := dmin; d < dmax; d += 2 {
		if logtimes { canal_logtimes <- Logtimes{time: time.Since(t0), c : d, cantidad : -1, unidad : "tripletas"} }
		dtripletas := Gen_APs(primos, d)
		numtripletas := len(dtripletas)
		nummatrices := 0
		
		//fmt.Println(numtripletas, " tripletas con distancia ", d)
		if logtimes { canal_logtimes <- Logtimes{time: time.Since(t0), c : d, cantidad : numtripletas, unidad : "tripletas"} }
	
		if numtripletas < 3 { continue}
		
		if logtimes { canal_logtimes <- Logtimes{time: time.Since(t0), c : d, cantidad : -1, unidad : "matrices"} }
		
		for j := 1; j < numtripletas - 1; j++ {
			i := j - 1
			k := j + 1
			for i >= 0 && k < numtripletas {
				sum := dtripletas[i] + dtripletas[k] - 2*dtripletas[j]
				if sum == 0 {
					if dtripletas[k] - dtripletas[j] > d {
						canal_matrices.Datos <- []int{d, dtripletas[i], dtripletas[j], dtripletas[k]}
						nummatrices++
					}
					i--
					k++
				} else if sum > 0 {
					i--
				} else {
					k++
				}
			}
		}
		//fmt.Println(nummatrices, "matrices con distancia ", d)
		if logtimes { canal_logtimes <- Logtimes{time: time.Since(t0), c : d, cantidad : nummatrices, unidad : "matrices"} }
		totalmatrices += nummatrices
	}
	close(canal_matrices.Datos)
	
	<- canal_matrices.Terminado
	
	if steps > 0 {
		canal_logtimes <- Logtimes{time: time.Since(t0), c : max, cantidad : totalmatrices, unidad : "matrices"}
		max += long
		steps--
		goto Inicio
	}
	
	if logtimes || long > 0 {
		close(canal_logtimes)
		<- logterminado
	}
	
}

func Buscar_APs(primos []int, dmin int) [][3]int {
	var APs [][3]int
	numprimos := len(primos)
	
	if numprimos < 3 { return APs }
	
	for j := 1; j < numprimos - 1; j++ {
		i := j - 1
		k := j + 1
		for i >= 0 && k < numprimos {
			sum := primos[i] + primos[k] - 2*primos[j]
			if sum == 0 {
				if primos[j] - primos[k] > dmin { APs = append(APs, [3]int{primos[i], primos[j], primos[k]}) }
				i--
				k++
				continue
			}
			if sum > 0 { i-- } else { k++ }
		}
	}
	return APs
}

func Gen_APs(primos []int, dist int) []int {
	var APs []int
	max := primos[len(primos)-1] - dist
	
	for  _, p := range primos {
		if p <= dist { continue }
		if p >= max { break }
		
		if esprimo[p - dist] && esprimo[p + dist] {
			APs = append(APs, p)
		}
	}
	return APs
}

func Max_in_map(dicc map[int]bool) int {
	max := 0
	for n := range dicc { if n > max { max = n } }
	return max
}

func Array_to_strings(array []int) []string {  
	dst := make([]string, len(array))
	for i, val := range array { dst[i] = strconv.Itoa(val) }
	return dst
}

func Mostrar_primos(esprimo []bool) {
	fmt.Print("Primos: ")
	for p, val := range esprimo { if val { fmt.Print(p, " ") } }
}

func Crear_canales() Canales {
	var canales Canales
	canales.Datos = make(chan []int)
	canales.Terminado = make(chan bool)
	return canales
}

func Recibe_matrices(filename string, canal Canales) {
	f_salida, err := os.Create(filename)
	if err != nil { log.Fatal(err) }
	defer f_salida.Close()
	
	salida := csv.NewWriter(f_salida)
	if err != nil { log.Fatal(err) }
	
	matriz := make([]string, 9)
	for recib := range canal.Datos {
		tripleta := recib[1:]
		d := recib[0]
		matriz[1] = strconv.Itoa(tripleta[0])
		matriz[0] = strconv.Itoa(tripleta[1])
		matriz[8] = strconv.Itoa(tripleta[2])
		matriz[2] = strconv.Itoa(tripleta[2] + d)
		matriz[4] = strconv.Itoa(tripleta[2] - d)
		matriz[3] = strconv.Itoa(tripleta[1] - d)
		matriz[6] = strconv.Itoa(tripleta[1] + d)
		matriz[5] = strconv.Itoa(tripleta[0] + d)
		matriz[7] = strconv.Itoa(tripleta[0] - d)
		
		salida.Write(matriz[:5])
	}
	salida.Flush()
	canal.Terminado <- true
}


func New_logtimes(logfile string, hilos int) (chan Logtimes, chan bool) {
	canal_logtimes := make(chan Logtimes, hilos)
	terminado := make(chan bool, 1)
	go Writer_logtimes(logfile, canal_logtimes, terminado)
	
	fmt.Println("Logtimes generado")
	
	return canal_logtimes, terminado
}

func Writer_logtimes(logfile string, canal_logtimes chan Logtimes, terminado chan bool) {
	//t0 := time.Now()
	
	f_salida, err := os.Create(logfile)
	if err != nil { log.Fatal(err) }
	defer f_salida.Close()
	
	salida := csv.NewWriter(f_salida)
	if err != nil { log.Fatal(err) }
	
	for info := range canal_logtimes {
		//info.time = time.Since(t0)
		salida.Write(logtimes_to_strings(info))
	}
	salida.Flush()
	terminado <- true
	
	fmt.Println("Cerramos Write_logtimes")
}

func logtimes_to_strings(info Logtimes) []string {
	return []string{
		strconv.FormatInt(info.time.Nanoseconds(), 10),
		strconv.Itoa(info.c),
		strconv.Itoa(info.cantidad),
		info.unidad,
	}
}

/* Utilizamos la Criba de Erastótenes (https://es.wikipedia.org/wiki/Criba_de_Erat%C3%B3stenes)
   para buscar todos los primos hasta el doble del máximo central posible */
func Gen_esprimo(esprimo []bool) {
	// esprimo tiene tamaño cmax*2
	max := len(esprimo)
	
	j := 0;
	for k := 0; k < max; k++ { esprimo[k] = true}
	
	esprimo[0] = false
	esprimo[1] = false
	
	for k := 2; k*k <= max; k++ {
		/* Si ya hemos eliminado este número continuamos */
		if (esprimo[k] == false) { continue }
		
		/* Incrementamos j en i unidades porque queremos tachar todos los múltiplos */
		for j = 2*k; j < max; j = j + k { esprimo[j] = false }
	}
}

func Map_primos(esprimo []bool) map[int]bool {
	//primos := make(map[int]bool, numprimos)
	primos := make(map[int]bool)
	
	for p, val := range esprimo {
		if val {
			primos[p] = true
		}
	}
	return primos
}

func Array_primos(esprimo []bool, numprimos int) []int {
	primos := make([]int, numprimos)
	
	i := 0
	for p, val := range esprimo {
		if val {
			primos[i] = p
			i++
		}
	}
	return primos
}

func Num_primos(esprimo []bool) int {
	cuantos := 0
	for _, val := range esprimo { if val { cuantos++ } }
	return cuantos
}
