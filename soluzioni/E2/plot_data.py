#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 2 - Numpy, Pandas, Matplotlib:      #
#                                                   #
#   Lettura File CSV e Grafico Dati                 #
#                                                   #
#####################################################

import sys,os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Lettura dati da file
df = pd.read_csv('dati_atmosferici.csv')

#stampo noi colonne
print(df.columns)

# stampo header DataFrame 
#print(df.head)



# grafico di temepratura e mm di pioggia in funzione del giorno, sullo stesso pannello, senza errori;
plt.plot(df['giorno'], df['temp'],    'o-', color='orange', label='Temperatura [$^{\circ}$C]')
plt.plot(df['giorno'], df['pioggia'], 'o-', color='blue',   label='Pioggia [mm]')
plt.xlabel('Giorno')
plt.legend(fontsize=14)
plt.show()


#grafico di temperatura e pioggia in funzione del giorno, su pannelli diversi, con errori;
fig, ax = plt.subplots(1,2, figsize=(13,7))

# pannello 0
ax[0].errorbar(df['giorno'], df['temp'], yerr=df['temp_e'], fmt='o', color='orange')
ax[0].set_title('Temperatura', color='orange', fontsize=16)
ax[0].set_xlabel('Giorno', fontsize=14)
ax[0].set_ylabel('Temperatura [$^{\circ}$C]', fontsize=14)
ax[0].set_ylim(0, 30)

#pannello 1
ax[1].errorbar(df['giorno'], df['pioggia'], yerr=df['pioggia_e'], fmt='o', color='blue')
ax[1].set_title('mm di Piogga', color='blue',  fontsize=16)
ax[1].set_xlabel('Giorno', fontsize=14)
ax[1].set_xlabel('Pioggia [mm]', fontsize=14)
ax[1].set_ylim(0, 10)

plt.show()


#scatter plot dei mm di pioggia in funzione della temepratura.
plt.scatter( df['temp'], df['pioggia'], color='limegreen' )
plt.xlabel('Temperatura [$^{\circ}$C]', fontsize=14)
plt.ylabel('Pioggia [mm]', fontsize=14)
plt.xlim(0,30)
plt.ylim(0,10)
plt.show()



