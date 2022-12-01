#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 8 - Monte Carlo Markov Chain:       #
#                                                   #
#   Studio linea spettrale di assorbimento          #
#       tramite MCMC                                #
#                                                   #
#####################################################

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy import stats
import matplotlib.pyplot as plt
import emcee
import corner


############################################################
#   Modello teorico dello spettro di linea di assorbimento #
############################################################

def model_l1(params, ev):
    """
    return m*e+b -alpha*Gauss(E-mu, sigma)
    """
    m, b, alpha1, e1, s1 = params
    return m*ev + b + alpha1 * np.exp(-0.5 * (ev - e1) ** 2 / s1**2)



############################################################
#   Probabilità logaritimche                               #
############################################################


def lnlike_l1(p, e, y, yerr):
    """ 
    Log Likelihood: -0.5 * Sommatoria( (data-model)^2/err^2 )
    """
    return -0.5 * np.sum(((y - model_l1(p, e))/yerr) ** 2)


def lnprior_l1(p):
    """ 
    Log Prior: probabilità uniforme 
    """
    m, b, alpha1, e1, s1 = p
    if (-2 < m < 0 and   0 < b < 50 and
        -10 < alpha1 < 0 and 1 < e1 < 10 and 0 < s1 < 2):
        return 0.0
    return -np.inf



def lnprob_l1(p, e, y, yerr):
    lp = lnprior_l1(p)

    if np.isfinite(lp):
        return lp + lnlike_l1(p, e, y, yerr)
    else:
        return -np.inf



############################################################
#   Proposta Metropolis-Hastings                          #
############################################################


# 
def mhmove(ndim):
    """
    Spostamento per proposta  metodo MH
    Random uniforme (dimensini ndim) nell'intervallo [-0.1,0.1] per valore delta  (Proposta)
    """
    return np.random.uniform(-0.05, 0.05, size=ndim)
    #return np.random.uniform(-0.1, 0.1, size=ndim)


def mheval(pnow, pnext, fp, pars):
    """
    Valutazione proposta con metodo MH
    """
    e, y, yerr = pars
    fpnow  = fp(pnow,  e, y, yerr )
    fpnext = fp(pnext, e, y, yerr )
    if fpnext >= fpnow:
        return pnext
    else:
        if np.random.random()<np.exp(fpnext-fpnow):
            return pnext
        else:
            return pnow


############################################################
#            Funzione principale con  metrodo MCMCM       #
############################################################

def mcmc():

    #--------------------------------------------------------#
    #  Lettura e controllo dati                              #
    #--------------------------------------------------------#

    l1df = pd.read_csv('absorption_line.csv')

    print(l1df.columns)
    
    plt.subplots(figsize=(9,6))
    plt.errorbar(l1df['E'], l1df['f'], yerr=l1df['ferr'], fmt='o', color='black')
    plt.show()
    

    ltruth = (-0.2, 10, -5, 4.8, 0.6) 

    
    #--------------------------------------------------------#
    #  MCMC base                                             #
    #--------------------------------------------------------#

    p0    = np.array([-1, 1, -1.0, 3, 0.1])
    ndim  = len(p0)


    mychain = np.array([p0]) # 

    for _ in range(15000):
        propxy  = mychain[-1]+mhmove(ndim)
        #newxy   = mheval(mychain[-1], propxy, lnlike_l1, (l1df['E'].values, l1df['f'].values, l1df['ferr'].values) )
        newxy   = mheval(mychain[-1], propxy, lnprob_l1, (l1df['E'].values, l1df['f'].values, l1df['ferr'].values) )
        mychain = np.append( mychain, [newxy], axis=0)



    labels = ['m', 'b', r'$\alpha$', r'$\mu$', r'$\sigma$' ]
        
    # Grafinco andamento dei parametri
    fig,axs = plt.subplots(ndim,1, figsize=(9,6), sharex=True)
    for i in range(ndim):
        axs[i].plot(mychain[:,i], color='red')
        axs[i].set_ylabel(labels[i])

    axs[-1].set_xlabel('Passi')
    plt.show()
        
    #plt.scatter(mychain[:,0], mychain[:,1], alpha=0.2, color='red')    
    #plt.xlim(-10, 10)
    #plt.ylim(-10, 10)
    #plt.show()



    # Grafico dati e campionamenti modello 
    plt.subplots(figsize=(9,6))
    plt.errorbar(l1df['E'], l1df['f'], yerr=l1df['ferr'], fmt='o', color='black')
    
    sel_chain = mychain[-1000:-1]
    eplot = np.arange(1, 10, 0.02)
    for s in np.random.randint(len(sel_chain), size=50):
        plt.plot(eplot, model_l1(sel_chain[s], eplot), color="royalblue", alpha=0.3)

    #plt.plot(l1df['E'], model_l1(mychain[-1], eplot), color="darkblue", alpha=0.3)
    plt.show()


    fig = corner.corner( sel_chain, labels=labels, truths=ltruth, color='royalblue');
    plt.show()
    
    #--------------------------------------------------------#
    #  MCMC tramite emcee                                    #
    #--------------------------------------------------------#

    # walkers
    nw = 32


    p0w = np.array(p0)  +0.1*np.random.randn(nw, ndim)
    lsampler = emcee.EnsembleSampler(nw, ndim, lnprob_l1, args=(l1df['E'].values, l1df['f'].values, l1df['ferr'].values))

    print("MCMC run")
    lsampler.run_mcmc(p0w, 2000, progress=True);


    fig, axes = plt.subplots(ndim, figsize=(10, 9), sharex=True)
    lsamples = lsampler.get_chain()

    for i in range(ndim):
        ax = axes[i]
        ax.plot(lsamples[:, :, i], "orange", alpha=0.3)
        ax.set_xlim(0, len(lsamples))
        ax.set_ylabel(labels[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)

    axes[-1].set_xlabel("Passi");
    plt.show()


    # Grafico dati e campionamenti modello
    plt.subplots(figsize=(9,6))
    plt.errorbar(l1df['E'], l1df['f'], yerr=l1df['ferr'], fmt='o', color='black')


    # 50 posterior.
    lflat_samples = lsampler.get_chain(discard=500, thin=15, flat=True)
    for s in lflat_samples[np.random.randint(len(lflat_samples), size=50)]:
        plt.plot(eplot, model_l1(s, eplot), color="orange", alpha=0.3)
    plt.show()


    fig = corner.corner( lflat_samples, labels=labels, truths=ltruth, color='orange');
    plt.show()
    

    
if __name__ == "__main__":

    mcmc()
