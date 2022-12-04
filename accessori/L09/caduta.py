import sys

g=9.81

def v(t):
    """
    Funzione che restituisce la velocità al tempo t

    return g*t
    """
    return g*t

def s(t):
    """
    Funzione che restituisce lo spazio percorso al tempo t

    return 0.5 *g*t^2
    """

    return 0.5 *g*t**2

def h(h0, t):
    """
    Funzione che restituisce la quota al tempo t con quota di partenza h0
    
    return h0 -0.5 *g*t^2
    """

    return h0 -0.5 *g*t**2



if __name__ == "__main__":

    t = float(sys.argv[1])
    print('v({:}) = {:}'.format(t, v(t)))
    print('s({:}) = {:}'.format(t, s(t)))

          
