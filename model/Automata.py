class Automata:
    def __init__(self, estados, entradas, transiciones, estadoInicial, estadosFinales):
        #self.descripcion = descripcion
        self.estados = estados
        self.entradas = entradas
        self.transiciones = transiciones
        self.estadoInicial = estadoInicial
        self.estadosFinales = estadosFinales


def NewAutomata( estados, entradas, transiciones, estadoInicial, estadosFinales):
    return Automata( estados, entradas, transiciones, estadoInicial, estadosFinales)

def get_descripcion(self):
    return self.descripcion
    
def get_estados(self):
    return self.estados
    
def get_entradas(self):
    return self.entradas
    
def get_transiciones(self):
    transiciones_str = []
        
    for estadoOrigen, transiciones in self.transiciones.items():
        for entrada, estadoDestino in transiciones.items():
            transicion_str = estadoOrigen + ":  " + entrada + " -> " + estadoDestino
            transiciones_str.append(transicion_str)
        
    return transiciones_str
    
def get_estado_inicial(self):
    return self.estadoInicial
    
def get_estados_finales(self):
    return self.estadosFinales
    
def get_imagen(self):
    return self.imagen

def set_estados(self, estados):
        self.estados = estados
    
def set_entradas(self, entradas):
    self.entradas = entradas
    
def set_transiciones(self, transiciones):
    self.transiciones = transiciones
    
def set_estado_inicial(self, estadoInicial):
    self.estadoInicial = estadoInicial
    
def set_estados_finales(self, estadosFinales):
    self.estadosFinales = estadosFinales
