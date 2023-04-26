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
os.chdir(r"C:\Users\usuario\Desktop\Matrices")
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
central=10*x-5*y



#%% Variables con Espectros

tiempo=np.arange(len(n))

ax2 = plt.axes()


data_inic=data.loc[data['Espectro']=='Inicial'].to_numpy()
data_h=data.loc[data['Espectro']=='Hide'].to_numpy()


fig, axs = plt.subplots(2, 2)

fig.tight_layout(pad = 4) # adjusts spacing of subplots


plt.sca(axs[0,0])

plt.title('15*n')
#plt.xlabel('Indice')
plt.ylabel('15*n', fontsize = 25)
plt.xlabel('Progresión',fontsize=25 )
plt.scatter( data_inic[:,0], data_inic[:,2], s =3,   c = 'firebrick', label= 'Inicial')
plt.scatter( data_h[:,0], data_h[:,2], s=3,  c = 'steelblue', label= 'Completado')
plt.legend(loc='upper left')


plt.sca(axs[1,0])
plt.title('j')
#plt.xlabel('Indice')
plt.ylabel('j', fontsize = 25)
plt.xlabel('Progresión',fontsize=25 )
plt.scatter( data_inic[:,0], data_inic[:,4], s =3,   c = 'firebrick', label= 'Inicial')
plt.scatter( data_h[:,0], data_h[:,4], s=3,  c = 'steelblue', label= 'Completado')
plt.legend()


plt.sca(axs[0,1])
plt.title('i')
#plt.xlabel('Indice')
plt.ylabel('i', fontsize = 25)
plt.xlabel('Progresión',fontsize=25 )
plt.scatter( data_inic[:,0], data_inic[:,3], s =3,   c = 'firebrick', label= 'Inicial')
plt.scatter( data_h[:,0], data_h[:,3], s=3,  c = 'steelblue', label= 'Completado')
plt.legend()




plt.sca(axs[1,1])
plt.title('k')
#plt.xlabel('Indice')
plt.ylabel('k', fontsize = 25)
plt.xlabel('Progresión',fontsize=25 )
plt.scatter( data_inic[:,0], data_inic[:,5], s =3,   c = 'firebrick', label= 'Inicial')
plt.scatter( data_h[:,0], data_h[:,5], s=3,  c = 'steelblue', label= 'Completado')
plt.legend()





plt.show()

