#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 7 - Metodi Monte Carlo:             #
#                                                   #
#   Diffusione 2D                                   #
#                                                   #
#####################################################


import sys,os
import numpy as np
import pandas as pd

from scipy import integrate

import matplotlib.pyplot as plt



############################################################
#            Random Walk 2D Uniforme                       #
############################################################


def random_walk2d(step, N):
    """
    funzione random_walk2d(step, N) per generare una sequenza di random walk 2D
        ad ogni passo il moto sarà lungo la direzione casuale 
        dettata dall'angolo phi  
    step: passo del random walk
    N   : numero di passi

    per ogni passo delta_X = step*cos(phi), delta_Y = step*sin(phi), 
    reuturn deltax, deltay: array con coordinate per i diversi passi
    """

    # Array posizioni x e y (partenza dalla posizione 0,0)
    deltax = np.array([0])
    deltay = np.array([0])

    # Valori random di phi per gli N passi distribuiti uniformemente
    phi = np.random.uniform(low=0, high=2*np.pi, size=N)

    # Ciclo sui valori di phi per calcolare gli spostamenti 
    for p in phi:

        # Valori temporanei con nuovo step
        tmpx = deltax[-1] + step*np.cos(p)
        tmpy = deltay[-1] + step*np.sin(p)

        # Appendo nuove posizione agli array degli spostamenti
        deltax = np.append(deltax, tmpx)
        deltay = np.append(deltay, tmpy)
        
    return deltax, deltay




############################################################
#    Random Walk 2D Non Uniforme p(phi)=sin(phi/2)/4       #
############################################################


def random_walk2d_pphi(step, N):
    """
    funzione random_walk2d_pphi(step, N) per generare una sequenza di random walk 2D
        ad ogni passo il moto sarà lungo la direzione casuale 
        dettata dall'angolo phi. 
        Distribuzione di probabilità di phi: p(ph) = 1/4 sin(phi/2). 
    step: passo del random walk
    N   : numero di passi

    per ogni passo delta_X = step*cos(phi), delta_Y = step*sin(phi), 
    reuturn deltax, deltay: array con coordinate per i diversi passi
    """

    # Array posizioni x e y (partenza dalla posizione 0,0)
    deltax = np.array([0])
    deltay = np.array([0])
    
    
    # Valori random per cumulativa per gli N passi
    #    distribuiti uniformemente nell'intervallo [0,1]
    cum = np.random.random(N)
    # phi da inversa cumulativa 
    phi = 2*np.arccos(1-2*cum)

    # Ciclo sui valori di phi per calcolare gli spostamenti 
    for p in phi:
        
        # Valori temporanei con nuovo step
        tmpx = deltax[-1] + step*np.cos(p)
        tmpy = deltay[-1] + step*np.sin(p)

        # Appendo nuove posizioni agli array degli spostamenti
        deltax = np.append(deltax, tmpx)
        deltay = np.append(deltay, tmpy)
        
    return deltax, deltay




############################################################
#            Funzione principale per grafici               #
############################################################
               
def diffusione_2d():


    # Definizione lunghezza passo (step) e numero passi
    step0   = 1
    Nsteps0 = 1000

    
    #--------------------------------------------------------#
    #  Random Walk  Unforme                                  # 
    #--------------------------------------------------------#
    
    # Ciclo per calcolo 5 random walk uniformi da 1000 passi 
    plt.subplots(figsize=(9,8))
    for i in range(5):
        x0,y0 = random_walk2d(step0, Nsteps0)
        plt.scatter(x0,y0, s=3)
        
    plt.xlabel(r'$\Delta x$')
    plt.ylabel(r'$\Delta y$')
    plt.xlim(-75, 75)
    plt.ylim(-75, 75)
    plt.show()



    # Calcolo per 1000 walker a diversi passi (10, 100, 1000)
    Nwalkers = 100

    # Array per posizioni walker
    x10   = np.empty(0)
    y10   = np.empty(0)
    x100  = np.empty(0)
    y100  = np.empty(0)
    x1000 = np.empty(0)
    y1000 = np.empty(0)

    # Array per calcolo media e media quadratica
    dsqm  = np.zeros(Nsteps0+1)
    dm    = np.zeros(Nsteps0+1)

    # Ciclo per i 1000 walker
    for iw in range(Nwalkers):

        # Posizioni x,y per walker iw 
        xw,yw = random_walk2d(step0, Nsteps0)

        # Posizione al passo 1000
        x1000 = np.append(x1000, xw[-1])
        y1000 = np.append(y1000, yw[-1])

        # Posizione al passo 100
        x100  = np.append(x100, xw[99])
        y100  = np.append(y100, yw[99])

        # Posizione al passo 10
        x10   = np.append(x10, xw[9])
        y10   = np.append(y10, yw[9])

        # Somma delle distanze e delle distanze al quadrato
        dsqm = dsqm + (xw**2+yw**2)
        dm   = dm  + np.sqrt(xw**2+yw**2)


    # distanza media e quadratica media
    dsqm = dsqm/Nwalkers
    dm   = dm/Nwalkers

    
    #Grafico posizione walker dopo 10, 100, 1000 passi 
    plt.scatter(x1000,y1000, s=10, alpha=0.8, label='{:d} steps'.format(    Nsteps0   ))
    plt.scatter(x100, y100,  s=10, alpha=0.7, label='{:d} steps'.format(int(Nsteps0/10)))
    plt.scatter(x10,  y10,   s=10, alpha=0.6, label='{:d} steps'.format(int(Nsteps0/100)))
    plt.xlabel(r'$\Delta x$', fontsize=14)
    plt.ylabel(r'$\Delta y$', fontsize=14)
    plt.xlim(-75, 75)
    plt.ylim(-75, 75)
    plt.legend(fontsize=12)
    plt.show()




    # Grafico distanza quadratica media in funzione del numero di passi
    plt.plot(dsqm)
    plt.xlabel(r'Passi', fontsize=14)
    plt.ylabel(r'$\left< d^2 \right>$', fontsize=14)
    plt.show()

    # Grafico distanza  media in funzione del numero di passi
    plt.plot(dm)
    plt.xlabel(r'Passi', fontsize=14)
    plt.ylabel(r'$\left< d \right>$', fontsize=14)
    plt.show()


    
    #--------------------------------------------------------#
    #  Random Walk Non Unforme                               # 
    #--------------------------------------------------------#
    
    # Ciclo per calcolo 5 random walk non uniformi da 1000 passi     
    fig,ax = plt.subplots(1,2, figsize=(16,8))
    for i in range(5):
        x0pphi,y0pphi = random_walk2d_pphi(step0, Nsteps0)

        ax[0].scatter(x0pphi,y0pphi, s=3)
        ax[1].scatter(x0pphi,y0pphi, s=3)
        
    ax[0].set_xlabel(r'$\Delta x$')
    ax[0].set_ylabel(r'$\Delta y$')
    ax[1].set_xlabel(r'$\Delta x$')
    ax[1].set_ylabel(r'$\Delta y$')
    ax[0].set_xlim(-500, 500)
    ax[0].set_ylim(-500, 500)
    ax[1].set_xlim(-500, 50)
    ax[1].set_ylim(-50,  50)

    plt.show()



                         
if __name__ == "__main__":

    diffusione_2d()
