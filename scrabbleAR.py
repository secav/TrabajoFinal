import PySimpleGUI as sg
from funciones_comunes.modulo_configuraciones import imprimir_configuraciones
from funciones_comunes.cambio_tablero_con_colores import imprimir_tablero
from funciones_comunes.modulo_rankin import imprimir_rankin
from funciones_comunes.modulo_reglas import imprimir_reglas
from funciones_comunes.modulo_posponer import abrir_posponer
from os import remove



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
	sg.theme('DarkAmber')
	layout=[[sg.Text('Menu Principal')],
	[sg.Button('Continuar partida',key='continue',visible=visi)],
	[sg.Button('Iniciar Partida', key='partida')],
			[sg.Button('Configuraciones', key='conf')],
			[sg.Button('Ranking',key='rank')],
			[sg.Button('Reglas',key='reglas')],
			[sg.Button('Salir')]]

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