#%%







Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(tiempo, n, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax2.set_title('n')


plt.show()


tiempo=np.arange(len(n))

ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(tiempo, i, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax2.set_title('i')


plt.show()


tiempo=np.arange(len(n))

ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(tiempo, j, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax2.set_title('j')


plt.show()

tiempo=np.arange(len(n))

ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(tiempo, k, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax2.set_title('k')


plt.show()


tiempo=np.arange(len(n))

ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(tiempo, a, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax2.set_title('a')


plt.show()






#%% 2. Plots 2 variables separando los 2 espectros

selecc=np.where(abs(n) < np.max(n) +1)
ax = plt.axes()

#nm=n[int(len(n)//2-len(n)//10): int(len(n)//2+len(n)//10)]
#im=n[len(i)//2-len(i)//10: len(i)//2+len(i)//10]
#am=a[len(i)//2-len(i)//10: len(i)//2+len(i)//10]


scatter=ax.scatter(n[selecc],i[selecc], s=5) #s da el tamaño


ax.set_title('n frente a i con a')
ax.set_xlabel('n')
ax.set_ylabel('i')

#plt.xlim(-200,200)
#plt.ylim()

plt.show()



ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(n,i, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax.set_facecolor("orange")
ax2.set_title('n frente a i ')
ax2.set_xlabel('n')
ax2.set_ylabel('i')


plt.show()


ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(j,k, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax.set_facecolor("orange")
ax2.set_title('j frente a k ')
ax2.set_xlabel('j')
ax2.set_ylabel('k')


plt.show()



ax2 = plt.axes()

Espectro=(data['Espectro']=='Inicial')
scatter=ax2.scatter(i,j, c=Espectro, cmap='RdYlBu', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=2),loc="lower right", title="grupo")

ax.set_facecolor("orange")
ax2.set_title('i frente a j ')
ax2.set_xlabel('i')
ax2.set_ylabel('j')


plt.show()



#%% plots ni con tiempo






ax2 = plt.axes()

ind=data['Indice'].to_numpy()
scatter=ax2.scatter(n,i, c=ind, cmap='gist_rainbow', s=5) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=10),loc="lower right", title="tiempo")

ax.set_facecolor("orange")
ax2.set_title('n frente a i con indice')
ax2.set_xlabel('n')
ax2.set_ylabel('i')

plt.show()



#no ha aportado mucho la cosa
ax3 = plt.axes()

tdist=data['t'].to_numpy()
scatter=ax3.scatter(n,i, c=central, cmap='gist_rainbow', s=5) #s da el tamaño
legend = ax3.legend(*scatter.legend_elements(num=10),loc="lower right", title="distancia al plano")

ax.set_facecolor("orange")
ax3.set_title('n frente a i con indice')
ax3.set_xlabel('n')
ax3.set_ylabel('i')

plt.show()

#%% plots 2 var con info del indice

ax4 = plt.axes()

ind=data['Indice'].to_numpy()
scatter=ax4.scatter(j,i, c=ind, cmap='gist_rainbow', s=5) #s da el tamaño
legend = ax4.legend(*scatter.legend_elements(num=10),loc="lower right", title="tiempo")


ax4.set_title('j frente a i con indice')
ax4.set_xlabel('j')
ax4.set_ylabel('i')

plt.show()



ax5 = plt.axes()

ind=data['Indice'].to_numpy()
scatter=ax5.scatter(n,k, c=ind, cmap='gist_rainbow', s=5) #s da el tamaño
legend = ax5.legend(*scatter.legend_elements(num=10),loc="lower right", title="tiempo")


ax5.set_title('n frente a k con indice')
ax5.set_xlabel('n')
ax5.set_ylabel('k')

plt.show()







#%%Plots de solo algunas matrices de 2 variables



ax2 = plt.axes()

num_matrices=10
pto_inicio=0
ind=data['Indice'].to_numpy()
ind_matrices=pto_inicio
scatter=ax2.scatter(n[ind_matrices:int(ind_matrices+num_matrices*8)],i[
    ind_matrices:ind_matrices+num_matrices*8],c=ind[
        ind_matrices:ind_matrices+num_matrices*8], cmap='gist_rainbow', s=50) #s da el tamaño
legend = ax2.legend(*scatter.legend_elements(num=10),loc="lower right", title="tiempo")

ax.set_facecolor("orange")
ax2.set_title('n frente a i con indice')
ax2.set_xlabel('n')
ax2.set_ylabel('i')

plt.show()





ax=plt.axes()
#ax.set_facecolor("white")
lista_gr=list(data.loc[:7, ['Grupo_de_transformaciones']].to_numpy())
for gr in lista_gr:
    gr_plot=data.loc[data['Grupo_de_transformaciones']==gr[0]].iloc[ind_matrices:ind_matrices+num_matrices,:]
    scatter=ax.scatter(gr_plot['n*15 =  [-1000,1000]'],gr_plot['i = [-200,200]'], s=100, label=gr[0]) #s da el tamaño
    ax.legend()

    ax.set_title('n frente a i')
    ax.set_xlabel('n')
    ax.set_ylabel('i')



#%% Plot 3D

ax4 = plt.axes(projection='3d')

ind=data['Indice'].to_numpy()
scatter=ax4.scatter(a,x,y, c=10*x-5*y, cmap='gist_rainbow', s=5) #s da el tamaño
#legend = ax4.legend(*scatter.legend_elements(num=10),loc="lower right", title="j")


ax4.set_title('4 variables')
ax4.set_xlabel('a')
ax4.set_ylabel('x')
ax4.set_zlabel('y')

ax4.view_init(elev=30, azim=30)

plt.show()


#%%
Ejex=np.arange(len(n))
Espectro=(data['Espectro']=='Inicial')
plt.title('n')
plt.scatter(Ejex, n, c=Espectro, cmap='RdYlBu')
plt.show()
plt.scatter(Ejex, i, c=Espectro, cmap='RdYlBu')
plt.title('i')
plt.show()
plt.scatter(Ejex, j, c=Espectro, cmap='RdYlBu')
plt.title('j')
plt.show()
plt.scatter(Ejex, k, c=Espectro, cmap='RdYlBu')
plt.title('k')
plt.show()


#%% Representacion por grupos de ni
#plt.rcParams["figure.figsize"] = (50,50)
#plt.rcParams["figure.dpi"] = 144
ax=plt.axes()
ax.set_facecolor("white")
lista_gr=list(data.loc[:7, ['Grupo_de_transformaciones']].to_numpy())
for gr in lista_gr:
    gr_plot=data.loc[data['Grupo_de_transformaciones']==gr[0]]
    scatter=ax.scatter(gr_plot['n*15 =  [-1000,1000]'],gr_plot['i = [-200,200]'], s=5, label=gr[0]) #s da el tamaño
    ax.legend()

    ax.set_title('n frente a i')
    ax.set_xlabel('n')
    ax.set_ylabel('i')
    
    

#recta   
from sklearn.linear_model import LinearRegression
xv=n
yv=i  

u=1/np.sqrt(2)*(xv+yv)
v=1/np.sqrt(2)*(xv-yv)


pto_medio=[]
vecto_ptou=[]
#Media en la dirección u 
ptos_selec=np.where(np.abs(u)<800)
for upto in np.unique(u):
    ideu = i[np.where(u==upto)]
    pto_medio.append(np.sum(ideu)/len(ideu))
    vecto_ptou.append(upto)
    

reg = LinearRegression().fit(np.array(vecto_ptou).reshape((-1, 1)), pto_medio) 
m=reg.coef_[0]
y0=reg.intercept_   
recta=u*m+y0   
    
  
    
  
    
  
    
pto_i=400
eje1=np.arange(-pto_i, pto_i) 
eje2=np.arange(-1000, 1000) 
rectai=m*eje2+y0
plt.plot(eje1, -eje1)
plt.plot(eje2,rectai)
#plt.ylim(-1500,1500)
#plt.xlim(-1500,1500)
plt.show()    




#%% Rotación
#Voy a probar la rotación

#Hago un cambio de variables u, v:
    #u=x*cos(45)+y*sen(45)
    #v=x*cos45-ysen(45)

from sklearn.linear_model import LinearRegression
xv=n
yv=i  

u=1/np.sqrt(2)*(xv+yv)
v=1/np.sqrt(2)*(xv-yv)


pto_medio=[]
vecto_ptou=[]
#Media en la dirección u 
ptos_selec=np.where(np.abs(u)<800)
for upto in np.unique(u):
    ideu = i[np.where(u==upto)]
    pto_medio.append(np.sum(ideu)/len(ideu))
    vecto_ptou.append(upto)
    

reg = LinearRegression().fit(np.array(vecto_ptou).reshape((-1, 1)), pto_medio) 
m=reg.coef_[0]
y0=reg.intercept_   
recta=u*m+y0   

plt.plot(u,i, '.')
plt.plot(vecto_ptou, pto_medio, '.')
plt.plot(u,recta)
#plt.xlim(-330,-300)
plt.grid()

plt.show()






#%% Representacion de asolo algunos de los grupos de simetria en los que se divide ni

indices= (n+i>0) & (i-m/np.sqrt(2)*(n+i)-y0>0)
#indices= (n+i<0)
n_s=n*indices
i_s=i*indices
plt.plot(n_s, i_s, '.')
plt.show()



plt.plot(n, '.')
plt.plot(n_s, '.')
plt.title(n)

plt.show()
plt.plot(i, '.')
plt.plot(i_s, '.')
plt.title(i)





#%% Representacion por grupos de las variables
#data['y']=y
ax=plt.axes()
lista_gr=list(data.loc[:7, ['Grupo_de_transformaciones']].to_numpy())
for gr in lista_gr:
    gr_plot=data.loc[data['Grupo_de_transformaciones']==gr[0]]
    scatter=ax.scatter(gr_plot.iloc[:,0],gr_plot['n*15 =  [-1000,1000]'], s=10, label=gr[0]) #s da el tamaño
    ax.legend()

    ax.set_title('n')
    ax.set_xlabel('tiempo')
    ax.set_ylabel('n')
    
    


plt.show()


# =============================================================================
# ax=plt.axes()
# lista_gr=list(data.loc[:7, ['Grupo_de_transformaciones']].to_numpy())
# for gr in lista_gr:
#     gr_plot=data.loc[data['Grupo_de_transformaciones']==gr[0]]
#     scatter=ax.scatter(gr_plot.iloc[:,0],gr_plot['a'], s=10, label=gr[0]) #s da el tamaño
#     ax.legend()
# 
#     ax.set_title('a')
#     ax.set_xlabel('tiempo')
#     ax.set_ylabel('a')
#     
#     
# 
# 
# plt.show()
# 
# =============================================================================

#%%
ax=plt.axes()
lista_gr=list(data.loc[:7, ['Grupo_de_transformaciones']].to_numpy())

scatter=ax.scatter(gr_plot.iloc[:,0],gr_plot['n*15 =  [-1000,1000]'], s=10, label=gr[0]) #s da el tamaño
ax.legend()
plt.show()
plt.plot(gr_plot['n*15 =  [-1000,1000]'], '.')


#%%Representacion de a, x y
from numpy import linalg as LA

plt.plot(a, '.')

plt.show()

plt.plot(n, '.')

plt.show()




#%% Papel del ruido


n=n15/15

tvar=-n+15*i+4*j+11*k
cte=(1+15**2+4**2+11**2)
tvar_n=tvar/(1+15**2+4**2+11**2)
plt.plot(t, '.')
plt.show()
plt.plot(tvar, '.')
plt.show()

import math as mt
np=(-t*cte+15*a+4*x+11*y)/cte
plt.plot(np, '.')

plt.show()
plt.plot(n, '.')
plt.show()

plt.plot(n-np, '.')

plt.show()

naxy=(+15*a+4*x+11*y)/cte
plt.plot(naxy, '.')
plt.show()
plt.plot(naxy-n-t, '.')


n=n15

plt.show()


#%% Plots del Hide




Esp_hide = data.loc[data['Espectro']=='Hide']


nijk = Esp_hide[['n*15 =  [-1000,1000]', 'i = [-200,200]', 'j = [-200,200]', 'k = [-200,200]']].to_numpy()

#nijk=nijk[:5000,:]
n=nijk[:,0]
i=nijk[:,1]
j=nijk[:,2]
k=nijk[:,3]







plt.plot(n, '.')
plt.title('n')
plt.show()
plt.plot(i, '.')
plt.title('i')
plt.show()
plt.plot(j, '.')
plt.title('j')
plt.show()
plt.plot(k, '.')
plt.title('k')
plt.show()



selecc=np.where(abs(n) < np.max(n) +1)
ax = plt.axes()

#nm=n[int(len(n)//2-len(n)//10): int(len(n)//2+len(n)//10)]
#im=n[len(i)//2-len(i)//10: len(i)//2+len(i)//10]
#am=a[len(i)//2-len(i)//10: len(i)//2+len(i)//10]


scatter=ax.scatter(n[selecc],i[selecc], s=5) #s da el tamaño


ax.set_title('n frente a i con a')
ax.set_xlabel('n')
ax.set_ylabel('i')

#plt.xlim(-200,200)
#plt.ylim()

plt.show()

