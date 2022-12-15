#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 9 - Moduli e Classi:                #
#                                                   #
#   Semplice modulo con due funzioni (mymodule)     #
#                                                   #
#####################################################


import numpy as np


def somma_n(n):
    """
    Funzione che restituisce la somma dei primi n numeri naturali
    n : numeri naturali da sommare
    """

    nn = np.arange(n)

    return nn.sum()



def somma_sqrtn(n):
    """
    Funzione che restituisce la somma delle radici dei primi n numeri naturali
    n : numeri naturali di cui sommare le radici
    """

    nn = np.arange(n)
    sqrtn = np.sqrt(nn)
    
    return sqrtn.sum()




