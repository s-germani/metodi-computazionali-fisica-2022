
class Cane():

    _tipo = 'Animale Domestico'
    
    def __init__(self, nome, razza, colore):
        self.nome   = nome
        self.razza  = razza
        self.colore = colore
 

    def descrizione(self):
        print('--------------------------------')
        print('Cane     {:}'.format(self._tipo ))        
        print('  nome   {:}'.format(self.nome  ))
        print('  razza  {:}'.format(self.razza ))
        print('  colore {:}'.format(self.colore))
        print('--------------------------------')




class Felino():

    _tipo = 'Carnivoro'
    
    def __init__(self, nomes, origine, peso):
        self.nomes    = nomes
        self.origine  = origine
        self.peso     = peso


    def descrizione(self):
        print('--------------------------------------------')
        print('Felino             {:}'.format(self._tipo   ))        
        print('  nome scientifico {:}'.format(self.nomes   ))
        print('  origine          {:}'.format(self.origine ))
        print('  peso             {:}'.format(self.peso    ))
        print('--------------------------------------------')


    
