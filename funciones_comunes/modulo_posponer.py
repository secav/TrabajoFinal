import json
import PySimpleGUI as sg

def guardar_posponer(turno_quien,start_time,fichas_jugadorb,fichas_computadora,acumulador_puntos_pc,acumulador_puntos_jugador,
paused_time,nivel_dificultad,tablero,bolsa_fichas,cont_cambio,lista_tuplas_usadas,tiempo,primera_vez,primero,palabras_permitidas,conjunto_hard=''):
	'''La funcion recibe datos de distinto tipo, crea un archivo de texto donde guarda dichos datos utilizando un diccionario
	y json '''
	archivo=open('juego_postergado.txt','w')
	fichas_jugador=[]
	num=1

	for i in fichas_jugadorb:
		letra=i.GetText()
		#print(letra)
		fichas_jugador.append(letra)
	dic={'fichas_jugador':fichas_jugador,'fichas_computadora':fichas_computadora,'acumulador_puntos_pc':acumulador_puntos_pc,
	'acumulador_puntos_jugador':acumulador_puntos_jugador,'paused_time':paused_time,'nivel_dificultad':nivel_dificultad,
	'tablero':tablero,'bolsa_fichas':bolsa_fichas,'cont_cambio':cont_cambio,'lista_tuplas_usadas':lista_tuplas_usadas,'max_tiempo':tiempo,'primera_vez':primera_vez,'primero':primero,'palabras_permitidas':palabras_permitidas,'conjunto_hard':conjunto_hard,
	'start_time':start_time,'turno_quien':turno_quien}
	json.dump(dic,archivo)
	archivo.close()



def abrir_posponer():
	'''La funcion intenta abrir el archivo donde se guarda la informacion del juego en el caso de que se haya pospuesto,
	 si el archivo no existe retorna false, de lo contrario retorna la informacion que se encuentra en el archivo '''
	try:
		archivo=open('juego_postergado.txt','r')
		dic=json.load(archivo)
		archivo.close()
		return dic
	except FileNotFoundError:
		return False
