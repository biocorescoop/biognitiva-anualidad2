# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:28:54 2023

@author: usuario
"""

import sympy as sp
import numpy as np
import pylab as plt
import pandas as pd
import matplotlib.colors as colors
from matplotlib import cm
import os
import copy as cp

os.chdir(r"C:\Users\usuario\Desktop\Matrices")
#plt.style.use(['dark_background'])
plt.rcParams['figure.figsize'] = [33, 22]
plt.rcParams.update({'font.size': 32})

#%%
data=pd.read_excel(r'C:/Users/usuario/Desktop/Matrices/esp_c_plano_tc.xlsx')

#data_g=data.loc[data['Grupo_de_transformaciones']=='e']

nijk = data[['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]', 'k = [-200,200]']].to_numpy()

#nijk=nijk[:5000,:]
n=nijk[:,0]
i=nijk[:,1]
j=nijk[:,2]
k=nijk[:,3]
n15=n


#Recuerda q no tengo n, si no 15n
a=15*n/15+i
x=4*n/15+j
y=11*n/15+k
t=data['t']
central=10*x-5*y




#%%

#Recuerdaq n es en realidad 15n y q no he elegido un eje perpendicular, pero no cambia gran cosa

u=n+i
v=i

plt.plot(u,v, '.')
plt.show()


#%% VAmos a hacer el análisis 2D de una sale matriz

data=pd.read_excel(r'C:/Users/usuario/Desktop/Matrices/esp_c_plano_tc.xlsx')

M1=data.iloc[:,:]

nijk1 = (M1[['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]', 'k = [-200,200]']].to_numpy()).astype(int)

#nijk=nijk[:5000,:]


vecto=np.array([-15,15,4,11])

array_t=np.arange(-30,30)
#array_t=np.array([0])

nijk_extend=nijk1[:8,:]
for tp in array_t:
    nijk_t=nijk1 + vecto*tp
    nijk_extend=np.concatenate((nijk_extend,nijk_t), axis=0)
    
print(nijk_extend.shape)


nijk_extend=nijk_extend[8:,:]



n1=nijk_extend[:,0]
i1=nijk_extend[:,1]
j1=nijk_extend[:,2]
k1=nijk_extend[:,3]

#del nijk_extend, nijk_t, vecto, nijk1, M1, data, tp, array_t

#%%



plt.plot(n1+i1,i1, '.')
plt.title('a frente i', fontsize=45)
plt.xlabel('a', fontsize=40)
plt.ylabel('i', fontsize=40)



#Esta es la "pantalla" original

ninic=1000
iinic=200
nrange=np.linspace(-ninic,ninic, 100)
irange=np.linspace(-iinic,iinic, 100 )
# =============================================================================
# plt.plot(np.tile(ninic, 100), irange, 'r')
# plt.plot(np.tile(-ninic, 100), irange, 'r')
# plt.plot(nrange, np.tile(iinic, 100), 'r')
# plt.plot(nrange, np.tile(-iinic, 100), 'r')
# =============================================================================
#este es el espectro original 


plt.show()

#%% Fourier ND


#fft.fftn(a, s=None, axes=None, norm=None)[source]




#Primer paso) convertir la imagen de n fernte a i en un array dos dimensioinal
# en el que los ptos se reprentan con un 1. Para ello primero calculo  la 
#diferencia entre el mayor valor de i y el menor valor de i; y hago lo mismo
#para n. Acto seguido genero una matriz de 0 cuadrada cuyo tamaño viene dado 
#por la mayor diferencia. 



def Fouriernd(input_, names, Umbral=3):
    
    
    #Le meto las varaibles y los nombre de las variables y me devuelve
    #la transformada de Fourier y la inversa
    
    
    
    #input_ es una lista de arrays conteniendo todos los datos
    r=input_
    print(len(r))
    dimension=len(input_)
    
    r_range=[]
    r0=[]
    for d in range(dimension):
        r_range.append(np.amax(r[d])-np.amin(r[d]) +1)
        print(r_range)
        #desplaza por datos originales para que todos los ptos sean >0
        r0.append(r[d]-np.amin(r[d]))
        
        

    
    
    #Creo una matriz cuadrada ded dimensiones
   
    Matr=np.zeros(r_range, dtype='int')
    print(r_range, Matr.shape)
    
   
    
    # Recorro los valores de n e i, asignándole el valor 1 a la matriz para los
    #índices en los que existe n e i
    indices_m=[]
    for p in range(len(r[0])):
        for d in range(dimension): 
            indices_m.append(r0[d][p])

        Matr[tuple(indices_m)]=1
        
        indices_m=[]
    
    #print(Matr)
    

    
    
    #Hago la transformada de Fourier
    furn=np.fft.fftn(Matr)
    
    #return Matr, furn
    
    
    #Selección de los picos obtenidos
    
    #Calculo la media y la desviación estándar
    PSDn=furn*np.conj(furn)
    media=np.mean(PSDn)
    desv=np.std(PSDn)
    
    
    #Sustituyo los valores por debajo de 2σ por la media (q creo q es 0)
    furn_fil=np.where((PSDn<Umbral*desv))
    PSDnf=cp.deepcopy(PSDn)
    PSDnf[furn_fil]= 0
    
    #Me da la senación de que la selección más razonable es  apartir de 3σ
    
    
    #del PSD2, media, desv, fur2_fil
    
    if len(r)==2:
        
        
        
        fig, axs = plt.subplots(1,2)

        #fig.tight_layout(pad = 4) # adjusts spacing of subplots
        
        #Ploteo el fourier normal
        
        plt.sca(axs[0])
        c=plt.imshow(np.real(PSDn), aspect='auto', norm=colors.LogNorm(), 
                           cmap='gist_rainbow')
        plt.xlabel('')
        plt.ylabel('v')
        plt.title('Transformada de Fourier')
        
        
        
        plt.sca(axs[1])
        
        #norm=colors.Normalize(vmin=-100, vmax=100)
        
        #Ploteo el fourier filtrado
        c=plt.imshow(np.real(PSDnf), aspect='auto', norm=colors.Normalize(vmin=-100, vmax=100),
                           cmap='gist_rainbow')
        plt.xlabel(names[0])
        plt.ylabel(names[1])
        plt.title(f'Transformada de Fourier para un umbral de {Umbral} σ' ) 
        #No entiendo por quéno me escribe parte decimal, pero bueno
        
        plt.show()
        
        
    if len(r)==8:
                
        fig, ax4 = plt.subplots(subplot_kw={"projection": "3d"})
        
        #ind=data['Indice'].to_numpy()
        surf=ax4.plot_surface(PSDnf, cmap='gist_rainbow', s=5) #s da el tamaño
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
        
        ax4.set_title('4 variables')
        ax4.set_xlabel('i')
        ax4.set_ylabel('j')
        ax4.set_zlabel('k')
        ax4.view_init(elev=30, azim=30)
        
        plt.show()
        
    furnf=cp.deepcopy(furn)
    furnf[furn_fil]=0
        
    return  furnf, Matr, furn, PSDnf






#%%

u=n1+i1
#v es 15*v
v= i1

array_dat=[u,v.astype(int)]
#del n1, i1, k1,
nombres=['u','v']

ff1 =Fouriernd(array_dat, nombres)





#%%3. Fourier2d inv n, i
fur2f=ff1[0]
Matr=ff1[1]
#Hago la transformada inversa
ifft2_=np.fft.ifft2(fur2f)

desvi=np.std(ifft2_)

#Transformo la señal en obtenida en unna función binaria (como la entrada)
ifft2_ampli=np.copy((ifft2_))
ifft2_ampli[np.where(ifft2_ampli>4*desvi)]=1
ifft2_ampli[np.where(ifft2_ampli<4*desvi)]=0


#%%

#Represento los datos orignales
Matr_uno=np.where(Matr==1)
iff_uno=np.where(np.real(ifft2_ampli)==1)


plt.scatter(iff_uno[0], iff_uno[1], s=1, label='Transformada Fourier')
plt.scatter(Matr_uno[0], Matr_uno[1], s=1, label='Datos originales')

plt.legend()

plt.xlabel('a')
plt.ylabel('i')
plt.title('Tranformada de Fourier inversa')

#plt.xlim(500,700)
#plt.ylim(550,400)



plt.show()


ptos_M=np.where(Matr==1)
ptos_pred=np.copy(ifft2_ampli[ptos_M])

fallo=np.where(ptos_pred!=1)
ratio=len(fallo[0])/ptos_pred.shape[0]
print(ratio, len(fallo[0]), np.std(ifft2_))

#2 sigma
#cogiendo umbral 0.05 pillo 2 fallos
#cogiendo umbral 0.1 pillo ~ 20 fallos
#std es 0.04


#3 sigma y 0.1: 111
#Hay un pto clave en la elección del umbral a la hora de recoger los ptos. En ppio, nno creo que introduzca mucho ruido

#%%

dif2= np.real(ifft2_ampli)-Matr

unos=np.where(dif2==1)
munos=np.where(dif2==-1)


plt.title('Diferencia señal original y recosntruida')
plt.scatter(munos[0], munos[1], s=3, label='ptos_fallados')
plt.scatter(unos[0], unos[1], s=3, label='ptos_nuevos')
plt.legend()
plt.show()



#%%


    

freqs=[]
freqs_v=[]
fila_v=[]
pto_inic=[]

Matr_fil2=np.real(ifft2_ampli)

Matr_fil=Matr_fil2[100:Matr_fil2.shape[0]-100, :]


for fil in range(Matr_fil.shape[0]):
    

    Fila=Matr_fil[fil, :]   
    ptos_nz=np.nonzero(Fila)
    ptos_nz=ptos_nz[0] 
    
    
    
    if ptos_nz.size>0:
        
        dif=np.zeros(len(ptos_nz)-1)
    
        #diferencia entre puntos sucesivos
        for val in range(len(ptos_nz)-1): dif[val]=ptos_nz[val+1]-ptos_nz[val]
        
        
        #Rango q escojo
        fraq=15
        
        #escojo el 80% central de la distrib
        dif_selec=dif[len(dif)//fraq: len(dif)*(1-1//fraq)]
        print(dif_selec)
        
        if dif_selec.size>40:
    
            
            
            #Programita que me encuentra las frecuencias de está separación
            num_elem=1
            var=-1
            while var !=0:
                print('num_elem', num_elem, var)
                freq=dif_selec[:num_elem]
                divisiones=len(dif_selec)//num_elem
                for valor in range(divisiones):
                    #print(dif_selec[valor:valor+num_elem])
                    var=0
                    print('valor', valor)
                    if np.sum(dif_selec[valor:valor+num_elem]-freq)!=0:
                        var=-1
                        num_elem+=1
                        break
                    
            #el último elemento me da el pto inicial
            freqs_v.append(freq)
            fila_v.append(fil+100)
            pto_inic.append( ptos_nz[len(dif)//fraq] )

                



#%% Ahora compruebo qué tal me reconstruye la distrib de ptos

#tengo 1) los valores de u 3) el pto en el que empieza cada frecuencia
#puedo generar un vector de puntos
ptos_tot=60 # Recorro 30*ptos_tot valores
ptos_esc=np.arange(150,250)


Matr_recr= np.zeros((Matr).shape)
for v_p in ptos_esc:
    u_vec=[pto_inic[v_p]]
    v_val=fila_v[v_p]
    d_vec=np.tile(freqs_v[v_p],ptos_tot )
    for elem in range(len(d_vec)): u_vec.append(u_vec[elem]+d_vec[elem])
    #plt.plot(np.tile(v_val, len(u_vec)), u_vec, '.' 'b')
    Matr_recr[v_val, np.array(u_vec).astype(int)]=1

#%%
M_runo= np.where(Matr_recr==1)

plt.scatter(iff_uno[0], iff_uno[1], s=30, label='Transformada Fourier')
plt.scatter(M_runo[0], M_runo[1], s=30, label='Frecuencias')
plt.legend()
#plt.xlim(1000,1500)


#plt.ylim(1500,2000)

#plt.xlim(700, 2600)

plt.show()


#%%

dif2= Matr_recr-Matr

unos=np.where(dif2==1)
munos=np.where(dif2==-1)


plt.scatter(munos[0], munos[1], s=3, label='ptos_fallados')
plt.scatter(unos[0], unos[1], s=3, label='ptos_nuevos')
plt.legend()
plt.xlim(1000,1700)
#plt.ylim(900,1000)
plt.show()


#%%            

plt.scatter(iff_uno[0], iff_uno[1], s=1, label='Transformada Fourier')
#plt.scatter(Matr_uno[0], Matr_uno[1], s=1, label='Datos originales')

plt.legend()

plt.xlabel('n')
plt.ylabel('i')
plt.title('n frente a i')

plt.xlim(1000,1700)
#plt.ylim(550,400)

plt.show()






#%% Freqs en v manteniendo u cte /horizontales)


    

freqs=[]
freqs_v=[]
fila_v=[]
pto_inic=[]

Matr_fil2=np.real(ifft2_ampli)

Matr_fil=Matr_fil2[:,100:Matr_fil2.shape[1]-100]


for fil in range(Matr_fil.shape[1]):
    

    Fila=Matr_fil[:, fil]   
    ptos_nz=np.nonzero(Fila)
    ptos_nz=ptos_nz[0] 
    
    
    
    if ptos_nz.size>0:
        
        dif=np.zeros(len(ptos_nz)-1)
    
        #diferencia entre puntos sucesivos
        for val in range(len(ptos_nz)-1): dif[val]=ptos_nz[val+1]-ptos_nz[val]
        
        #escojo el 80% central de la distrib
        dif_selec=dif[len(dif)//20: len(dif)*(1-1//20)]
        print(dif_selec)
        
        if dif_selec.size>40:
    
            
            
            #Programita que me encuentra las frecuencias de está separación
            num_elem=1
            var=-1
            while var !=0:
                print('num_elem', num_elem, var)
                freq=dif_selec[:num_elem]
                divisiones=len(dif_selec)//num_elem
                for valor in range(divisiones):
                    #print(dif_selec[valor:valor+num_elem])
                    var=0
                    print('valor', valor)
                    if np.sum(dif_selec[valor:valor+num_elem]-freq)!=0:
                        var=-1
                        num_elem+=1
                        break
                    
            #el último elemento me da el pto inicial
            freqs_v.append(freq)
            fila_v.append(fil+100)
            pto_inic.append( ptos_nz[len(dif)//10] )

                

            
    
    

            


