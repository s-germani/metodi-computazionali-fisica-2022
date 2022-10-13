import sys,os
import numpy as np
import pandas as pd



# Giorno del mese (1-30)
gg = np.arange(1,31)

# Temperatura 
temp = np.array( [ 20., 19., 21., 22., 21., 22., 22., 23., 22., 21., 22., 23., 22.,
                   22., 22., 23., 23., 23., 23., 23., 23., 24., 24., 24., 24., 25.,
                   24., 23., 23., 25.  ] )

# Errore temperatura
temp_e = 0.5*np.ones(30)


# mm di piioggia
mm = np.array([2., 1., 1., 2., 2., 2., 2., 2., 3., 3., 4., 3., 4., 3., 2., 3., 3.,
       4., 4., 4., 4., 4., 4., 5., 5., 5., 5., 5., 4., 4.])

# errore mm di pioggia
mm_e = 0.2* np.ones(30)



# creo DataFrame vuoto
dfatm = pd.DataFrame(columns=['giorno', 'temp', 'temp_e', 'pioggia', 'pioggia_e'])

# Assegno valori alle colonne del DataFrame
dfatm['giorno']    = gg
dfatm['temp']      = temp
dfatm['temp_e']    = temp_e
dfatm['pioggia']   = mm
dfatm['pioggia_e'] = mm_e


# Salvo dataframe su file
dfatm.to_csv('dati_atmosferici.csv', index=False)



