import PySimpleGUI as sg
from pattern.es import spelling,lexicon,tag
import random
import sys
from modulo_reglas import imprimir_reglas
import cambio_fichas as cf
from threading import Timer as timer
from modulo_configuraciones import imprimir_configuraciones
from modulo_rankin import imprimir_rankin

def imprimir_tablero():
    def check_pattern(palabra,nivel,conjunto_dificil):
    	'''esta funcion devuelve un boolean en true si la palabra es sustantivo, verbo o adjetivo y es correcta dependiendo del nivel de dificultad'''
    	palabra=palabra.lower()
    	if (palabra in spelling) or (palabra in lexicon):
    		tipo_palabra=tag(palabra)[0][1]
    		print(tipo_palabra)
    		if nivel=='facil':
    			return True
    		elif (nivel=='medio') and (tipo_palabra=='VB' or tipo_palabra=='NN'):
    			return True
    		elif (nivel=='dificil') and (tipo_palabra==conjunto_dificil):
    			return True
    		else:
    			return False
    	else:
    		return False

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
    def letra_elegida(dic,cambio=False,ficha_cambio=None):
    	'''La funcion recibe la lista de fichas y retorna una letra'''
    	if dic[1]:
    		llave_random=random.choice(dic[1])
    		print(llave_random)
    		if(ficha_cambio!=None):
    			print(ficha_cambio.GetText())
    		if(cambio==True)and(llave_random==ficha_cambio.GetText()):
    			print('si')
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
    	dos_consonantes=['pr','pl','pt','br','bl','bs','tr','mp','mb','dr','dj','dy','cr','ct','ch','cl','fr','fl','gr','gl']
    	list_letras_juntas.append(a)
    	list_letras_juntas.append(b)
    	juntas=juntas.join(list_letras_juntas)
    	valido=False
    	if es_vocal(a):
    		valido=True
    	elif not(es_vocal(a)) and (es_vocal(b)):
    		if not(juntas in mixtas):
    			valido=True
    	else:
    		if (a=='r')or(a=='s'):
    			valido=True
    		elif (a=='n')and((b!='p')or(b!='b')):
    			valido=True
    		elif juntas in dos_consonantes:
    			valido=True
    		else:
    			valido=False
    	return valido

    def comprobar(elem):
    	'''Comprueba si el casillero no tiene ninguna letra todavia, y en ese caso actualiza el casillero con el nuevo valor '''
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
    	'''esta funcion ve si se van poniendo las letras consecutivamente, ya sea vertical u horizontal, y las guarda en una lista
    	se le ingresa el elemento para conseguir la letra colocada, el evento(la tupla donde se coloco la letra), un indice que indica cuantas letras
    	se ingresaron hasta ese momento, un diccionario que guarda la informacion de la letra que fue ingresada antes de la actual, una lista donde se guardan
    	las letras que va ingresando el usuario(para luego obtener la palabra formada, y 2 variables booleanas que indican si la palabra esta siendo colocada
    	vertical u horizontalmente'''
    	continuar=True
    	indice=indice+1
    	if indice==0:
    		dic_letra_anterior['pos']=indice
    		dic_letra_anterior['tup']=event
    		dic_letra_anterior['letra']=elem.GetText()
    		list_palabra.append(dic_letra_anterior['letra'])
    	elif (event[0]==dic_letra_anterior['tup'][0]) and (event[1]==dic_letra_anterior['tup'][1]+1) and (abajo==False) and (letrasjuntas(dic_letra_anterior['letra'],elem.GetText())):
    		al_lado=True
    		dic_letra_anterior['pos']=indice
    		dic_letra_anterior['tup']=event
    		dic_letra_anterior['letra']=elem.GetText()
    		list_palabra.append(dic_letra_anterior['letra'])
    		boton_confirmar=True
    	elif (event[0]==dic_letra_anterior['tup'][0]+1) and (event[1]==dic_letra_anterior['tup'][1]) and (al_lado==False) and (letrasjuntas(dic_letra_anterior['letra'],elem.GetText())):
    		abajo=True
    		dic_letra_anterior['pos']=indice
    		dic_letra_anterior['tup']=event
    		dic_letra_anterior['letra']=elem.GetText()
    		list_palabra.append(dic_letra_anterior['letra'])
    		boton_confirmar=True
    	else:
    		indice=indice-1
    		continuar=False
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
    def column_tablero(nivel='facil'):
     	'''Retorna el diseño del tablero '''
     	sin_color=('black','white')
     	descuento=('white','red')
     	premio=('white','blue')
     	relleno1=('black','yellow')
     	relleno2=('black','orange')
     	rojo=[(14,0),(13,1),(12,2),(11,3),(10,4),(9,5),(5,9),(4,10),(3,11),(2,12),(1,13),(0,14)]
     	azul=[(6,6),(8,6),(6,8),(8,8),(6,3),(8,3),(3,6),(3,8),(6,11),(8,11),(11,6),(11,8),(14,11),(14,3),(0,11),(0,3),(11,14),(3,14),(3,0),(11,0)]
     	naranja=[(5,2),(4,1),(9,2),(10,1),(5,12),(4,13),(9,12),(10,13),(13,4),(12,5),(12,9),(13,10),(2,5),(1,4),(2,9),(1,10)]
     	tablero=[]
     	datos_ext=[(14,7),(0,7),(7,14),(7,0)]
     	datos_int=[(4,7),(7,10),(10,7),(7,4)]
     	if(nivel=='facil'):
     		azul.extend(datos_ext)
     		azul.extend(datos_int)
     	elif(nivel=='medio'):
     		rojo.extend(datos_ext)
     		azul.extend(datos_int)
     	elif(nivel=='dificil'):
      		rojo.extend(datos_ext)
      		rojo.extend(datos_int)		
	  	
     	for i in range(15):
     		row = []
     		for j in range(15):
     			if((i==7)and(j==7)):
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





    def columna_bolsa(seg,menos):
    	'''Devuelve el diseño del tiempo y la bolsa de fichas que se le muestran al jugador'''
    	layout=[
    	[sg.T('Tiempo ')],
    	[sg.T(seg)],
    	[sg.T(' '  * 10)],
    	[sg.T(' '  * 10)],
    	[sg.Button(image_filename="bolsachica.png",image_size=(100, 100),key="bolsa", border_width=0)],
    	[sg.Text('Presione aqui para')],
    	[sg.Text('cambiar las fichas'),sg.Text('(3)',key='cant_cambio')]]
    	return layout
    	
    def columna_puntos():
        '''Devuelve el diseño de los puntajes, el de la computadora y el del jugador '''
        layout=[[sg.Text('Puntaje computadora')],
        [sg.Text('0', key='text_pun_comp')],
        [sg.T(' ')],
        [sg.T(' ')],
        [sg.Text('Puntaje jugador')],
        [sg.Text('0', key='text_pun_jug')],
        [sg.Text('Puntaje palabra actual')],
        [sg.Text('0',key='text_pun_pal')]]
        return layout
        
        
        
    	
		
		
    
    def columna_atril_computadora():
        '''Devuelve el diseño del atril de la computadora '''
        layout=[[but(''),but(''),but(''),but(''),but(''),but(''),but('')]]
        return layout
    
    def columna_atril_jugador():
        '''Devuelve el diseño del atril del jugador con sus fichas correspondientes '''
        layout=[[but(letra_elegida(bolsa_fichas),1),but(letra_elegida(bolsa_fichas),2),but(letra_elegida(bolsa_fichas),3),but(letra_elegida(bolsa_fichas),4),but(letra_elegida(bolsa_fichas),5),but(letra_elegida(bolsa_fichas),6),but(letra_elegida(bolsa_fichas),7)]]
        return layout

    def reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas):
    	'''Saca del tablero las letras que no cumplieron o que el usuario decidio borrar y permite volver a usar esas fichas  '''
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
    def timeout():
    	print('fin del juego')


    #programa principal:

    #tiempo_juego                   #esto viene importado
    #dic_configuracion              #esto viene importado
    nivel_dificultad='facil'        #esto viene importado

    bolsa_fichas=crear_fichas()
    conjunto_hard=''
    if(nivel_dificultad=='dificil'):
    	posibles_conjuntos=['NN','VB','JJ']
    	conjunto_hard=random.choice(posibles_conjuntos)
    	print('Juega con el conjunto: '+conjunto_hard)


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
    but = lambda name,clave=None : sg.Button(name,button_color=color_button,size=tam_button,key=clave)
    layout = [
             [sg.Button('INICIAR',key='inicio',size=(12,None)),sg.Button('Ranking',key='rank'),sg.Button('Reglas',key='reglas'),sg.Button('Terminar juego',key='terminar')],
             [sg.Text('Turno:                 ',key='tur')],
             [sg.Text(' '*60),sg.Column(columna_atril_computadora(),background_color='Black',size=(290,45 ))],
             [sg.Column(columna_puntos()),sg.Column(column_tablero()),sg.Column(columna_bolsa(60,0))],
            [sg.Text(' '*60),sg.Column(columna_atril_jugador(),background_color='Black',size=(290,45 ))],
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
    palabra=''
    fichas_jugador=[]
    for i in range(7):
    	fichas_jugador.append(window.FindElement(i+1))
    	print(i+1)

    cont_cambio=3
    while True:

        event, values = window.Read()
        print(event,values)
        if event is None or 'tipo' == 'Exit':
            break


        elif event =='inicio' and listo==False:
            listo=True
            desicion=['computadora','usuario']
            t = timer(3.0, timeout)
            t.start()
            eleccion=random.choice(desicion)
            print(eleccion)
            texto=window.FindElement('tur')
            texto.Update('Turno:'+eleccion)
            inicio=window.FindElement('inicio')
            inicio.Update('Posponer')


        if(listo==True): #si ya se apreto el boton iniciar se pueden utizar los otros botones del juego
           if type(event)==int:
                ficha=window.FindElement(event)
                print('tipo:',type(ficha))
                print('tipo:',ficha.GetText())
                print(ficha.ButtonColor)
                if not(ficha in fichas_usadas):
                   button_selected = True
                   current_button_selected=ficha.GetText()

           elif type(event)==tuple  and button_selected and not(ficha in fichas_usadas):
                print(event)
                elem=window.FindElement(event)
                sumador_puntos_jugador=sumador_puntos_jugador+calcular_puntos(ficha,current_button_selected,bolsa_fichas)
                text=window.FindElement('text_pun_pal')
                text.Update(sumador_puntos_jugador)
                if not(event in lista_tuplas_usadas):
                    elem=window.FindElement(event)
                    print('imprimo el get texto')
                    print(elem.GetText())
                    indice, dic_letra_anterior, list_palabra, abajo, al_lado, continuar=comprobar_fichas(ficha,event,indice, dic_letra_anterior, list_palabra, abajo, al_lado)
                    print('salio')
                    if continuar== True:
                        comprobar(elem)
                        print('ficha.GetText():',ficha.GetText())
                        lista_tuplas_usadas.append(event)
                        tuplas_recien_usadas.append(event)#son los lugares recien ocupados, si la palabra no es correcta tengo que sacar de estos lugares lo escrito
                        fichas_usadas.append(ficha)
                        fichas_recien_usadas.append(ficha)#son las fichas elegidas ese turno por el usuario, las tengo que devolver en caso de que sea incorrecto
                        block_button(ficha)

           elif event=='bolsa' and (cont_cambio>0):
                for i in range(7):
                    fichas_jugador.append(window.FindElement(i+1))
                    print(i+1)
                cambio=cf.creacion_ventana(fichas_jugador)
                print('lista cambio:')
                if len(cambio)>=1:
                   for i in cambio:
                        ficha_cambio=window.FindElement(i)
                        vieja=ficha_cambio
                        ficha_cambio.Update(letra_elegida(bolsa_fichas,True,ficha_cambio))
                        bolsa_fichas[0][vieja.GetText()][0] +=1 ###
                        texto=window.FindElement('cant_cambio')
                   cont_cambio-=1
                   nuevo='('+(str(cont_cambio))+')'
                   texto.Update(nuevo)

           elif event == 'verifica':
                print(list_palabra)
                palabra=palabra.join(list_palabra)
    #            print(palabra,'holaaaaaaaaaaa')
                if (check_pattern(palabra,nivel_dificultad,conjunto_hard)):
                    acumulador_puntos_jugador+=sumador_puntos_jugador
                    text=window.FindElement('text_pun_jug')
                    text.Update(acumulador_puntos_jugador)
                    sumador_puntos_jugador=0
                    text=window.FindElement('text_pun_pal')
                    text.Update(sumador_puntos_jugador)
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
                    sumador_puntos_jugador=0
                    text=window.FindElement('text_pun_pal')
                    text.Update(sumador_puntos_jugador)
                    i=0
                    dic_letra_anterior={}
                    list_palabra=[]
                    abajo=False
                    al_lado=False
                    continuar=True
                tuplas_recien_usadas=[]
                fichas_recien_usadas=[]

           elif event=='borrador':
                sumador_puntos_jugador=but
                text=window.FindElement('text_pun_pal')
                text.Update(sumador_puntos_jugador)
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

        elif event == 'reglas':
            imprimir_reglas()

        if event=='rank':
            imprimir_rankin(acumulador_puntos_jugador,'difi')
        if(event=='terminar'):
             break


    window.Close()
