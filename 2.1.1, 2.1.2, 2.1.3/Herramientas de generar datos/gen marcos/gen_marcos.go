package main

import (
	"fmt"
	"os"
	//"io"
	"log"
	"encoding/csv"
	"strconv"
	"matanid"
	//"sort"
	"time"
)


type Logtimes struct {
	c int
	cantidad int // -1 es que comienza la función
	time time.Duration
	unidad string
}

var canal_logtimes chan Logtimes
var logtimes bool
var t0 time.Time
var reducir bool

var esprimo []bool
var cmax, cmin, n int

func main() {
	t0 = time.Now()
	var filename string
	var logfile string
	var logterminado chan bool
	
	genfilas := false
	secuencial := false
	reducir = true
		
	for i := 0; i < len(os.Args); i++ {
		switch os.Args[i] {
			case "-cmax":
				cmax, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-cmin":
				cmin, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "-o" :
				filename = os.Args[i+1]
				i++
			case "-n" :
				n, _ = strconv.Atoi(os.Args[i+1])
				i++
			case "--genfilas" :
				genfilas = true
			case "--logtimes" :
				logtimes = true
			case "--secuencial" :
				secuencial = true
			case "--noreducir" :
				reducir = false
		}
	}
	
	if n == 0 { n = 2 }
	
	if len(filename) == 0 {
		if !genfilas {
			filename = fmt.Sprintf("marcos_%dx%d_%d-%d.csv", 2*n+1, 2*n+1, cmin, cmax)
		} else {
			filename = fmt.Sprintf("filas_%dx%d_%d-%d.csv", 2*n+1, 2*n+1, cmin, cmax)
		}
	}
	if logtimes {
		if secuencial {
			logfile = fmt.Sprintf("logtimes_secuencial_%dx%d_%d-%d.csv", 2*n+1, 2*n+1, cmin, cmax)
		} else {
			logfile = fmt.Sprintf("logtimes_%dx%d_%d-%d.csv", 2*n+1, 2*n+1, cmin, cmax)
		}
		canal_logtimes = make(chan Logtimes, 5)
		logterminado = make(chan bool, 1)
	}
	
	esprimo = make([]bool, 2*cmax)
	matanid.Gen_esprimo(esprimo)
	numprimos := matanid.Num_primos(esprimo)
	primos := matanid.Array_primos(esprimo, numprimos)
	
	if logtimes { go Write_logtimes(logfile, canal_logtimes, logterminado) }
	canal_matrices := make(chan []int, 5)
	terminado := make(chan bool)
	
	if !secuencial {
		canal_filas := make(chan []int, 5)
		canal_pares := make(chan []int, 5)
		
		go Gen_pares(canal_pares, primos)
		go Gen_filas(canal_pares, canal_filas)
		if !genfilas {
			go Gen_matrices(canal_filas, canal_matrices)
			go Recibe_matrices(filename, canal_matrices, terminado)
		} else {
			go Recibe_matrices(filename, canal_filas, terminado)
		}
	} else {
		var buffilas matanid.Mibuffer
		buffilas.Inicializar(2*n+1)
		go Recibe_matrices(filename, canal_matrices, terminado)
		
		for _, c := range primos {
			if c < cmin { continue } else if c > cmax { break }
			
			pares := gen_pares_p(c, primos)
			
			if len(pares) <= 4*n { continue }
			
			canal_pares := make(chan []int, 1)
			canal_pares <- pares
			close(canal_pares)
			
			canal_filas := make(chan []int, 1)
			go Gen_filas(canal_pares, canal_filas)
			
			buffilas.Vaciar()
			for fila := range canal_filas { buffilas.Add(fila[1:]) }
			
			if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : -1, time : time.Since(t0), unidad : "matrices"} }
			num_filas := buffilas.Elementos()
			num_matrices := 0
			
			for i := 0; i < num_filas; i++ {
				num_matrices += Matrices_con_la_fila(buffilas, i, canal_matrices, c)
			}
			
			if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : num_matrices, time : time.Since(t0), unidad : "matrices"} }
		}
		close(canal_matrices)
	}
	
	<- terminado
	close(canal_logtimes)
	
	if logtimes { <- logterminado }
}

