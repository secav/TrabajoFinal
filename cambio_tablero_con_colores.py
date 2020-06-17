import PySimpleGUI as sg
import random
import sys
from modulo_reglas import imprimir_reglas

#Recibe la palabra y hace la comparacion con pattern,por ahora solo retorna True
#FALTA TODO EL TRAMO DE PATTERN
def check_pattern(): #def check_pattern(pal, nivel)
	'''esta funcion devuelve un boolean en true si la cadena es palabra, verbo o adjetivo dependiendo del nivel del juego'''
	#if nivel=='facil':
	#elif nivel=='medio':
	#else:
	return True

#El dic_importado adentro del for es redundante??
def crear_fichas():
	'''Genera una lista que contiene un diccionario con la cantidad y valor en puntos de cada letra y una lista que informa la cantidad de letras de las que hay mas de 0'''
	#x[0] es la letra, x[1] es la cantidad y x[2] es el valor en puntos
	letra=[('A',11,1),('B',3,3),('C',4,2),('D',4,2),('E',11,1),('F',2,4),('G',2,1),('H',2,4),('I',6,1),('J',2,4),('K',1,8),('L',4,1),('LL',1,8),('M',3,2),('N',5,1),('Ñ',1,8),('O',8,1),('P',2,3),('Q',1,8),('R',4,1),('RR',1,8),('S',7,1),('T',4,1),('U',6,1),('V',2,4),('W',1,8),('X',1,8),('Y',1,4),('Z',1,10)]
	dic_importado={}
	lista_disponibles=[]
	lista_completa=[]
	for x in letra:
		if x[1] > 0:
			lista_disponibles.append(x[0])
		dic_importado[x[0]]=[x[1],x[2]]
	lista_completa=[dic_importado,lista_disponibles]
	print(lista_completa)
	return lista_completa

#la funcion recibe el diccionario y retorna una letra
def letra_elegida(dic):
	'''La funcion recibe la lista de fichas y retorna una letra'''
	if dic[1]:
		llave_random=random.choice(dic[1])
		dic[0][llave_random][0] -=1
		if dic[0][llave_random][0] == 0:
			dic[1].remove(llave_random)
		return llave_random
	else:
		sg.popup('El diccionario esta vacio')
		sys.exit()

def letrasjuntas(a, b):
	'''devuelve true si las 2 letras ingresadas pueden estar juntas en una palabra'''
	es_vocal= lambda x: x in "aeiou"
	mixtas= ['qa','qe','qi','qo']
	juntas=''
	a=a.lower()
	b=b.lower()
	list_letras_juntas=[]
	dos_consonantes=['pr','pl','pt','br','bl','bs','tr','mp','mb','dr','dj','dy','cr','ct','ch','fr','fl','gr','gl']
	list_letras_juntas.append(a)
	list_letras_juntas.append(b)
	juntas=juntas.join(list_letras_juntas)
	print(juntas)
	valido=False
	if es_vocal(a):
		valido=True
		print('vocal')
	elif not(es_vocal(a)) and (es_vocal(b)):
		if not(juntas in mixtas):
			valido=True
			print('mixto')
	else:
		if (a=='r')or(a=='s'):
			valido=True
			print('r o s')
		elif (a=='n')and((b!='p')or(b!='b')):
			valido=True
			print('excepcion de la n')
		elif juntas in dos_consonantes:
			valido=True
			print('dos consonantes')
		else:
			valido=False
			print('no valido')
	return valido

def comprobar(elem):
	print('texto:',elem.GetText())
	if(elem.GetText()==''):
		print('si es')
		if(len(current_button_selected)>1)and not(current_button_selected[1].isdigit()):
			print('len',len(current_button_selected),'es digito',current_button_selected[1].isdigit())

			x=current_button_selected[0]+current_button_selected[1]
		else:
			x=current_button_selected[0]
		print('x:',x)
		elem.Update(x)

def comprobar_fichas(elem,event, indice, dic_letra_anterior, list_palabra, abajo, al_lado):
	'''esta funcion ve si se van poniendo las letras consecutivamente y las guarda en una lista '''
	continuar=True
	indice=indice+1
	if indice==0:
		dic_letra_anterior['pos']=indice
		dic_letra_anterior['tup']=event
		dic_letra_anterior['letra']=elem.GetText()
		list_palabra.append(dic_letras)
		print('primera letra')
	elif (event[0]==dic_letra_anterior['tup'][0]) and (event[1]==dic_letra_anterior['tup'][1]+1) and (abajo==False) and (letrasjuntas(dic_letra_anterior['letra'],elem.GetText())):
		al_lado=True
		dic_letra_anterior['pos']=indice
		dic_letra_anterior['tup']=event
		dic_letra_anterior['letra']=elem.GetText()
		list_palabra.append(dic_letras)
		boton_confirmar=True
		print('letra valida al costado')
	elif (event[0]==dic_letra_anterior['tup'][0]+1) and (event[1]==dic_letra_anterior['tup'][1]) and (al_lado==False) and (letrasjuntas(dic_letra_anterior['letra'],elem.GetText())):
		abajo=True
		dic_letra_anterior['pos']=indice
		dic_letra_anterior['tup']=event
		dic_letra_anterior['letra']=elem.GetText()
		list_palabra.append(dic_letras)
		boton_confirmar=True
		print('letra valida abajo')
	else:
		indice=indice-1
		continuar=False
		print('letra lejos o no valida')
