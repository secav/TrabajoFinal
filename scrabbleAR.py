import PySimpleGUI as sg
from funciones_comunes.modulo_configuraciones import imprimir_configuraciones
from funciones_comunes.cambio_tablero_con_colores import imprimir_tablero
from funciones_comunes.modulo_rankin import imprimir_rankin
from funciones_comunes.modulo_reglas import imprimir_reglas
from funciones_comunes.modulo_posponer import abrir_posponer
from os import remove
import sys

def columna_opciones():
	'''Devuelve el diseño de los botones de configuracion, ranking y reglas'''
	layout=[[sg.Button( key='conf',image_filename="./imagenes/engranaje.png",image_size=(36, 36),border_width=0,button_color=('black','black')),
	sg.Button(key='reglas',image_filename="./imagenes/libro.png",image_size=(36, 36),border_width=0,button_color=('black','black')),
	sg.Button(key='rank',image_filename="./imagenes/medalla.png",image_size=(36, 36),border_width=0,button_color=('black','black'))]]
	return layout

def columna_principal():
	'''Devuelve el diseño de los botones de continuar partida, iniciar Partida y salir'''
	layout=[[sg.Button('Continuar partida',key='continue',visible=visi,image_filename="./imagenes/boton_naranja.png",image_size=(126, 33),border_width=0,button_color=('black','black'))],
	[sg.Button('Iniciar Partida', key='partida',image_filename="./imagenes/boton_naranja.png",image_size=(126, 33),border_width=0,button_color=('black','black'))],
	[sg.Button('Salir',image_filename="./imagenes/boton_naranja.png",image_size=(126, 33),border_width=0,button_color=('black','black'))]
]
	return layout

''' Este codigo imprime la ventana de Menu principal del juego con 2 botones: el que abre el tablero e inicia una partida
y el que abre la ventana para configurar el juego'''
salio=False
while(salio==False):

	opcion=abrir_posponer()
	print('opcion',opcion)
	if(type(opcion)==bool):
		visi=False
	else:
		visi=True
	print('visi',visi)
	sg.theme('Black')

	if sys.platform == 'win32':
		cant_esp=9
	else:
		cant_esp=6

	layout=[[sg.Image('./imagenes/cinta.png')],

	[sg.Text(' '*cant_esp),sg.Column(columna_principal())],
	[sg.Text(' '*(cant_esp+2)),sg.Column(columna_opciones())]]

	window=sg.Window('ScrableAr').Layout(layout)
	while True:
		evento, valor = window.Read()
		if evento=='continue':
			remove('juego_postergado.txt')
			imprimir_tablero(opcion)
			break
		if evento == 'partida':
			if (type(opcion)!=bool):
				remove('juego_postergado.txt')
			imprimir_tablero()
			break
		elif evento == 'conf':
			imprimir_configuraciones()
		elif evento == 'reglas':
			imprimir_reglas()
		elif evento=='rank':
			imprimir_rankin()
		elif evento in ('Salir', None):
			salio=True
			break
	window.close()
