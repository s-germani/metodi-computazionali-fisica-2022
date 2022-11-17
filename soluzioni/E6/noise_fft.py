#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 6 - Trasformate di Fourier:         #
#                                                   #
#   FFT di diversi tipi di rumore                   #
#                                                   #
#####################################################

import numpy as np
import pandas as pd
from scipy import constants, fft, optimize
import matplotlib.pyplot  as plt


#####################################################################
#      Funzioni per fit Spettro di Potenza                          #         
#####################################################################


def noisef(f, N, beta):
    """
    Funzione per fit Spettro Potenza di diversi tipi di rumore

    f    : frequenze
    N    : normalizzazione
    beta : esponente per dipendenza da frequenza

    return N/f^beta
    """
    
    return N/f**beta




#####################################################################
#      Funzioni principale per calcolo FFT                          #         
#####################################################################

def noise_fft():


    #---------------------------------------------------------------#
    #              Lettura files di dati                            #
    #---------------------------------------------------------------#

    
    df1 = pd.read_csv('data_sample1.csv')
    df2 = pd.read_csv('data_sample2.csv')
    df3 = pd.read_csv('data_sample3.csv')

    print('DF1', df1.columns)
    print('DF2', df2.columns)
    print('DF3', df3.columns)


    #---------------------------------------------------------------#
    #              Grafico segnali di input                         #
    #---------------------------------------------------------------#

    fig,ax = plt.subplots(figsize=(9,6))

    plt.plot(df1['time'], df1['meas'], color='cyan',      label='Sample 1')
    plt.plot(df2['time'], df2['meas'], color='limegreen', label='Sample 2')
    plt.plot(df3['time'], df3['meas'], color='orange',    label='Sample 3')
    plt.legend()
    plt.xlabel('time [s]')
    plt.xlabel('Signal')
    plt.show()

    #---------------------------------------------------------------#
    #              Calcolo FFT e Grafico PS                         #
    #---------------------------------------------------------------#

    # Campione 1
    dt1 = df1['time'][1]-df1['time'][0]

    c1  = fft.fft(df1['meas'].values)
    f1  = fft.fftfreq(len(c1), d=dt1)

    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2,  color='cyan')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.show()


    # Campione 2
    dt2 = df2['time'][1]-df2['time'][0]

    c2  = fft.fft(df2['meas'].values)
    f2  = fft.fftfreq(len(c2), d=dt2)

    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2,  color='limegreen')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.show()



    # Campione 3
    dt3 = df3['time'][1]-df3['time'][0]

    c3  = fft.fft(df3['meas'].values)
    f3  = fft.fftfreq(len(c3), d=dt3)

    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2,  color='orange')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.show()



    # Grafico PS Campion1 1,2,3
    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2,        color='cyan')
    plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2,        color='limegreen')
    plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2,        color='orange')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.show()


    #---------------------------------------------------------------#
    #              Fit PS                                           #
    #---------------------------------------------------------------#

    # Fit Sample 1
    pv1, pc1 = optimize.curve_fit(noisef , f1[2:len(c1)//2], np.absolute(c1[2:len(c1)//2])**2, p0=[1, 1])
    print('Parameters Fit Sample 1', pv1)
    
    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f1[:len(c1)//2],  np.absolute(c1[:len(c1)//2])**2,           color='cyan')
    plt.plot( f1[1:len(c1)//2], noisef(f1[1:len(c1)//2], pv1[0], pv1[1] ), color='darkcyan'   )
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.text(0.1, 0.1, r'Sample 1 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv1[1], np.sqrt(pc1[1,1])), fontsize=14, transform=ax.transAxes, color='darkcyan' )
    plt.show()



    # Fit Sample 2
    pv2, pc2 = optimize.curve_fit(noisef , f2[5:len(c2)//2], np.absolute(c2[5:len(c2)//2])**2, p0=[1, 1])
    print('Parameters Fit Sample 2', pv2)

    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f2[:len(c2)//2],  np.absolute(c2[:len(c2)//2])**2,           color='limegreen')
    plt.plot( f2[1:len(c2)//2], noisef(f2[1:len(c2)//2], pv2[0], pv2[1] ), color='darkgreen')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.text(0.1, 0.1, r'Sample 2 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv2[1], np.sqrt(pc2[1,1])), fontsize=14, transform=ax.transAxes, color='darkgreen' )
    plt.show()



    # Fit Sample 3
    pv3, pc3 = optimize.curve_fit(noisef , f3[5:len(c3)//2], np.absolute(c3[5:len(c3)//2])**2, p0=[1, 1])
    print('Parameters Fit Sample 3', pv3)

    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f3[:len(c3)//2],  np.absolute(c3[:len(c3)//2])**2,           color='orange')
    plt.plot( f3[1:len(c3)//2], noisef(f3[1:len(c3)//2], pv3[0], pv3[1] ), color='darkred'   )
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.text(0.1, 0.1, r'Sample 3 -  $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv3[1], np.sqrt(pc3[1,1])), fontsize=14, transform=ax.transAxes, color='darkred' )
    plt.show()



    #---------------------------------------------------------------#
    #              Grafico Finale                                   #
    #---------------------------------------------------------------#

    # Grafico PS Campion1 1,2,3 con Fit
    plt.style.use('dark_background')
    fig,ax = plt.subplots(figsize=(9,6))
    plt.plot( f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2, color='white',  label=r'Sample 1 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv1[1], np.sqrt(pc1[1,1])) )
    plt.plot( f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2, color='pink'  , label=r'Sample 2 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv2[1], np.sqrt(pc2[1,1])) )
    plt.plot( f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2, color='tomato', label=r'Sample 3 - $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv3[1], np.sqrt(pc3[1,1])) )

    plt.plot( f1[1:len(c1)//2], noisef(f1[1:len(c1)//2], pv1[0], pv1[1] ), color='slategray' )
    plt.plot( f2[1:len(c2)//2], noisef(f2[1:len(c2)//2], pv2[0], pv2[1] ), color='magenta'   )
    plt.plot( f3[1:len(c3)//2], noisef(f3[1:len(c3)//2], pv3[0], pv3[1] ), color='darkred'   )

    plt.legend(fontsize=14, frameon=False)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f [Hz]')
    plt.show()



if __name__ == "__main__":

    noise_fft()
