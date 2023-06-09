from logging import root
from pathlib import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import tkinter as tk
import networkx as nx

from matplotlib import pyplot as plt
import numpy as np
from model.Automata import *
from collections import deque


from tkinter import filedialog
import json


def cargar_cadena_txt(ruta_archivo):
    try:
        # Cargar el contenido del archivo en una cadena de texto
        with open(ruta_archivo, 'r') as archivo:
            cadena = archivo.read()

        print(cadena)
        return cadena
    except Exception as e:
        raise Exception("Error al cargar el archivo: " + str(e))


def cargar_automata_desde_json() -> Automata:
    """
    Esta función carga un autómata desde un archivo JSON seleccionado por el usuario.
    :return: una instancia de la clase Automata, que se crea utilizando datos cargados desde un archivo
    JSON seleccionado por el usuario a través de un cuadro de diálogo de archivo. Si no se selecciona
    ningún archivo, la función devuelve Ninguno.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='Seleccionar archivo JSON', filetypes=[('JSON Files', '*.json')])

    if file_path:
        with open(file_path, 'r') as file:
            automata_data = json.load(file)

        estados = automata_data['estados']
        entradas = automata_data['entradas']
        transiciones = automata_data['transiciones']
        estado_inicial = automata_data['estado_inicial']
        estados_finales = automata_data['estados_finales']

        afnd = NewAutomata(estados, entradas, transiciones,
                           estado_inicial, estados_finales)
        return afnd
    else:
        return None


def convertir_afnd_a_afd(afnd: Automata) -> Automata:
    """
    Esta función convierte un autómata finito no determinista (NFA) en un autómata finito determinista
    (DFA).

    :param afnd: un objeto de la clase Automata que representa el autómata finito no determinista que se
    convertirá en un autómata finito determinista
    :type afnd: Automata
    :return: una instancia de la clase Automata, que representa el autómata finito determinista (DFA)
    convertido a partir de la entrada de autómata finito no determinista (NFA) dada.
    """
    # Inicializar el AFD con el estado inicial del AFND
    estado_inicial_afd = frozenset([afnd.estadoInicial])
    estados_afd = [estado_inicial_afd]
    entradas_afd = afnd.entradas
    transiciones_afd = {}
    estados_finales_afd = []

    # Cola para almacenar los estados a procesar
    cola = deque([estado_inicial_afd])

    while cola:
        estado_actual = cola.popleft()

        # Verificar si el estado actual es un estado final
        if any(estado in estado_actual for estado in afnd.estadosFinales):
            estados_finales_afd.append(estado_actual)

        # Calcular las transiciones para cada entrada
        for entrada in entradas_afd:
            estados_destino = set()

            # Obtener los estados alcanzables desde el estado actual con la entrada actual
            for estado in estado_actual:
                if estado in afnd.transiciones and entrada in afnd.transiciones[estado]:
                    estados_destino.update(afnd.transiciones[estado][entrada])

            # Si hay estados destino, agregar la transición al AFD
            if estados_destino:
                estados_destino = frozenset(estados_destino)
                transiciones_afd.setdefault(estado_actual, {})[
                    entrada] = estados_destino

                # Si el estado destino no se ha procesado, agregarlo a la cola para su procesamiento
                if estados_destino not in estados_afd:
                    estados_afd.append(estados_destino)
                    cola.append(estados_destino)

    afd = Automata(estados_afd, entradas_afd, transiciones_afd,
                   estado_inicial_afd, estados_finales_afd)

    return afd


def mostrar_automatas(automata_no_determinista, automata_determinista):
    """
    La función "mostrar_automatas" traza autómatas no deterministas y deterministas utilizando la
    biblioteca networkx en Python.

    :param automata_no_determinista: Un objeto autómata no determinista
    :param automata_determinista: Objeto de autómata finito determinista (DFA) que representa un
    lenguaje o una expresión regular. Tiene un conjunto de estados, un estado inicial, un conjunto de
    estados finales y un conjunto de transiciones que definen cómo se mueve el autómata de un estado a
    otro en función de los símbolos de entrada
    """
    # Plot non-deterministic automaton
    plt.figure(figsize=(8, 6))
    grafo_no_determinista = nx.DiGraph()
    grafo_no_determinista.add_nodes_from(automata_no_determinista.estados)
    for estado, transiciones in automata_no_determinista.transiciones.items():
        for entrada, estados_destino in transiciones.items():
            for estado_destino in estados_destino:
                grafo_no_determinista.add_edge(
                    estado, estado_destino, label=entrada)
    pos_no_determinista = nx.spring_layout(grafo_no_determinista, k=0.3)


    # Colores y tamaños de nodos
    node_colors_no_determinista = [
        'lightblue' for _ in grafo_no_determinista.nodes]
    node_colors_no_determinista[list(automata_no_determinista.estados).index(
        automata_no_determinista.estadoInicial)] = 'green'
    node_colors_no_determinista[list(automata_no_determinista.estados).index(
        automata_no_determinista.estadosFinales[0])] = 'red'
    node_sizes_no_determinista = [
        1000 if node == automata_no_determinista.estadoInicial else 800 if node in automata_no_determinista.estadosFinales else 500 for node in grafo_no_determinista.nodes]

    nx.draw_networkx(
        grafo_no_determinista,
        pos_no_determinista,
        with_labels=True,
        node_color=node_colors_no_determinista,
        node_size=node_sizes_no_determinista,
        font_color='black',
        font_size=12,
        linewidths=0.5,
        edge_color='gray',
        alpha=0.7
    )
    edge_labels_no_determinista = nx.get_edge_attributes(
        grafo_no_determinista, 'label')
    nx.draw_networkx_edge_labels(grafo_no_determinista, pos_no_determinista,
                                 edge_labels=edge_labels_no_determinista, font_color='black')
    plt.title('Autómata no determinista')
    plt.axis('off')
    plt.show()

    # Plot deterministic automaton
    plt.figure(figsize=(8, 6))
    grafo_determinista = nx.DiGraph()
    grafo_determinista.add_nodes_from(automata_determinista.estados)

    frozenset_nodes = []

    for estado, transiciones in automata_determinista.transiciones.items():
        if isinstance(estado, frozenset):  # Verificar si el estado es un frozenset
            frozenset_nodes.append(estado)
            for entrada, estados_destino in transiciones.items():
                estados_frozenset_destino = [e for e in estados_destino if isinstance(e, frozenset)]
                if estados_frozenset_destino:  # Verificar si hay estados frozenset destino
                    for estado_destino in estados_frozenset_destino:
                        grafo_determinista.add_edge(estado, estado_destino, label=entrada)
    
    # Obtener las transiciones de los frozensets
    for frozenset_node in frozenset_nodes:
        transiciones = automata_determinista.transiciones[frozenset_node]
        for entrada, estados_destino in transiciones.items():
            for estado_destino in estados_destino:
                if isinstance(estado_destino, frozenset):
                    for nodo_destino in frozenset_nodes:
                        if nodo_destino.issubset(estado_destino):
                            grafo_determinista.add_edge(frozenset_node, nodo_destino, label=entrada)

    # Posiciones de los nodos en el grafo
    pos_determinista = nx.spring_layout(grafo_determinista, k=0.3)

    # Colores y tamaños de nodos
    node_colors_determinista = ['lightblue' if isinstance(node, frozenset) else 'white' for node in grafo_determinista.nodes]
    node_colors_determinista[list(automata_determinista.estados).index(
        automata_determinista.estadoInicial)] = 'green'
    node_colors_determinista[list(automata_determinista.estados).index(
        automata_determinista.estadosFinales[0])] = 'red'
    node_sizes_determinista = [
        1000 if node == automata_determinista.estadoInicial else 800 if node in automata_determinista.estadosFinales else 500 for node in grafo_determinista.nodes]

    # Dibujar el grafo determinista
    nx.draw_networkx(
        grafo_determinista,
        pos_determinista,
        with_labels=True,
        node_color=node_colors_determinista,
        node_size=node_sizes_determinista,
        font_color='black',
        font_size=12,
        linewidths=0.5,
        edge_color='gray',
        alpha=0.7
    )

    # Agregar etiquetas a las transiciones
    edge_labels = {(u, v): d['label'] for u, v, d in grafo_determinista.edges(data=True)}
    nx.draw_networkx_edge_labels(grafo_determinista, pos_determinista, edge_labels=edge_labels, font_size=10)
    
    plt.title('Autómata Finito Determinista')
    plt.axis('off')
    plt.show()

def cargar_automata_json():
    """
    Esta función carga un autómata desde un archivo JSON, lo convierte en un autómata determinista y
    muestra ambos autómatas.
    """
    afnd = cargar_automata_desde_json()

    if afnd:
        print(afnd.entradas)
        afd = convertir_afnd_a_afd(afnd)
        mostrar_automatas(afnd, afd)
        print("Esta en la condicion")
    else:
        tk.messagebox.showwarning(
            'Advertencia', 'No se seleccionó ningún archivo.')


def cargar_automata_txt():
    """
    Esta función carga un autómata desde un archivo JSON, lo convierte en un autómata determinista y
    muestra ambos autómatas.
    """
    afnd = cargar_automata_txt()

    if afnd:
        print(afnd.entradas)
        afd = convertir_afnd_a_afd(afnd)
        mostrar_automatas(afnd, afd)
        print("Esta en la condicion")
    else:
        tk.messagebox.showwarning(
            'Advertencia', 'No se seleccionó ningún archivo.')