#	dic_letra_anterior=dic_letras.copy()
	print(dic_letra_anterior)
	return indice, dic_letra_anterior, list_palabra, abajo, al_lado, continuar

def calcular_puntos(elem,current_button_selected,bolsa):
	'''Calcula el puntaje de una letra dependiendo de el color del casillero'''
	puntaje_rojo=0.5
	puntaje_azul=2
	if(len(current_button_selected)>1)and not(current_button_selected[1].isdigit()):
		x=current_button_selected[0]+current_button_selected[1]
	else:
		x=current_button_selected[0]
	print(x)
	if elem.ButtonColor[1] == 'red':
		puntos=bolsa[0][x][1]*puntaje_rojo
	elif elem.ButtonColor[1] == 'blue':
		puntos=bolsa[0][x][1]*puntaje_azul
	else:
		puntos=bolsa[0][x][1]
	return puntos

def button(name,key ):
	return (sg.Button(name,button_color=color_button,size=tam_button,key=key),name)
def definir(inicio,ini,inicial):
	posi=True
	lista=[]
	print(inicio)
	if (inicio):
		lista.append(ini.GetText())
		valor=inicial+1
		sig=window.FindElement(valor)
		sumo=1
		if(comprobar(sig,2)!=True):
			valor=inicial+10
			sig=window.FindElement(valor)
			sumo=10
			if(comprobar(sig,2)!=True):
				posi=False
			else:
				lista.append(sig.GetText())
		else:
			lista.append(sig.GetText())
		while(posi==True)and(valor+sumo<100):
			print('while')
			valor+=sumo
			sig=window.FindElement(valor)
			if(comprobar(sig,2)!=True):
				posi=False
			else:
				lista.append(sig.GetText())
		print('lista:',lista)
		pal=''
		for i in lista:
			pal=pal+i
		print(pal)
		sentence=parse(pal).split()
		for lis in sentence:
			for k in lis:
				if(k[1]== 'VB'):
					return 'verbo'
				elif (k[1]== 'NN'):
					return 'sustantivo'
				else:
					return 'otro'

	else:
		return 'No se encontro palabra'

def column():
	'''Retorna las filas de butones con los colores '''
	sin_color=('black','white')
	descuento=('white','red')
	premio=('white','blue')
	relleno1=('black','yellow')
	relleno2=('black','orange')
	rojo=[(14,0),(13,1),(12,2),(11,3),(10,4),(9,5),(5,9),(4,10),(3,11),(2,12),(1,13),(0,14),(14,7),(0,7),(7,14),(7,0)]
	azul=[(6,6),(8,6),(6,8),(8,8),(6,3),(7,4),(8,3),(3,6),(4,7),(3,8),(7,10),(6,11),(8,11),(11,6),(10,7),(11,8),(14,11),(14,3),(0,11),(0,3),(11,14),(3,14),(3,0),(11,0)]
	amarillo=[(13,4),(12,5),(12,9),(13,10),(2,5),(1,4),(2,9),(1,10)]
	naranja=[(5,2),(4,1),(9,2),(10,1),(5,12),(4,13),(9,12),(10,13)]
	tablero=[]
	for i in range(15):
		row = []
		for j in range(15):
			if((i==7)and(j==7))or(i,j)in amarillo:
				color=relleno1
			elif(i,j)in naranja:
				color=relleno2
			elif(i,j)in azul:
				color=premio
			elif(i==j)or(i,j)in rojo:
				color=descuento
			else:
				color=sin_color
			row.append(sg.Button('',  size=(3, 1),button_color=color, pad=(0, 0), key=(i,j)))
		tablero.append(row)

	return tablero

def reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas):
	'''Este metodo saca del tablero las letras que no cumplieron o que el usuario deseo borrar y permite volver a usar esas fichas  '''
	for i in fichas_recien_usadas:
		if i in fichas_usadas:
			 print('ESTA',i.GetText())
			 fichas_usadas.remove(i)
			 Uncheck_button(i)
	for k in tuplas_recien_usadas:
		lugar=window.FindElement(k)
		lugar.Update('')
		if k in lista_tuplas_usadas:
			lista_tuplas_usadas.remove(k)
	


#programa principal:

