#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 9 - Moduli e Classi:                #
#                                                   #
#   Ricostruzione degli eventi nei file di dati     #
#     a utilizzando il modulo reco                  #
#                                                   #
#####################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import reco



fM0 = 'hit_times_M0.csv'
fM1 = 'hit_times_M1.csv'
fM2 = 'hit_times_M2.csv'
fM3 = 'hit_times_M3.csv'



def get_hits(hf):
    """
    Funzione che legge un file csv e restituisce un array di reco.Hits
    """
    
    df = pd.read_csv(hf)

    hits = np.array([reco.Hit( r['mod_id'], r['det_id'], r['hit_time'] ) for i, r in df.iterrows() ])
    
    return hits


def get_events(ahits, twindow):
    """
    Funzione che crea un array di reco.Event a partire da un array ordinato di reco.Hit (ahits)
    
    Due Hit consecutivi, hit1 e hit2, sono raggruppati nello stesso evento (Event) se:
       hit2.time-hit1.time < twindow 
    """

    events = np.empty(0)

    tlast = -9999
    
    for h in ahits:

        if h.time - tlast > twindow:
            events = np.append( events, reco.Event() )

        events[-1].AddHit(h)
        tlast = h.time

    return events



        
def reconstruct():
    
    # Read filles and create hits Hits 
    hitsM0 = get_hits( fM0 )
    hitsM1 = get_hits( fM2 )
    hitsM2 = get_hits( fM1 )
    hitsM3 = get_hits( fM3 )

    hits = np.concatenate( (hitsM0, hitsM1, hitsM2, hitsM3) )

    #np.sort(hits, kind='mergesort' )
    hits.sort(kind='mergesort' )


    print('Total Number of Hitss:', hits.size)
    
    #for h in hits:
    #    print(h.time, h.mid, h. sid)


    # Tempi hit e differenza fra hit successivi
    hit_times = np.array( [ h.time for h in hits ] )
    hit_dt  = np.diff(hit_times)

    dtmask = hit_dt > 0


    # Grafico tempi Hit (y scala lienare e logaritmica)
    plt.hist(np.log10(hit_dt[dtmask]), bins=100)
    plt.xlabel(r'$log_{10}(\Delta t)$ [ns]')
    plt.show()

    plt.hist(np.log10(hit_dt[dtmask]), bins=100)
    plt.xlabel(r'$log_{10}(\Delta t)$ [ns]')
    plt.yscale('log')
    plt.show()

    logbins = np.logspace(0, 6, 100)
    plt.hist(hit_dt[dtmask], bins=logbins)
    plt.xlabel(r'$\Delta t$ [ns]')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()


    time_window = 100

    recoev = get_events(hits, time_window)

    print('Number of reconstructed Events:', recoev.size)


    xmod = [-5,  5, -5,  5]
    ymod = [ 5,  5, -5, -5]
    
    xdet = [-2.5, 2.5, 0, -2.5,  2.5]
    ydet = [ 2.5, 2.5, 0, -2.5, -2.5]
    
    all_x = [ xm + xd for xm in xmod for xd in xdet]
    all_y = [ ym + yd for ym in ymod for yd in ydet]

    
    for ie in range(10):

        print('---------------- Event {:} ----------------'.format(ie) )
        print('nhits ', recoev[ie].nhits )
        print('tspan',  recoev[ie].tspan )
        print('tstart', recoev[ie].tstart)
        print('tstop ', recoev[ie].tstop )
        print(' Event Hits:') 

        hitpos_x = np.empty(0)
        hitpos_y = np.empty(0)
        hit_t    = np.empty(0)
        for hh in recoev[ie].hits:
            print(hh.mid, hh.sid, hh.time)
            hitpos_x = np.append( hitpos_x, xmod[hh.mid] + xdet[hh.sid] )
            hitpos_y = np.append( hitpos_y, ymod[hh.mid] + ydet[hh.sid] )
            hit_t    = np.append(hit_t, hh.time-recoev[ie].tstart)


        img,ax = plt.subplots(figsize=(9,8))
        plt.title('Event: {:} - Hits: {:}'.format(ie, recoev[ie].nhits))
        plt.scatter(all_x,    all_y,    color='lightgray',  s=240,  alpha=0.3)
        #plt.scatter(hitpos_x, hitpos_y, color='red',        s=240)
        plt.scatter(hitpos_x, hitpos_y,      s=240,  c=hit_t, cmap='plasma_r')
        plt.axvline( 0, color='lightgray')
        plt.axhline( 0, color='lightgray')
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        # Cilorbar 
        plt.colorbar( ax=ax, label='Hit $t-t_{start}$')
        plt.clim(0, 150)
        
        plt.show()

        
    ev_nhits  = np.empty(0)
    ev_tspan  = np.empty(0)
    ev_dt     = np.empty(0)

    tstop_last = 0
    for  ev in  recoev:

        ev_nhits  = np.append( ev_nhits, ev.nhits )
        ev_tspan  = np.append( ev_tspan, ev.tspan )
        if tstop_last > 0:
            ev_dt     = np.append( ev_dt   , ev.tstart-tstop_last )

        tstop_last = ev.tstop

    
    # Grafici su Eventi ricoutruiti 
    plt.hist(ev_nhits, bins=20, range=(0.5, 20.5), color='orange')
    plt.xlabel('Event nhits')
    plt.yscale('log')
    plt.show()

    plt.hist(ev_tspan, bins=50, color='orange')
    plt.xlabel('Event tspan [ns]')
    plt.yscale('log')
    plt.show()

    plt.hist(np.log10(ev_dt), bins=50, color='orange')
    plt.xlabel(r'Events $log_{10}(\Delta t [ns])$')
    plt.yscale('log')
    plt.show()

    plt.scatter(ev_nhits, ev_tspan,  color='orange')
    plt.xlabel('Event nhits')
    plt.ylabel('Event tspan [ns]')
    plt.show()

    plt.scatter(ev_nhits, ev_tspan, alpha=0.1, color='orange')
    plt.xlabel('Event nhits')
    plt.ylabel('Event tspan [ns]')
    plt.xlim(0,21)
    plt.ylim(-10, 140)
    plt.show()

    
if __name__ == "__main__":

    reconstruct()
