#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 3 - Integrazione e Derivazione:     #
#                                                   #
#   Distanza percorsa da velocità                   #
#                                                   #
#####################################################



import sys,os
import numpy as np
import pandas as pd

from scipy import integrate

import matplotlib.pyplot as plt



# Lettura file 
veldf = pd.read_csv('vel_vs_time.csv')

# Colonne Data Frame
print(veldf.columns)


## grafico velocità vs tempo
plt.plot(veldf['t'], veldf['v'])
plt.xlabel('tempo [s]')
plt.ylabel('velocità [m/s]')
plt.show()


# Array per le distanze
dists = np.array([])


# Ciclo su intervalli temporali 
for iv in range(1, len(veldf['v'])+1): 
    # integrale per distanza nell'intevallo temporale 0-iv
    idists = integrate.simpson(veldf['v'][:iv],   dx=0.5)
    # appendo valore dell'integrale all'array di distanze
    dists = np.append(dists, idists)


## grafico distanza vs tempo
plt.plot(veldf['t'], dists)
plt.xlabel('tempo [s]')
plt.ylabel('distanza percorsa [m]')
plt.show()


