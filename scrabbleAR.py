import PySimpleGUI as sg
from funciones_comunes.modulo_configuraciones import imprimir_configuraciones
from funciones_comunes.cambio_tablero_con_colores import imprimir_tablero


''' Este codigo imprime la ventana de Menu principal del juego con 2 botones: el que abre el tablero e inicia una partida
y el que abre la ventana para configurar el juego'''
sg.theme('DarkAmber')
layout=[[sg.Text('Menu Principal')],
[sg.Button('Iniciar Partida', key='partida')],
        [sg.Button('Configuraciones', key='conf')],
        [sg.Button('Salir')]]

window=sg.Window('ScrableAr').Layout(layout)

while True:
	evento, valor = window.Read()
	if evento == 'partida':
		imprimir_tablero()  
	if evento == 'conf':
		imprimir_configuraciones()
	if evento in ('Salir', None):
		break

window.close()

