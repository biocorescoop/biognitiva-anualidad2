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


#%%Funciones
def transformacionM (M,gt):
    
    
    Mgt=sp.Matrix(np.zeros([3,3]))
    if gt=='mg': 
        for l in range(np.shape(M)[0]):
            Mgt[:,l]=M[2-l,:].T
            
    if gt=='g2': 
        for l in range(np.shape(M)[0]):
            Mgt[:,l]=M[:,2-l][::-1]
            
    if gt=='g': 
        for l in range(np.shape(M)[0]):
            Mgt[:,l]=M[l,:][::-1]
    
    return Mgt



def calculo_sigma (Mvar, M, var):
    ecs=sp.Matrix((Mvar.T-M)[1:3]) #como solo tengo q calcular 2 var, me quedo con 2 ecs
    ecs=ecs.subs(list(zip([pn,pi],var[:2]))) #sustituyo n e i por su valor
    result=sp.solve(ecs, (pj,pk)) #solve  ecuaciones
    valores=list(result.values())
    val=np.zeros(4, float)
    val[0]=var[0]
    val[0:2]=var[0:2]
    val[2:4]=valores
    return val
    
    
def calculo_g (Mvar, M):
    eps=1e-5
    ecs=Mvar-M
#solve(f, [x, y])
#result=sp.solve(ecs[1],ecs[3], ecs[4], ecs[0], ecs[2], ecs[6], ecs[5], ecs[7], ecs[8], (pk,pn,pj,pi)) #solve  ecuaciones
    result=sp.solve(ecs[1:4], (pn,pj,pk,pi)) #solve  ecuaciones
# Uso solo 4 ecuaciones, no necesito más
#me devuelve pn,pk y pj en funcion de pi

    ivec=[1,2,4,7,8,11,13,14] #creo un array con los valores posibles de i

    valores=list(result.values())
    val=np.array([0.0,0.0,0.0, 0.0],float )
    for m in ivec:
        valk=valores[2].subs(pi,m)
        if abs(valk%1)<eps or (1-abs(valk%1))<eps:
            break
        
    val[0]=valores[0].subs(pi,m) #15n
    val[1]=m #i
    val[3]=valk #k
    val[2]=valores[1].subs(pi,m) #j

    return val     
        
# =============================================================================
#         v=valores
#         # Python for loop in one line
#         c=1
#         for v in valores :
#             val[0]=m
#             val[c]=v.subs(pi,m)
#             c+=1
# =============================================================================
    
    
    
    
   




#%% 1. Matriz anidada
x=sp.Symbol('x')
y=sp.Symbol('y')
a=sp.Symbol('a')

matr=sp.Matrix([[10*x-5*y-a , 8*x-7*y+2*a , 12*x-3*y-a] , [12*x-3*y , 10*x-5*y , 8*x-7*y] , [8*x-7*y+a , 12*x-3*y-2*a , 10*x-5*y+a]])

sn=sp.Symbol('15n') #meto direcatemnete el 15 en el valor de n 
si=sp.Symbol('i')
sj=sp.Symbol('j')
sk=sp.Symbol('k')

matr_2=matr.subs(list(zip([a,x,y],[15*sn/15+si,4*sn/15+sj,11*sn/15+sk])))


#a11,a12,a13,a21,a22,a23,a31,a32,a33 = sp.symbols('a11, a12, a13, a21, a22, a23, a31, a32, a33')
#M=sp.Matrix([[a11,a12,a13], [a21,a22,a23], [a31,a32,a33]])
pn,pi,pj,pk=sp.symbols('15pn, pi, pj, pk')
Me=matr_2.subs(list(zip([sn,si,sj,sk],[pn,pi,pj,pk])))


Mg=transformacionM(Me, 'g')
Mg2=transformacionM(Me, 'g2')
Mmg=transformacionM(Me, 'mg')
dict_M=dict(hg=Mg, mσg2=Mg2, mgv=Mmg)










#%%

data=pd.read_excel(r'C:\Users\usuario\Desktop\Matrices\matr_normalizadas.xlsx')

data['Espectro']= 'Inicial' #Añado a q pertenece el espectro
#data_test=data.iloc[:9,:]
#data=data_test

Indices=data['Indice']
lenMv=[]
Mincl=[]

#creo mis grupos de comprobacion

dic_t=dict(  eσ=['e','σ'],
hg=['h','g'],
mgv=['v', 'mg'],
mσg2=['mσ','g2'])


dic_g=dict(  eσ='e', hg= 'g', mgv= 'mg', mσg2='g2')
dic_gs=dict(  eσ='σ', hg= 'h', mgv= 'v', mσg2='mσ')

