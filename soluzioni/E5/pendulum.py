
#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 5 - Equazioni Dfferenziali:         #
#                                                   #
#   Pendolo Semplice                                #
#                                                   #
#####################################################

import numpy as np
from scipy import integrate, constants
import matplotlib.pyplot as plt
import matplotlib.animation as animation


############################################################################
#      Funzione per Equazione Differenziale del Pendolo                    #
############################################################################

def pendulum_eqn(r, t, l):
    """
    Funzione che definisce le equazioni differenziali del moto di un pendolo semplice
    
    r      : vettore con variabili r(theta,omega)
    t      : variabile tempo
    l      : lunghezza filo di sopensione
    """
    g = constants.g
    dthetadt = r[1]
    domegadt = -g/l * np.sin(r[0])
    return (dthetadt,domegadt)



############################################################################
#      Funzioni per animazione                           #
############################################################################


def animate_pendulum(i, x, y, dt, line, mass, text):
    """
    Funzione pe animazione pendolo

    Assegna la posizione  istante per istante  agli ogetti da animare
    Il fulcro del pendolo è posizionato alle coordinate (0,0)

    Parametri
    ----------

    i    : indice del frame da rappresenare (obbligatorio con FuncAnimatuin)
    x    : array con coordinate x della massa del pendolo in funzione del tempo
    y    : array con coordinate y della massa del pendolo in funzione del tempo
    dt   : distanza temporale fra i punti dell'array dei tempi con cui si è risolta l'equazione del moto
    line : oggetto grafico  che rappresenta il filo di sospensione (plt.plot([0,x[i]],[0,yi[i]]))
    mass : oggetto grafico  che rappresenta la massa del pendolo   (plt.plot(   x[i],    yi[i] ))
    text : testo con tempo che scorre

    Output
    -----------
    return line, mass, text
    """
    
    line_x = [0, x[i]]
    line_y = [0, y[i]]
    line.set_data(line_x,line_y)

    mass_x = x[i]
    mass_y = y[i]
    mass.set_data(mass_x,mass_y)

    time_template = 'time = %.1fs'
    text.set_text(time_template % (i*dt))

    return line, mass, text



############################################################################
#      Funzione principale per calcolo e grafici                           #
############################################################################

def pendulum():

    #------------------- Definizioni preliminari --------------------------#
    
    # lunghezza pendolo 
    l1=0.5 # m
    l2=1.0 # m

    # Parametri per condizioni iniziali
    theta0 = np.radians(45)
    omega0 = 0

    # Condizioni iniziali al punto di massima oscillazione (theta=theta0, omega=emega0=0) 
    rinit45 = (theta0, omega0)
    
    # Condizioni iniziali al punto di massima oscillazione (theta=theta0*2/3, omega=emega0=0) 
    rinit30 = (theta0*2/3, omega0)


    # delta t per array tempi
    dt = 0.01

    # array con tempi
    ptimes = np.arange(0, 5, dt)


    #------------------- Soluzione Equazione Moto ------------------------#

    # Soluzioni tramite scipy.integrate.odeint
    psol45_1  = integrate.odeint(pendulum_eqn, rinit45, ptimes, args=(l1,)) 
    psol45_2  = integrate.odeint(pendulum_eqn, rinit45, ptimes, args=(l2,)) 
    psol30_1  = integrate.odeint(pendulum_eqn, rinit30, ptimes, args=(l1,))
    

    # Grafico soluzioni 
    plt.subplots(figsize=(9,7))
    #plt.title('Pendolo', fontsize=16)
    plt.plot(ptimes, np.degrees(psol45_1[:,0]), label=r'$\theta_0 = 45^{\circ}$ l=0.5 $m$')
    plt.plot(ptimes, np.degrees(psol45_2[:,0]), label=r'$\theta_0 = 45^{\circ}$ l=1.0 $m$')
    plt.plot(ptimes, np.degrees(psol30_1[:,0]), label=r'$\theta_0 = 30^{\circ}$ l=0.5 $m$')
    plt.xlabel('t [s]',            fontsize=14)
    plt.ylabel(r'$\theta$  [deg]', fontsize=14)
    plt.xticks( fontsize=14 )
    plt.yticks( fontsize=14 )
    plt.legend( fontsize=14, ncol=3, bbox_to_anchor=(-0.01, 1.0, 1.0, 0.15), loc='lower left', framealpha=0  )
    plt.show()



    #------------------- Animazione  ------------------------------------#

    # proiezione su asse x e y della soluzione. 
    x1 =  1*np.sin(psol45_1[:, 0])
    y1 = -1*np.cos(psol45_1[:, 0])


    # Figura per animazione 
    fig = plt.figure(figsize=(9,8))
    ax  = fig.add_subplot(111, autoscale_on=False, xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
    #ax.grid()


    # Oggetti da animare (linea, massa, testo)
    pendulum_line, = ax.plot([], [], 'o-', lw=2, markersize=5,  color='slategray')
    pendulum_mass, = ax.plot([], [], 'o',        markersize=15, color='darkred'  )
    time_text      = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=16)

    # Animazione 
    pendulum_ani = animation.FuncAnimation(
        fig,                                                        # Figura per animazione
        animate_pendulum,                                           # Funzione per animazione con calcolo oggetti ad ogni istante
        np.arange(1, len(y1)),                                      # valori su cui iterare ( corripondnete all'indice i in animate)
        fargs=( x1,y1,dt, pendulum_line, pendulum_mass, time_text), # argomenti aggiuntivi della funzione animate 
        interval=25,                                                # Intervallo fra due frame successivi (ms)
        blit=True)                                                  # Ottimizzazione grafica
    plt.show()



if __name__ == "__main__":

    pendulum()
    
