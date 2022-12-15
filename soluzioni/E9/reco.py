#####################################################
# S. Germani (stefano.germani@unipg.it)             #
#                                                   #
# Universià degli Studi di Perugia                  #
# Corso di Metodi Computazionali per la Fisica      #
#---------------------------------------------------#
# Esercitazione 9 - Moduli e Classi:                #
#                                                   #
#   Modulo reco con classi Hit ed Event             #
#      per la ricostruzione di eventi nei dati      #
#                                                   #
#####################################################


import numpy as np


class Hit:

    """
    Classe che definisce gli hit di un rivelatore suddividi in Moduli ognuno dei quali contiene diversi sensori
    
    Attributi:
    mid  : Id Modulo
    sid  : Id Sensore
    time : Time Stamp rivelazione
    """

    def __init__(self, mid, sid, time):

        self.mid     = mid  # module id
        self.sid     = sid  # single detector id inside module
        self.time    = time
        #self.signal  = signal


    def __eq__(self, other) :
        return self.time == other.time

    def __lt__(self, other) :
        return self.time < other.time

    def __gt__(self, other) :
        return self.time > other.time




class Event:

    def __init__(self):
        
        self.nhits  = 0
        self.tsart  = -9999
        self.tstop  = -9999
        self.tspan  = -9999

        self.hits = np.empty(0)


    def __eq__(self, other) :
        return self.tstart == other.tstart and self.tstop == other.tstop and self.nhits == other.nhits

    def __lt__(self, other) :
        return self.tstart < other.tstart

    def __gt__(self, other) :
        return self.tstart > other.tstart


        
    def AddHit(self,  hit):
        
        self.hits = np.append(self.hits, hit)
        self.nhits = self.hits.size
        if self.nhits == 1:
            self.tstart = hit.time
        self.tstop = hit.time
        self.tspan = self.tstop - self.tstart
        

        
