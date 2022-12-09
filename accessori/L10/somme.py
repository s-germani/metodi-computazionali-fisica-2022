import sys,os
import numpy as np 
import ctypes



# Carico la lireria libsomme (libsomme.so) che è presente nella cartella  (sdir)
_libsomme = np.ctypeslib.load_library('libsomme', '../accessori/L10')


# definizoine tipi di input (argtypes) e di output (restypes) per la funzione sum_n di libsomme 
_libsomme.sum_n.argtypes = [ctypes.c_int]
_libsomme.sum_n.restype  = ctypes.c_int

# definizoine tipi di input (argtypes) e di output (restypes) per la funzione sum_sqrtn di libsomme 
_libsomme.sum_sqrtn.argtypes = [ctypes.c_int]
_libsomme.sum_sqrtn.restype  = ctypes.c_double


# definizoine tipi di input (argtypes) e di output (restypes) per la funzione sum_array di libsomme 
_libsomme.sum_array.argtypes = [np.ctypeslib.ndpointer(dtype=np.float), ctypes.c_int]
_libsomme.sum_array.restype  = ctypes.c_double


# utilizzo di _libsomme.sum_n
# il parametro n va necessariamente convertito in int
def sum_n(n):
    return _libsomme.sum_n(int(n))


# utilizzo di _libsomme.sum_sqrtn
# il parametro n va necessariamente convertito in int
def sum_sqrtn(n):
    return _libsomme.sum_sqrtn(int(n))


# utilizzo di _libsomme.sum_array
# il parametro n va necessariamente ricavato dall'array di input e convertito in int
# l'oggetto av va necessariamente convertito in array (potrebbbe essere anche  uno scalare, una lista, o una ntupla )
def sum_array(av):
    n = len(av)
    av = np.asarray(av, dtype=np.float)
    return _libsomme.sum_array(av, int(n))