func Gen_pares(canal_pares chan []int, primos []int) {
	for _, c := range primos {
		if c < cmin { continue } else if c > cmax { break }
		
		pares := gen_pares_p(c, primos)
		
		if len(pares) >= 4*n { canal_pares <- pares }
	}
	close(canal_pares)
	
	fmt.Println("Cerramos Gen_pares")
}

func gen_pares_p(c int, primos []int) []int {
	if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : -1, time : time.Since(t0), unidad : "pares"} }
	
	pares := []int{c}
	for _, p := range primos {
		if p >= c { break } // p debe ser menor que c para no repetir
		if (c - p) % 3 != 0 { continue }
		
		if esprimo[2*c - p] { pares = append(pares, p) }
	}
	
	if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : len(pares), time : time.Since(t0), unidad : "pares"} }
	
	return pares
}

func Gen_filas(canal_pares chan []int, canal_filas chan []int) {
	tam := 2*n+1
	pos := make([]int, tam)
	signo := make([]bool, tam)
	fila := make([]int, tam)
	sum := make([]int, tam)
	
	for pares := range canal_pares {
		c := pares[0]
		if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : -1, time : time.Since(t0), unidad : "filas"} }
		
		pares = pares[1:]
		numpares := len(pares)
		numfilas := 0
		fmt.Println(numpares, "pares con el primo", c)
		fmt.Println(pares)
		
		pos[0] = 0
		signo[0] = false
		fila[0] = pares[0]
		sum[0] = pares[0]
		pos[1] = 0
		signo[1] = true
		
		for i := 1; i >= 0; {
			if i == 2*n {
				fila[i] = tam*c - sum[i-1]
				par := 2*c-fila[i]
				if par > 0 { if esprimo[fila[i]] && esprimo[par] { //{ for _, p := range pares[pos[i-1]+1:] { if p == fila[i] || p == par {
					canal_filas <- append([]int{c}, fila...)
					numfilas++
					break
				} }
				i--
				continue
			}
			
			// avanzamos posición en signo o en par
			if signo[i] || i == 0 { // si es el primer elemento no consideramos su par para no repetir filas
				pos[i]++
				if pos[i] >= numpares { i--; continue }
				signo[i] = false
				fila[i] = pares[pos[i]]
			} else {
				fila[i] = 2*c - fila[i]
				signo[i] = true
			}
			
			// calculamos sum[i]
			if i > 0 { sum[i] = sum[i-1] + fila[i] } else { sum[0] = fila[i] }
			
			if i > 1 {
				if sum[i] > tam*c {
					signo[i] = true // si ya se ha pasao de tamaño no vamos a coger su par que es mayor que el xd
					continue
				}
				restante := (tam*c-sum[i])/(tam-i-1)
				if restante > 2*c {
					// si debe haber elementos por completar mayores de lo que los pares lo permiten,
					// retroceder hasta el último elemento p > 2*c
					for signo[i] && i > 0 { i-- }
					continue
				}
			}
			
			pos[i+1] = pos[i]
			i++
			signo[i] = true
		}
		if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : numfilas, time : time.Since(t0), unidad : "filas"} }
	}
	close(canal_filas)
	
	fmt.Println("Cerramos Gen_filas")
}

