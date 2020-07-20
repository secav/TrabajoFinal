import json
from os import remove
import PySimpleGUI as sg

def guardar_posponer(start_time,fichas_jugadorb,fichas_computadora,acumulador_puntos_pc,acumulador_puntos_jugador,
paused_time,nivel_dificultad,tablero,bolsa_fichas,cont_cambio,lista_tuplas_usadas,tiempo,primera_vez,primero,palabras_permitidas,conjunto_hard=''):
	archivo=open('juego_postergado.txt','w')
	fichas_jugador=[]
	num=1
	#print(len(fichas_jugadorb))
	for i in fichas_jugadorb:
		letra=i.GetText()
		#print(letra)
		fichas_jugador.append(letra)
	dic={'fichas_jugador':fichas_jugador,'fichas_computadora':fichas_computadora,'acumulador_puntos_pc':acumulador_puntos_pc,
	'acumulador_puntos_jugador':acumulador_puntos_jugador,'paused_time':paused_time,'nivel_dificultad':nivel_dificultad,
	'tablero':tablero,'bolsa_fichas':bolsa_fichas,'cont_cambio':cont_cambio,'lista_tuplas_usadas':lista_tuplas_usadas,'max_tiempo':tiempo,'primera_vez':primera_vez,'primero':primero,'palabras_permitidas':palabras_permitidas,'conjunto_hard':conjunto_hard,
	'start_time':start_time}
	json.dump(dic,archivo)
	archivo.close()
	for clave,valor in dic.items():
		print(clave,valor)
		

def abrir_posponer():
	try:
		archivo=open('juego_postergado.txt','r')
		dic=json.load(archivo)
		archivo.close()
		remove('juego_postergado.txt')
		return dic
	except FileNotFoundError:
		return False
		
