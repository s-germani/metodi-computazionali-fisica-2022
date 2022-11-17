#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 6 - Trasformate di Fourier:         #
#                                                   #
#   Analisi con FFT di dati su inquinanti a Perugia #
#    dati elaborati a partire dalle misure          #
#    pubblicamente disponibili grazie al            #
#    programma Copernicus della UE:                 #
#     https://www.copernicus.eu/it                  #
#                                                   #
#####################################################

import numpy as np
import pandas as pd
from scipy import constants, fft
import matplotlib.pyplot  as plt



def copernicus():

    #---------------------------------------------------------------#
    #              Lettura file di dati                             #
    #---------------------------------------------------------------#

    dfPG = pd.read_csv('copernicus_PG_selected.csv')

    print(dfPG.size)
    print(dfPG.columns)

    #---------------------------------------------------------------#
    #              Grafico inquinanti                               #
    #---------------------------------------------------------------#

    plt.subplots(figsize=(10,7))
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_co_ug/m3'],    label='CO'   )
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_nh3_ug/m3'],   label='NH3'  )
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_no2_ug/m3'],   label='NO2'  )
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_pm10_ug/m3'],  label='PM10' )
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_pm2p5_ug/m3'], label='PM2.5')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_so2_ug/m3'],   label='SO2'  )
    plt.xlabel('Time [d]')
    plt.ylabel(r'Concentration [$\mu g/m^3$]')
    plt.legend(fontsize=14)
    plt.yscale('log')
    plt.show()

    

    #---------------------------------------------------------------#
    #              Analisi CO                                       #
    #---------------------------------------------------------------#

    #print(dfPG['mean_co_ug/m3'].values)

    coft   = fft.fft( dfPG['mean_co_ug/m3'].values )      # Coefficienti FT 
    cops   = np.absolute(coft)**2                          # Spettro di potenza
    cofreq = fft.fftfreq( len(coft), d=1 )                 # Frequenze

    
    #print(cops)
    #print(cofreq)

    # Grafico Spettro di Potenza senza escludere il termine c(0) per f=0 e le frequenze negative il cui coefficiente c(-f)
    #  è il cmplesso coniugato del coefficiente c(f): c(-f) = c(f)*

    #  le frequenze sono ordinate secondo l'ordine [0-->fmax, -fmax, 0[
    #  per produrre un grafico corretto si possono riordinare le frequenze con fft.fftshift
    cofrshift = fft.fftshift(cofreq)
    copsshift = fft.fftshift(cops)
    
    
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot(cofrshift, copsshift)
    #plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r'f [$d^{-1}$]',                  fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()

    
    # Grafico Spettro di Potenza per frequenze positive (escludendo anche il termine c(0) per f=0 
    #  che corrisponde alla somma di tutti i valori campionati
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot(cofreq[1:len(coft)//2], cops[1:len(coft)//2])
    plt.xscale('log')
    plt.xlabel(r'f [$d^{-1}$]',                  fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()

    # Grafico Spettro di Potenza log-log
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot(cofreq[1:len(coft)//2], cops[1:len(coft)//2])
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r'f [$d^{-1}$]',                  fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()


    # Massimo spettro di potenza
    coam = np.argmax(cops[1:len(coft)//2])+1
    print('Massimo PS: {:f} - Freq {:f} - Periodo: {:d}'.format( cops[coam], cofreq[coam], int(1/cofreq[coam])) )


    # Grafico Spettro di Potenza in funzione del periodo (1/freq) con Massimo
    fig,ax = plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot(1/cofreq[1:len(coft)//2], cops[1:len(coft)//2])
    plt.plot( 1/cofreq[coam], cops[coam], 'o' )
    plt.xscale('log')
    plt.yscale('log')
    plt.text(0.8, 0.2, 'T ~ {:d} d'.format(int(1/cofreq[coam])), transform=ax.transAxes, fontsize=14, color='slategray')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()
    




    # Applico filtro su frequenze più alte tramite una maschera:
    # 1. definisco maschera per frequenze in superiori a fcut in valore assoluto (fcut = 0.5*10^-2, 1*10^-2, 2*10^-2)
    #    va considerato che le frequenze vanno da -fmax ad fmax ma che i coefficienti per frequenze negative
    #    sono il coniugato di quelli per frequenze positive; 
    # 2. copio i coefficienti della FFT per applicare il filtro;
    # 3. pongo a zero i coefficienti per frequenze superiori ad fcut
    # 4. ricavo il segnale filtrato attraverso la trasformata di Fourer inversa

    # definisco maschera per frequenze in superiori a fcut in valore assoluto (fcut = 0.5*10^-2, 1*10^-2, 2*10^-2)
    filter_comask05 = np.absolute(cofreq)  > 0.5e-2
    filter_comask1  = np.absolute(cofreq)  > 1e-2
    filter_comask2  = np.absolute(cofreq)  > 2e-2

    # copio i coefficienti della FFT per applicare il filtro;
    filtered_coft05 = coft.copy()
    filtered_coft1  = coft.copy()
    filtered_coft2  = coft.copy()

    # pongo a zero i coefficienti per frequenze superiori ad fcut
    filtered_coft05[filter_comask05] = 0
    filtered_coft1[ filter_comask1]  = 0
    filtered_coft2[ filter_comask2]  = 0

    #filtered_coft05[0]  = 0
    #filtered_coft05[-1] = 0

    # ricavo il segnale filtrato attraverso la trasformata di Fourer inversa
    filtered_co05 = (fft.ifft(filtered_coft05)).astype(float)
    filtered_co1  = (fft.ifft(filtered_coft1) ).astype(float)
    filtered_co2  = (fft.ifft(filtered_coft2) ).astype(float)



    # Grafico con confronto fra senale originale e segnale filtrati
    #print(len(filtered_coft1), len(filtered_co1), dfPG.shape )
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_co_ug/m3'], color='gray',  label='CO' )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_co2,     color='red',        lw=3,
              label=r'CO filtered $\nu$ < 1/{:d} d'.format(int(1/2e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_co1,     color='darkorange', lw=3,
              label=r'CO filtered $\nu$ < 1/{:d} d'.format(int(1/1e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_co05,    color='purple',     lw=3,
              label=r'CO filtered $\nu$ < 1/{:d} d'.format(int(1/0.5e-2)) )

    plt.legend()
    #plt.yscale('log')
    plt.xlabel('Time [d]')
    plt.ylabel(r'Concentration [$\mu g/m^3$]')
    plt.show()



    # Grafico dei residui fra segnale originale e segnale filtarto
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_co_ug/m3']-filtered_co05,    color='purple')
    #plt.yscale('log')
    plt.xlabel('Time [d]')
    plt.ylabel(r'$\Delta$ Concentration [$\mu g/m^3$]')
    plt.show()



    # Trasformata di  Fourier inversa e Grafici con componente costante sottratta
    f0const = filtered_coft05[0].astype(float)/len(filtered_coft05)
    filtered_coft05[0]  = 0

    
    # ricavo il segnale filtrato attraverso la trasformata di Fourer inversa
    filtered_co05 = (fft.ifft(filtered_coft05)).astype(float)

    # Grafico con confronto fra senale originale e segnale filtrati
    #print(len(filtered_coft1), len(filtered_co1), dfPG.shape )
    plt.subplots(figsize=(10,7))
    plt.title('CO')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_co_ug/m3']-f0const, color='gray',  label='CO' )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_co05,    color='purple',     lw=3,
              label=r'CO filtered $\nu$ < 1/{:d} d'.format(int(1/0.5e-2)) )

    plt.legend()
    #plt.yscale('log')
    plt.xlabel('Time [d]')
    plt.ylabel(r'$\Delta$ Concentration [$\mu g/m^3$]')
    plt.show()




    #---------------------------------------------------------------#
    #              Analisi PM10                                       #
    #---------------------------------------------------------------#
    # Ripeto parte dell'analisi per le PM10

    pm10ft   = fft.fft( dfPG['mean_pm10_ug/m3'].values )
    pm10ps   = np.absolute(pm10ft)**2
    pm10freq = fft.fftfreq( len(pm10ft), d=1 )

    # Grafico Spettro di Potenza log-log
    plt.subplots(figsize=(10,7))
    plt.title('PM10')
    plt.plot(pm10freq[1:len(pm10ft)//2], pm10ps[1:len(pm10ft)//2])
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel(r'f [$d^{-1}$]',                  fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()



    # Massimo spettro di potenza
    pm10am = np.argmax(pm10ps[1:len(pm10ft)//2]) +1
    print('Massimo PS: {:f} - Freq {:f} - Periodo: {:d}'.format( pm10ps[pm10am], pm10freq[pm10am], int(1/pm10freq[pm10am])) )

    # Grafico Spettro di Potenza in funzione del periodo (1/freq) con Massimo
    fig,ax = plt.subplots(figsize=(10,7))
    plt.title('PM10')
    plt.plot(1/pm10freq[1:len(pm10ft)//2], pm10ps[1:len(pm10ft)//2])
    plt.plot( 1/pm10freq[pm10am], pm10ps[pm10am], 'o' )
    plt.xscale('log')
    plt.yscale('log')
    plt.text(0.8, 0.2, 'T ~ {:d} d'.format(int(1/pm10freq[pm10am])), transform=ax.transAxes, fontsize=14, color='slategray')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()


    
    filter_pm10mask05 = np.absolute(pm10freq) > 0.5e-2
    filter_pm10mask1  = np.absolute(pm10freq)  > 1e-2
    filter_pm10mask2  = np.absolute(pm10freq)  > 2e-2

    filtered_pm10ft05 = pm10ft.copy()
    filtered_pm10ft1  = pm10ft.copy()
    filtered_pm10ft2  = pm10ft.copy()

    filtered_pm10ft05[filter_pm10mask05] = 0
    filtered_pm10ft1[ filter_pm10mask1]  = 0
    filtered_pm10ft2[ filter_pm10mask2]  = 0


    filtered_pm1005 = (fft.ifft(filtered_pm10ft05)).astype(float)
    filtered_pm101  = (fft.ifft(filtered_pm10ft1) ).astype(float)
    filtered_pm102  = (fft.ifft(filtered_pm10ft2) ).astype(float)

    #print(len(filtered_pm10ft1), len(filtered_pm101), dfpm10p.shape )
    plt.subplots(figsize=(10,7))
    plt.title('PM10')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_pm10_ug/m3'], color='gray',  label='PM10' )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_pm102,     color='red',        lw=3,
              label=r'PM10 filtered $\nu$ < 1/{:d} d'.format(int(1/2e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_pm101,     color='darkorange', lw=3,
              label=r'PM10 filtered $\nu$ < 1/{:d} d'.format(int(1/1e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_pm1005,    color='purple',     lw=3,
              label=r'PM10 filtered $\nu$ < 1/{:d} d'.format(int(1/0.5e-2)) )

    plt.legend()
    #plt.yscale('log')
    plt.show()





    #---------------------------------------------------------------#
    #              Analisi NH3                                       #
    #---------------------------------------------------------------#
    # Ripeto parte dell'analisi per le NH3

    nh3ft   = fft.fft( dfPG['mean_nh3_ug/m3'].values )
    nh3ps   = np.absolute(nh3ft)**2
    nh3freq = fft.fftfreq( len(nh3ft), d=1 )

    # Grafico Spettro di Potenza log-log
    plt.subplots(figsize=(10,7))
    plt.title('NH3')
    plt.plot(nh3freq[1:len(nh3ft)//2], nh3ps[1:len(nh3ft)//2])
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel(r'f [$d^{-1}$]',                  fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()


    # Massimo spettro di potenza
    nh3am = np.argmax(nh3ps[1:len(nh3ft)//2]) +1
    print('Massimo PS: {:f} - Freq {:f} - Periodo: {:d}'.format( nh3ps[nh3am], nh3freq[nh3am], int(1/nh3freq[nh3am])) )

    # Grafico Spettro di Potenza in funzione del periodo (1/freq) con Massimo
    fig,ax = plt.subplots(figsize=(10,7))
    plt.title('NH3')
    plt.plot(1/nh3freq[1:len(nh3ft)//2], nh3ps[1:len(nh3ft)//2])
    plt.plot( 1/nh3freq[nh3am], nh3ps[nh3am], 'o' )
    plt.xscale('log')
    plt.yscale('log')
    plt.text(0.8, 0.2, 'T ~ {:d} d'.format(int(1/nh3freq[nh3am])), transform=ax.transAxes, fontsize=14, color='slategray')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.show()

    
    filter_nh3mask05 = np.absolute(nh3freq) > 0.5e-2
    filter_nh3mask1  = np.absolute(nh3freq)  > 1e-2
    filter_nh3mask2  = np.absolute(nh3freq)  > 2e-2

    filtered_nh3ft05 = nh3ft.copy()
    filtered_nh3ft1  = nh3ft.copy()
    filtered_nh3ft2  = nh3ft.copy()

    filtered_nh3ft05[filter_nh3mask05] = 0
    filtered_nh3ft1[ filter_nh3mask1]  = 0
    filtered_nh3ft2[ filter_nh3mask2]  = 0


    filtered_nh305 = (fft.ifft(filtered_nh3ft05)).astype(float)
    filtered_nh31  = (fft.ifft(filtered_nh3ft1) ).astype(float)
    filtered_nh32  = (fft.ifft(filtered_nh3ft2) ).astype(float)

    #print(len(filtered_nh3ft1), len(filtered_nh31), dfnh3p.shape )
    plt.subplots(figsize=(10,7))
    plt.title('NH3')
    plt.plot( dfPG['date']-dfPG['date'][0], dfPG['mean_nh3_ug/m3'], color='gray',  label='NH3' )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_nh32,     color='red',        lw=3,
              label=r'NH3 filtered $\nu$ < 1/{:d} d'.format(int(1/2e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_nh31,     color='darkorange', lw=3,
              label=r'NH3 filtered $\nu$ < 1/{:d} d'.format(int(1/1e-2)) )
    plt.plot( dfPG['date']-dfPG['date'][0], filtered_nh305,    color='purple',     lw=3,
              label=r'NH3 filtered $\nu$ < 1/{:d} d'.format(int(1/0.5e-2)) )

    plt.legend()
    #plt.yscale('log')
    plt.show()



    #---------------------------------------------------------------#
    #              Confronto PS per diversi inquinanti              #
    #---------------------------------------------------------------#

    # Spettro di potenza CO, PM10, NH3
    plt.subplots(figsize=(10,7))
    plt.plot(1/nh3freq[1:len(nh3ft)//2],   nh3ps[1:len(nh3ft)//2],   label='NH3')
    plt.plot(1/cofreq[1:len(coft)//2],     cops[1:len(coft)//2],     label='CO')
    plt.plot(1/pm10freq[1:len(pm10ft)//2], pm10ps[1:len(pm10ft)//2], label='PM10')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(fontsize=14)
    plt.show()


    # Spettro di potenza CO, PM10, NH3 normalizzato con coefficiente c(0)**2  per migliore confronto 
    #  il coefficiente c(0) per la frequenza f=0 corrisponde alla somma di tutti i campionamenti
    #   c(0)/nsample corrisponde al valormedio della curva
    plt.subplots(figsize=(10,7))
    plt.plot(1/nh3freq[1:len(nh3ft)//2],   nh3ps[1:len(nh3ft)//2]/nh3ps[0],    label='NH3')
    plt.plot(1/cofreq[1:len(coft)//2],     cops[1:len(coft)//2]/cops[0],       label='CO')
    plt.plot(1/pm10freq[1:len(pm10ft)//2], pm10ps[1:len(pm10ft)//2]/pm10ps[0], label='PM10')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(fontsize=14)
    plt.show()



    # Spettro di potenza CO, PM10, NH3 normalizzato al massimo
    plt.subplots(figsize=(10,7))
    plt.plot(1/nh3freq[1:len(nh3ft)//2],   nh3ps[1:len(nh3ft)//2]/nh3ps[nh3am],     label='NH3')
    plt.plot(1/cofreq[1:len(coft)//2],     cops[1:len(coft)//2]/cops[coam],         label='CO')
    plt.plot(1/pm10freq[1:len(pm10ft)//2], pm10ps[1:len(pm10ft)//2]/pm10ps[pm10am], label='PM10')
    plt.xlabel(r'T [$d$]',                       fontsize=14)
    plt.ylabel(r'$|c_{FFT}|^2$ [$\mu g^2/m^6$]', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(fontsize=14)
    plt.show()



    


if __name__ == "__main__":

    copernicus()