func Gen_matrices(canal_filas chan []int, canal_matrices chan []int) {
	var buffilas matanid.Mibuffer
		
	buffilas.Inicializar(2*n+1)
	c := 0
	num_matrices := 0
	
	for fila := range canal_filas {
		if c != fila[0] {
			if num_matrices > 0 {
				fmt.Println(buffilas.Elementos(), "filas con el primo", c, "\n", num_matrices, "marcos con el primo", c)
				if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : num_matrices, time : time.Since(t0), unidad : "matrices"} }
			}
			
			buffilas.Vaciar()
			c = fila[0]
			num_matrices = 0
			if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : -1, time : time.Since(t0), unidad : "matrices"} }
		}
		
		num_fila := buffilas.Add(fila[1:])
		if num_fila == 0 { continue }
		
		num_matrices += Matrices_con_la_fila(buffilas, num_fila, canal_matrices, c)
	}
	
	fmt.Println(buffilas.Elementos(), "filas con el primo", c, "\n", num_matrices, "marcos con el primo", c)
	if logtimes { canal_logtimes <- Logtimes{c : c, cantidad : num_matrices, time : time.Since(t0), unidad : "matrices"} }

	close(canal_matrices)
	fmt.Println("Cerramos Gen_matrices")
}

func Matrices_con_la_fila(buffilas matanid.Mibuffer, numfila int, canal_matrices chan []int, c int) int {
	num_matrices := 0
	fila := buffilas.Get(numfila)
	
	for i := 0; i < numfila; i++ {
		otrafila := buffilas.Get(i)
		
		matriz := filas_to_matriz(fila, otrafila, c)
		if matriz != nil {
			canal_matrices <- matriz
			num_matrices++
		}
	}
	return num_matrices
}

func filas_to_matriz(fila []int, otrafila []int, c int) []int{
	var esquina, otraesquina [2]int
	esquina[0] = -1
	otraesquina[0] = -1
	
	for k1, val1 := range fila { for k2, val2 := range otrafila {
		if val1 == val2 {
			if esquina[0] != -1 { return nil }
			esquina[0] = k1
			esquina[1] = k2
		} else if val1 == 2*c - val2 {
			if otraesquina[0] != -1 || esquina[0] == k1 { return nil }
			otraesquina[0] = k1
			otraesquina[1] = k2
		}
	}}
	
	if esquina[0] == -1 || otraesquina[0] == -1 { return nil }
	
	return Rellenar_matriz(c, fila, otrafila, esquina, otraesquina)
}

func Rellenar_matriz(c int, fila []int, otrafila []int, esquina [2]int, otraesquina [2]int) []int {
	matriz := make([]int, 8*n+1)
	matriz[0] = c
	matriz[1] = fila[esquina[0]]
	matriz[8*n] = 2*c - otrafila[esquina[1]]
	matriz[2*n+1] = fila[otraesquina[0]]
	matriz[6*n] = otrafila[otraesquina[1]]
	j := 2
	for k := 0; k < 2*n+1; k++ {
		if k == esquina[0] || k == otraesquina[0] { continue }
		matriz[j] = fila[k]
		matriz[6*n-1+j] = 2*c - fila[k]
		j++
	}
	j = 2*n+2
	for k := 0; k < 2*n+1; k++ {
		if k == esquina[1] || k == otraesquina[1] { continue }
		matriz[j] = otrafila[k]
		matriz[j+1] = 2*c - otrafila[k]
		j += 2
	}
	matanid.Ordenar_marco(matriz[1:], n)
	return matriz
}

func Recibe_matrices(filename string, canal_matrices chan []int, terminado chan bool) {
	f_salida, err := os.Create(filename)
	if err != nil { log.Fatal(err) }
	defer f_salida.Close()
	
	salida := csv.NewWriter(f_salida)
	if err != nil { log.Fatal(err) }
	
	for matriz := range canal_matrices {
		if reducir {
			salida.Write(matanid.Array_to_strings(matriz[:4*n+1]))
		} else {
			salida.Write(matanid.Array_to_strings(matriz))
		}
	}
	salida.Flush()
	terminado <- true
}

func Write_logtimes(logfile string, canal_logtimes chan Logtimes, terminado chan bool) {
	f_salida, err := os.Create(logfile)
	if err != nil { log.Fatal(err) }
	defer f_salida.Close()
	
	salida := csv.NewWriter(f_salida)
	if err != nil { log.Fatal(err) }
	
	for info := range canal_logtimes {
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