rotaciones=['e', 'g', 'g2', 'mg']

v_transf_i=data['Grupo_de_transformaciones']
#Recorro los indices para saber q matrices estan incompletas

d= {'n*15 =  [-1000,1000]': [0], 'i = [-200,200]': [0], 'j = [-200,200]': [0],'k = [-200,200]': [0], 'Indice': [0], 'Grupo_de_transformaciones': 'a', 'Espectro': 'a'}
Matrfin=pd.DataFrame(data=d)



count=0
for ind in range(np.max(Indices)+1):
    
#prubeo con los primeros
  
    
    
#for ind in np.arange(2):
    
    
    puntosM=np.where(Indices==ind)
    
    Mx_ind=data.loc[(data['Indice']==ind)]

    Mx_ind=Mx_ind.loc[:,['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]','k = [-200,200]', 'Indice', 'Grupo_de_transformaciones', 'Espectro']]
    
    
    #si no tengo los 8 grupos de rasnfromaciones
    #if len(puntosM[0])<8:
    if len(Mx_ind)<8:
        
        
        count+=1
        print(ind, 8-len(Mx_ind), count)
        
        #recorro los 4 pares de grupos y compruebo si están
        for dict_clave in dic_t:
            elem_ausentes=list(set(dic_t[dict_clave]).difference(v_transf_i.iloc[puntosM]))

            
               #si falta uno, cmpleto haciendo la reflexión respecto de la diagonal
               
            if len(elem_ausentes)==1:
              
                #Uso como matriz de artida la correspondiente al elemento q sí está presente
                elem_pres=list(set(dic_t[dict_clave]).difference(elem_ausentes))
                varnijk = Mx_ind.loc[(Mx_ind['Grupo_de_transformaciones'] == elem_pres[0])].loc[
                    :,['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]','k = [-200,200]']].to_numpy()[0]        
                M_var = matr_2.subs(list(zip([sn,si,sj,sk],varnijk))
                
                nijk_nueva =  calculo_sigma (M_var, Me, varnijk) #calculo los nuevos nijk 
                list_row=nijk_nueva.tolist()
                list_row.extend([ind, elem_ausentes[0], 'Hide'])
                #print(list_row,Mx_ind, len(Mx_ind) )
                Mx_ind.loc[len(Mx_ind)+1]=list_row #la añado a la lista
                #print(Mx_ind)
                           
            if len(elem_ausentes)==2:
               
               #uso e como matriz de partida para calcular la rotación
               varnijk=Mx_ind.loc[(Mx_ind['Grupo_de_transformaciones'] == 'e')].loc[
                   :,['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]','k = [-200,200]']].to_numpy()[0]
               M_var = matr_2.subs(list(zip([sn,si,sj, sk],varnijk)))
               nijk_nueva1=calculo_g(M_var,dict_M[dict_clave] )
               #Uso los nuevos nijk como entrada para calcular sigma
               Mnueva = matr_2.subs(list(zip([sn,si,sj, sk],nijk_nueva1)))
               nijk_nueva2= calculo_sigma (Mnueva, Me, nijk_nueva1) 
               
               list_row1=nijk_nueva1.tolist()
               list_row1.extend([ind, dic_g[dict_clave], 'Hide'])
               list_row2=nijk_nueva2.tolist()
               list_row2.extend([ind, dic_gs[dict_clave], 'Hide'])
               Mx_ind.loc[len(Mx_ind)]=list_row1
               Mx_ind.loc[len(Mx_ind)]=list_row2
              
    
    Matrfin=pd.concat([Matrfin,Mx_ind], ignore_index=True)
        

Matrfin=Matrfin.drop(labels=0, axis=0) #quito l aprimera columna q he puesto yo  a capon





#Matrfin.to_excel("espectro_completo.xlsx")
             
             

Mx_ind#%%Reordeno la matriz

dic_elem = dict(list(zip(list(np.arange(8)),list(Matrfin.loc[:8, ['Grupo_de_transformaciones']].to_numpy()))))


Matrfin_ord=pd.DataFrame()

for ind in range(np.max(Indices)+1):
    
   
    for pos in range(8):
        #Matrfin_ord.loc[len(Matrfin_ord)]=Matrfin.loc[(Matrfin['Grupo_de_transformaciones'] == dic_elem[pos][0]) & (Matrfin['Indice']==ind)]
        Matrfin_ord=pd.concat([Matrfin_ord, Matrfin.loc[(Matrfin['Grupo_de_transformaciones'] == dic_elem[pos][0]) & (Matrfin['Indice']==ind)]])

       
Matrfin_ord.to_csv("esp_c_ord.csv")    


        
        
   