bolsa_fichas=crear_fichas()

lista_tuplas_usadas=[]
list_palabra=[]
indice=-1
abajo=False
al_lado=False
continuar=True
dic_letras={}
dic_letra_anterior={}


tam_celda =25
color_button = ('white','green')
tam_button = 3,1
but = lambda name : sg.Button(name,button_color=color_button,size=tam_button)
layout = [[sg.Button('INICIAR',button_color=('white','black'),key='inicio'),sg.Text('Turno:                          ',key='tur'),sg.Button('Configuracion',button_color=('white','black'),key='conf'),sg.Button('Ranking',button_color=('white','black'),key='rank'),sg.Button('Reglas',button_color=('white','black'),key='reglas'],
         [sg.Column(column()),sg.Button(image_filename="bolsa_roja.png",image_size=(100, 100),key="bolsa", border_width=0)],
        [but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas)),but(letra_elegida(bolsa_fichas))],
        [sg.Button('Borrar',button_color=('black','white'),key='borrador'),sg.Button('Verificar',button_color=('white','red'),key='verifica')]]

window = sg.Window('ScrabbleAR',layout)

listo=False
acumulador_puntos_jugador=0
sumador_puntos_jugador=0
button_selected = False
current_button_selected = ''
Check_button = lambda x: window.FindElement(x).Update(button_color=('black','yellow'))
Uncheck_button = lambda x:x.Update(button_color=('white','green'))
block_button=lambda x: x.Update(button_color=('black','red'))
fichas_usadas=[]
tuplas_recien_usadas=[]
fichas_recien_usadas=[]
while True:
    event, values = window.Read()
    print(event,values)
    if event is None or 'tipo' == 'Exit':
        break
    elif event =='inicio' and listo==False:
        listo=True
        desicion=['computadora','usuario']
        eleccion=random.choice(desicion)
        print(eleccion)
        texto=window.FindElement('tur')
        texto.Update('Turno:'+eleccion)
        inicio=window.FindElement('inicio')
        inicio.Update('Posponer')

    elif type(event)==tuple and not(ficha in fichas_usadas) and button_selected:
        print(event)
        elem=window.FindElement(event)

        sumador_puntos_jugador=sumador_puntos_jugador+calcular_puntos(elem,current_button_selected,bolsa_fichas)
        if not(event in lista_tuplas_usadas):
            elem=window.FindElement(event)

            print('imprimo el get texto')
            print(elem.GetText())
            indice, dic_letra_anterior, list_palabra, abajo, al_lado, continuar=comprobar_fichas(elem,event,indice, dic_letra_anterior, list_palabra, abajo, al_lado)
            print('salio')
            if continuar== True:
                comprobar(elem)
                print('ficha.GetText():',ficha.GetText())
                lista_tuplas_usadas.append(event)
                tuplas_recien_usadas.append(event)#son los lugares recien ocupados, si la palabra no es correcta tengo que sacar de estos lugares lo escrito
                fichas_usadas.append(ficha)
                fichas_recien_usadas.append(ficha)#son las fichas elegidas ese turno por el usuario, las tengo que devolver en caso de que sea incorrecto
                block_button(ficha)

    elif type(event)==str and (event!='inicio') and (event!='conf') and (event!='verifica') and (event!='borrador') :
        ficha=window.FindElement(event)
        print('tipo:',type(ficha))
        print(ficha.ButtonColor)

        if not(ficha in fichas_usadas):
            #Check_button(event)
            button_selected = True
            current_button_selected=event

   
    elif event == 'verifica': #en el sg.text iria: no se encontro la palabra, es palabra o es adjetivo, es verbo. dependiendo del nivel y de lo que suceda

        i=0
        dic_letra_anterior={}
        list_palabra=[]
        abajo=False
        al_lado=False
        continuar=True

        if (check_pattern()):
            acumulador_puntos_jugador+=sumador_puntos_jugador
            sumador_puntos_jugador=0
            print('Puntos jugador: '+str(int(acumulador_puntos_jugador)))
            indice=-1
            for i in fichas_recien_usadas:
                 i.Update(letra_elegida(bolsa_fichas))
                 Uncheck_button(i)
                 if i in fichas_usadas:
                     fichas_usadas.remove(i)
				
        else:
            indice=-1
            reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas)
        tuplas_recien_usadas=[]
        fichas_recien_usadas=[]
    elif event == 'reglas':
        print('holaaaaaaaaaaaaa')
        imprimir_reglas()
	
    elif event=='borrador':
        i=0
        dic_letra_anterior={}
        list_palabra=[]
        abajo=False
        al_lado=False
        continuar=True
        indice=-1
        reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas)
        tuplas_recien_usadas=[]
        fichas_recien_usadas=[]
  #hay que tener en cuenta que cuando borre no pierda el turno el jugador
 
