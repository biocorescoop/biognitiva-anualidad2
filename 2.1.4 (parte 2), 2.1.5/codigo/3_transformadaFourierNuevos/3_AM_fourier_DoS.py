# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:11:55 2023

@author: usuario
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:02:06 2023

@author: Diego
"""



import sympy as sp
import numpy as np
import pylab as plt
import pandas as pd
import matplotlib.colors as colors
from matplotlib import cm
import os
os.chdir(r"C:\Users\usuario\Desktop\Matrices\Repositorio")

plt.style.use(['dark_background'])
plt.rcParams['figure.figsize'] = [33, 22]
plt.rcParams.update({'font.size': 32})

def par():
    plt.style.use(['dark_background'])
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






#%% Fourier

ptos_max=len(n)
pto_inic=0

attr= (i[pto_inic:ptos_max])
attr=np.nan_to_num(attr)

length = len(attr) # length of our 'time' series
order_series = np.arange(pto_inic, ptos_max)


yhat = []
PSD = []
freqs = []

#for attr in allAttributes[0:7]:
#for attr in n:

yhat = np.fft.fft(attr, length) # Compute the FFT
PSD = yhat * np.conj(yhat) / length # Power Spectral Density (power spectrum) # np.conj is the conjugate of the complex number yhat
freqs = np.fft.fftfreq(np.array(attr).size, 1)

#yhat.append(yhat_temp)
#PSD.append(PSD_temp)    
#freqs.append(freqs_temp)
    
#del yhat_temp, PSD_temp, freqs_temp
    
freq = ((1 / length) * np.arange(length)) # Creates an x-axis of all frequencies for the plot in case the defined one doesn't work
L = np.arange(1, np.floor(length / 2), dtype = 'int') # only plot first half

# =============================================================================
# Now, use peaks in the power spectrum to filter out noise and isolate signal
# ============================================================================
# Let's try with just one for now

#value = 2
PSD_value = PSD
    
# bad_indices = np.where(PSD_value > 2.3eq7)



freq_sort=np.sort(PSD_value)[::-1]
#indices = PSD_value >= freq_sort[100]
indices = PSD_value > 1e6
#indices= (np.abs(freq)<0.1) & (PSD_value>1e5)

PSDclean = PSD_value * indices # zeroes out all indices with smaller Fourier coefficients, keeps only with power greater than specified
yhat_clean = indices * yhat
ffilt = np.fft.ifft(yhat_clean) # Inverse FFT for filtered time signal




# =============================================================================
# And plot
# =============================================================================

fig, axs = plt.subplots(3, 1)

fig.tight_layout(pad = 4) # adjusts spacing of subplots


plt.sca(axs[0])

plt.title('Distribución de k')
plt.xlabel('Progresión del valor', fontsize = 20)
plt.ylabel('k', fontsize = 20)
plt.plot( attr, '.', c = 'firebrick')
plt.legend()



plt.sca(axs[1])
plt.title('Densidad espectral de k')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')
plt.plot(freq, PSD_value, c = 'firebrick', linewidth = 2, label = 'Ruido')
plt.plot(freq, PSDclean, c = 'whitesmoke', linewidth = 1.5, label = 'Señal')
# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.xlim(.370, .380)
#plt.ylim(0,5e6)
#plt.ylim(0,5e5)
#plt.xlim(0,0.05)
#plt.xlim(0.13,0.14)
plt.grid(True)
plt.legend()




plt.sca(axs[2])
plt.title('Señal filtrada')
plt.xlabel('Progresión')
plt.ylabel('n')
plt.scatter(order_series,attr, marker = '.', c = 'firebrick', label = 'Señal ruidosa')
# plt.plot(order_series, ffilt, c = 'whitesmoke', linewidth = .1, label = 'Señal filtrada')
plt.plot(order_series,ffilt, c = 'whitesmoke', marker = '.', label = 'Señal filtrada')
# plt.xlim(freq[L[0]], freq[L[-1]])
plt.grid(True)
plt.legend()
#plt.xlim(500,1000)

plt.show()

#%%

plt.figure()
plt.title('Densidad espectral de k')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')
plt.plot(freq, PSD_value, c = 'firebrick', linewidth = 2, label = 'Ruido')

# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.xlim(.370, .380)
#plt.ylim(0,5e6)
#plt.ylim(0,5e5)
#plt.xlim(0,0.05)
#plt.xlim(0.13,0.14)
plt.grid(True)
plt.legend()



#%% Busco los puntos para los cuales existen las simetrías



# =============================================================================
# eps=1e-1
# lista_fc= []
# for elem in range(3,len(PSD)//2):
#     if (2*np.abs(PSD[elem+1]-PSD[elem-1])/(PSD[elem+1]+PSD[elem-1])< eps)&  (2*np.abs(
#             PSD[elem+2]-PSD[elem-2])/(PSD[elem+2]+PSD[elem-2])< eps) & (2*np.abs(
#                     PSD[elem+3]-PSD[elem-3])/(PSD[elem+3]+PSD[elem-3])< eps):
#         lista_fc.append(elem)
# 
# print(lista_fc)
# =============================================================================


lista_fc=len(PSD)//2*np.arange(1,8)//8

L=len(PSD)//2
plt.figure()
plt.title('Densidad espectral de n')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')
plt.plot(freq[:L], PSD_value[:L], c = 'firebrick', linewidth = 2, label = 'Señal')
plt.plot(freq[np.array(lista_fc)], PSD[lista_fc], 'o',  markersize= 10, c = 'whitesmoke',  label = 'ptos simetría')
# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.xlim(.370, .380)
#plt.ylim(0,5e6)
plt.ylim(0,1e6)
#plt.xlim(0,0.05)
#plt.xlim(0.13,0.14)
plt.grid(True, alpha=0.3)
plt.legend()




#%% Degree of simmetry

# =============================================================================
# DES= \int(S**2)/\int(f**2)
# donde S es la función simétrica respecto del punto x
# =============================================================================

# =============================================================================
# En este script se va a medir el grado de simetría para un conjunto de puntos de
# dimensión variable en torno de los ptosde simetría
# =============================================================================

phi = np.angle(yhat)

lista_fc=len(PSD)//2*np.arange(1,8)//8

dist= len(PSD)//2
eps=0.1
umbral=1e1

DES_fc=[]
DEAS_phi=[]
DES_ln=[]

elem=0
for octav in range(len(lista_fc)):
    
    pto_inic=lista_fc[octav]
    
    DES_ind=[]
    DEAS = []
    DES_ln_i=[]
    
    dist= lista_fc[3]-np.abs(lista_fc[3]-pto_inic)
    
    

    
    for ind in range(1,dist):
        
        f=PSD[pto_inic-ind:pto_inic+ind+1]
        S= (f + f[::-1])/2 #simetrizo la función al sumar f trspuesto
        
        
# =============================================================================
#         Calculo de la integral. Primera aprox, suma de Riemmann 
#         :int(y(x)dx)=\sum base*altura=\sum(y(x))+base. Si base es 1. Int=sum(y(x))
# =============================================================================
        
        int_f=np.sum(f**2)
        int_S=np.sum(S**2)
        DES_ind.append( int_S/int_f)
       
        
       #Vamos a probara a mirar el logaritmo de PSD
       
        f_ln=np.log(f)
        S_ln=(f_ln+f_ln[::-1])/2
        DES_ln_i.append(np.sum(S_ln**2)/np.sum(f_ln**2)) 
        
       
        #Hemos compromado como no existe simetría en phi
# =============================================================================
#         f_phi=phi[pto_inic-ind:pto_inic+ind+1]
#         S_phi = (f_phi - f_phi[::-1])/2 #antisimetrizo la función al restar f trspuesto
#         DEAS.append(np.sum(S_phi**2)/np.sum(f_phi**2)) 
# =============================================================================
        
    DES_fc.append(np.array(DES_ind))
    DES_ln.append(DES_ln_i)    
    #DEAS_phi.append(DEAS)
    
    plt.figure()
    plt.title(f'octavo: {octav +1}' )
    plt.plot(DES_ind, label='simetría PSD')
    #plt.plot(DES_ln_i, label='simetría ln_PSD')
    plt.legend()
    plt.show()
    
        
       





#%% Desv relativa por pto




lista_fc= lista_fc=len(PSD)//2*np.arange(1,8)//8

dist= len(PSD)//32
eps=0.1
umbral=1e1

dif_rel=[]
dif_rel_ln=[]
dif_abs=[]

elem=0
for pto_inic in lista_fc:
    
    dist= lista_fc[3]-np.abs(lista_fc[3]-pto_inic)

    L_dif_rel=[]
    L_dif_rel_ln=[]
    L_dif_abs=[]
    
    for ind in range(dist):
    
       
        L_dif_rel.append( np.abs(PSD[pto_inic+ind]- PSD[pto_inic-ind]
                           ) / np.abs(PSD[pto_inic+ind]+  PSD[pto_inic-ind]))
        
        L_dif_rel_ln.append(np.log(np.abs(PSD[pto_inic+ind]+  PSD[pto_inic-ind]))* np.abs(PSD[pto_inic+ind]- PSD[pto_inic-ind]
                           ) / np.abs(PSD[pto_inic+ind]+  PSD[pto_inic-ind]))
    
        L_dif_abs.append( np.abs(PSD[pto_inic+ind]- PSD[pto_inic-ind]))
        
    
                     
    dif_rel.append(L_dif_rel)
    dif_rel_ln.append(L_dif_rel_ln)
    dif_abs.append(L_dif_abs
                   )
 
# =============================================================================
#     plt.figure()
#     plt.plot(dif_abs[elem])
#     plt.title(f'Dif_abs Dieciseisavo: {1+elem}' )
#     plt.show()
# =============================================================================
    
    plt.figure()
    plt.plot(dif_rel[elem], label= 'Dif. relativa')
    
    plt.title(f'octavo: {octav +1}' )
    plt.plot(DES_fc[elem], label='DoS')
  
    plt.legend()
    plt.show()
    
# =============================================================================
#     plt.figure()
#     plt.plot(dif_rel_ln[elem])
#     plt.title(f'Dif_rel_ln Dieciseisavo: {1+elem}' )
#     plt.show()
# =============================================================================
    
    elem+=1
    
    
    
    
#%% Desv relativa por pto



lista_fc= lista_fc=len(PSD)//2*np.arange(1,8)//8

dist= len(PSD)//32
eps=0.1
umbral=1e1

dif_rel=[]
dif_rel_ln=[]
dif_abs=[]
dif_acum=[]
elem=0

for pto_inic in lista_fc:
    

    
    dist= lista_fc[3]-np.abs(lista_fc[3]-pto_inic)

    L_dif_rel=[]
    L_dif_rel_acum=[]
   
    
    for ind in range(dist):
    
       
        L_dif_rel.append( np.abs(PSD[pto_inic+ind]- PSD[pto_inic-ind]
                           ) / np.abs(PSD[pto_inic+ind]+  PSD[pto_inic-ind]))
        L_dif_rel_acum.append(np.sum(L_dif_rel)/len(L_dif_rel))
        
       
        
    
                     
    dif_rel.append(L_dif_rel)
    dif_rel_ln.append(L_dif_rel_ln)
    dif_abs.append(L_dif_abs)
    dif_acum.append(L_dif_rel_acum)
                   
 
# =============================================================================
#     plt.figure()
#     plt.plot(dif_abs[elem])
#     plt.title(f'Dif_abs Dieciseisavo: {1+elem}' )
#     plt.show()
# =============================================================================
    elem1=elem+1
    plt.figure()
    plt.plot(1-np.array(dif_acum[elem]), label= '1 - Dif. relativa')
    
    plt.title(f'Punto de simetría: {elem +1}' )
    plt.plot(DES_fc[elem], label='DoS')
  
    plt.legend(loc='lower left')
    plt.savefig("3_DoS_{elem1}.png".format(elem1=elem1))
    plt.show()

    
    
# =============================================================================
#     plt.figure()
#     plt.plot(dif_rel_ln[elem])
#     plt.title(f'Dif_rel_ln Dieciseisavo: {1+elem}' )
#     plt.show()
# =============================================================================
    
    elem+=1




#%% Busco para cada punto, el intervalo en el que sigue existiendo la siemtría a través
#de la desviacion relativa

#Recorro los puntos q he encontrado

#longitud del intervalo
Long_fc=[]

lista_fc= lista_fc=len(PSD)//2*np.arange(1,7)//8

eps=0.1
umbral=1e1

for pto in lista_fc:
    
    ind=1
    
    #Cuento la cantidad de puntos que puedo avanzar tal que la distancia relativa entre
    # puntos equidistantes sea menor que eps.
    
    #Además doy la posilidad de que un punto se salga de la estadística, 
    #evaluando el siguiente, al introducir el operador or
    
    #He introducido otro criterio que es que el pico sea suficiéntemente grande
    
    while (2*np.abs(PSD[pto+ind]-PSD[pto-ind])/(
            PSD[pto+ind]+PSD[pto-ind])< eps) or (2*np.abs(
                PSD[pto+ind+1]-PSD[pto-ind-1])/(PSD[pto+ind+1]+PSD[pto-ind-1]
                ))< eps or (PSD[pto+ind]+PSD[pto-ind])/2<umbral:
        ind+=1
        
    Long_fc.append(ind)   
    
    
Ptos_fc=[]

for elem in range(len(Long_fc)): Ptos_fc.append(np.arange(lista_fc[elem]-Long_fc[elem],(lista_fc[elem]+Long_fc[elem]+1)))

Ptos_fc=np.concatenate( Ptos_fc, axis=0)  

plt.figure()
plt.title('Densidad espectral de k')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')
plt.plot(freq[1:], PSD_value[1:], c = 'firebrick', linewidth = 2, label = 'Señal')
plt.plot(freq[np.array(Ptos_fc)], PSD[Ptos_fc], '.',  markersize= 3, c = 'whitesmoke',  label = 'ptos simetría')
#plt.yscale('log')
# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.xlim(.370, .380)
#plt.ylim(0,5e6)
#plt.ylim(0,5e5)
#plt.xlim(0,0.05)
#plt.xlim(0.13,0.14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()



#%% Estudio la proporcion entre los puntos


# =============================================================================
# 
# lista_fc=len(PSD)//2*np.arange(1,7)//8
# 
# 
# 
# #Recorro los puntos q he encontrado
# 
# #longitud del intervalo
# Long_fc=[]
# 
# eps=0.3
# umbral=1e5
# 
# 
# pto_inic=lista_fc[1]
# 
# dif_rel=[]
# size_peak=[]
# 
# for ind in range(len(PSD)//4):
#     dif_rel.append( np.abs(PSD[pto_inic+ind]-PSD[pto_inic-ind])/(
#             PSD[pto_inic+ind]+PSD[pto_inic-ind]))
#     size_peak.append((PSD[pto_inic+ind]+PSD[pto_inic-ind])/2)
# 
# size_peak=np.array(size_peak)    
# 
# 
# ax2 = plt.axes()
# 
# fig=plt.figure()
# plt.scatter(range(len(dif_rel)), dif_rel,  c=  size_peak, s=5, norm=colors.LogNorm(vmax=1e6))
# plt.colorbar()
# 
# 
# 
# =============================================================================

# =============================================================================
# #%% 
# 
# lista_fc=len(PSD)//2*np.arange(1,8)//8
#  
# PSD2=np.copy(PSD)
# PSD=PSD2
# #elijo el octavo en el que me muevo 1º, 2º, etc.
# octavo=4
# 
# pto_inic=lista_fc[octavo-1] 
# 
# #el tamaño del intervalo lo da la distancia entre el pto inici y el 0,
# #para conisderara solo la mitad positivo me quedo con PSD//2.
# 
# prop= np.arange((2*(len(PSD)//2)*(4-np.abs(4-octavo))/8), dtype='float64')
# size_peak=[]
# 
# #quito losptos q son demasiado pequeños (1e-25)
# #PSD [np.where(PSD<1e-7)] = 1e-7
# PSD=np.real(PSD)
# 
# dif_prop=[]
# dif_prop_rel = []
# 
# 
# for ind in range(len(prop)//2):
#     #como el origen es el 0, hay que restar
#     
#     
#     prop[len(prop)//2+ind]= PSD[pto_inic+ind]/PSD[pto_inic+ind-1]
#     prop[len(prop)//2-ind]= PSD[pto_inic-ind]/PSD[pto_inic-ind+1]
#     
#     dif_prop_rel.append( np.abs(PSD[pto_inic+ind]/PSD[pto_inic+ind-1]- 
#                             PSD[pto_inic-ind]/PSD[pto_inic-ind+1]) / np.abs(PSD[pto_inic+ind]/PSD[pto_inic+ind-1]+ 
#                                                     PSD[pto_inic-ind]/PSD[pto_inic-ind+1]))
#                    
#     dif_prop.append( np.abs(PSD[pto_inic+ind]/PSD[pto_inic+ind-1]- 
#                            PSD[pto_inic-ind]/PSD[pto_inic-ind+1]) )
#                                                                             
#                                                                             
#     size_peak.append((PSD[pto_inic+ind]+PSD[pto_inic-ind])/2)
# 
# size_peak=np.array(size_peak)    
# 
# 
# 
# 
# plt.figure()
# plt.plot(freqs[:len(prop)], prop)
# #plt.ylim(0,5)
# #plt.xlim(2,len(prop-2))
# plt.title('proporcion')
# plt.show()
# 
# plt.figure()
# plt.plot(dif_prop)
# plt.title('dif_prop')
# plt.show()
# 
# plt.figure()
# plt.plot(dif_prop_rel)
# plt.title('dif_prop rel')
# plt.show()
# #%%
# 
# PSD=prop
# prop=np.arange(len(PSD))
# pto_inic=len(PSD)//2
# PSD[np.where(PSD<1e-10)]=1e-10
# 
# 
# for ind in range(len(prop)//2):
#     #como el origen es el 0, hay que restar
#     
#     
#     prop[len(prop)//2+ind]= PSD[pto_inic+ind]/PSD[pto_inic+ind-1]
#     prop[len(prop)//2-ind]= PSD[pto_inic-ind]/PSD[pto_inic-ind+1]
#     
#     dif_prop.append( np.abs(PSD[pto_inic+ind]/PSD[pto_inic+ind-1]- 
#                             PSD[pto_inic-ind]/PSD[pto_inic-ind+1])
#                     /(PSD[pto_inic+ind]/PSD[pto_inic+ind-1]- 
#                                             PSD[pto_inic-ind]/PSD[pto_inic-ind+1]))
# 
# 
# plt.figure()
# plt.plot(freqs[:len(prop)], prop)
# #plt.ylim(0,1e5)
# #plt.xlim(2,len(prop-2))
# plt.show()
# #%%
# 
# 
# 
# 
# # =============================================================================
# # Es una forma de visualizar la relación entre tamaño y dif rel
# # al elevar la dif rel al cuadrado le doy más importancia, lo q me permite tener una idea más adecauada
# # del intervalo hasta el cual la incertidumbre es significativa
# # =============================================================================
# 
# # =============================================================================
# # Todo me lleva a suponer que es necesario considerar de alguna forma la media y
# # desviación en los puntos para hacer una estimación más razonable del límite 
# # a partir del cual no considerara la simetría
# # =============================================================================
# 
# 
# 
# 
# 
# plt.plot(size_peak*np.array(dif_rel)**2)
# plt.show()
# 
# =============================================================================

#%%


