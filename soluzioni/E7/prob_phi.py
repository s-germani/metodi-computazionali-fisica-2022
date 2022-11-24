#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 7 - Metodi Monte Carlo:             #
#                                                   #
#   Distribuzione di Probabilità phi Non Uniforme   #
#                                                   #
#####################################################


import sys,os
import numpy as np

import matplotlib.pyplot as plt






def pphi(phi):
    """
    funzione per probabilità di phi p(phi) = 1/4 sin(phu/2)
    
    return sin(phi/2) / 4
    """
    return np.sin(phi/2)/4


def phi(N):
    """
    funzione per generare una distribuzione random di angoli phi con p(phi)=1/4 sin(phi/2)
    N   : dimensione dell'array di valori di phi  generato

    Genera N valori random della cumulativa (cum) con probabilità uniforme nell'intervallo [0,1]
    Calcola il valore di phi dalla cumulativa inversa phi = 2*arccos(1-2*cum)

    return phi
    """
    
    # valore random per cumulativa 
    cum = np.random.random(N)
    # phi da inversa cumulativa
    phi = 2*np.arccos(1-2*cum)
        
    return phi





def phi_distribution():

    

    # array con valori di phi pergrafico p(phi)
    xphi = np.arange(0, 2*np.pi, 0.1)

    # Grafico p(phi)
    plt.plot(xphi, pphi(xphi) )
    plt.xlabel(r'$\varphi$ [rad]')
    plt.ylabel(r'p($\varphi$)')
    plt.show()
    
    
    #----------------------------------------------------------#
    # Genrazione distribuzione secondo p(phi)
    #----------------------------------------------------------#
    
    N = 100000    # eventi generati
    
    phibins = 99  # numero bin per histogramma phi
    binw = (2*np.pi/phibins)  #largezza bin
    
    # Fattori di conversione fra altezza bin e probabilità 
    p2n = N*binw  # fattore di conversione da probabilità ad altezza bin
    n2p = 1/p2n   # fattore di conversione da altezza bin a probabilità 

    
    # Genero N valori di phi secondo la distrbuzione di probabilità p(phi)
    myphi = phi(N)


    
    # Istogramma valori di phi generati  con sovrapposta la curva di valori attesi da p2n*pphi(phi)
    nb,xbins,_ = plt.hist(myphi, bins=phibins, label='MC' )
    plt.plot(xphi, p2n*pphi(xphi),  label=r'$N \cdot p(\varphi) d\varphi$')
    plt.xlabel(r'$\varphi$ [rad]')
    plt.ylabel(r'Eventi')
    plt.legend(fontsize=14)
    plt.show()

    #print(nb)
    #print(xbins)



    # Istogramma valori di phi generati riscalati per rappresentare la probabilità 
    xc = (xbins[:-1]+xbins[1:])/2
    plt.plot(xc, nb*n2p,       label=r'$nb /(N \cdot d\varphi$)')
    plt.plot(xphi, pphi(xphi), label=r'$p(\varphi)$')
    plt.xlabel(r'$\varphi$ [rad]')
    plt.ylabel(r'$p(\varphi)$')
    plt.legend(fontsize=14)
    plt.show()

    

    # Istogramma valori di phi generati espressi in gradi
    plt.hist(np.rad2deg(myphi), bins=90)
    plt.xlabel(r'$\varphi$ [deg]')
    plt.ylabel(r'')
    plt.show()

                         
if __name__ == "__main__":

    phi_distribution()
