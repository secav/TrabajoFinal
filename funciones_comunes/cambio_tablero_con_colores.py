import PySimpleGUI as sg
from pattern.es import spelling,lexicon,tag
import random
import sys
from funciones_comunes.modulo_reglas import imprimir_reglas
import funciones_comunes.cambio_fichas as cf
from funciones_comunes.modulo_configuraciones import imprimir_configuraciones
from funciones_comunes.modulo_rankin import guardar_ranking
from funciones_comunes.modulo_posponer import guardar_posponer
from itertools import permutations
from time import sleep
import time
import json

def imprimir_tablero(pospuesto=False):
    def check_pattern(palabra,nivel,conjunto_dificil):
    	'''esta funcion devuelve un boolean en true si la palabra es sustantivo, verbo o adjetivo y es correcta dependiendo del nivel de dificultad'''
    	palabra=palabra.lower()
    	if (palabra in spelling) or (palabra in lexicon):
    		tipo_palabra=tag(palabra)[0][1]
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
    def crear_fichas(lista_importada):
    	'''Genera una lista que contiene un diccionario con la cantidad y valor en puntos de cada letra y una lista que informa la cantidad de letras de las que hay mas de 0'''
    	#x[0] es la letra, x[1] es la cantidad y x[2] es el valor en puntos
    	dic_importado={}
    	lista_disponibles=[]
    	lista_completa=[]
    	for x in lista_importada:
    		dic_importado[x['letra']]=[x['cant'],x['pun']]
    		if x['cant'] > 0:
    			lista_disponibles.append(x['letra'])
    	lista_completa=[dic_importado,lista_disponibles]
    	print(lista_completa)
    	return lista_completa

    #la funcion recibe el diccionario y retorna una letra
    def letra_elegida(dic,quien_cambia=None,ficha_cambio=None):
    	'''La funcion recibe la lista de fichas y retorna una letra, si la funcion recibe el parametro quien_cambia devuelve una ficha al diccionario de fichas'''
    	if dic[1]:
			
    		if quien_cambia!=None:
    			if quien_cambia=='usuario':
    				ficha_text=ficha_cambio.GetText()
    				dic[0][ficha_text][0]+=1
    				if dic[0][ficha_text][0]==1:
    					dic[1].append(ficha_text)
    			elif quien_cambia=='pc':
    				dic[0][ficha_cambio][0]+=1
    				if dic[0][ficha_cambio][0]==1:
    					dic[1].append(ficha_cambio)
    			
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

    def column_tablero(nivel='facil',tab=False):
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
      
        if (tab==False):
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
        else:   
            dic={}	 
            for i in tab:
                tup=(i[0][0],i[0][1])
                dic[tup]=i[1]  							        
            for i in range(15):
                row = []
                for j in range(15):
                    letra=''					
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
                    if (i,j) in dic.keys():
                       letra=dic[i,j]
                    row.append(sg.Button(letra,  size=(3, 1),button_color=color, pad=(0, 0), key=(i,j)))
                tablero.append(row)
			 
                
                
        return tablero

    def columna_timer():
        '''Devuelve el diseño del tiempo que se le muestra al jugador'''
        layout=[
        [sg.Text('TIEMPO',font='Heveltica 15')],
        [sg.Text('00:00:00',font='Heveltica 15',key='tiemp')],
        ]
        return layout





    def columna_bolsa(menos,cont_cambio):
    	'''Devuelve el diseño de la bolsa de fichas que se le muestran al jugador'''
    	cont=str(cont_cambio)
    	cont='('+cont+')'
    	layout=[[sg.T(' '  * 10)],
    	[sg.T(' '  * 10)],
    	[sg.T(' '  * 10)],
    	[sg.T(' '  * 10)],
    	[sg.Button(image_filename="./imagenes/bolsachica.png",image_size=(100, 100),key="bolsa", border_width=0)],
    	[sg.Text('Presione aqui para cambiar las fichas',font='Fixedsys 16',size=(15,None))],
    	[sg.Text(cont,key='cant_cambio',font='Fixedsys 16')]]
    	return layout

    def columna_puntos(compu,jugador):
        '''Devuelve el diseño de los puntajes, el de la computadora y el del jugador '''
        compu=str(compu)+'         '
        jugador=str(jugador)+'       '
        layout=[[sg.Frame('Puntaje computadora',[[sg.Text(compu, key='text_pun_comp',font='Fixedsys 16')]],font='Fixedsys 16',size=(15,None))],
        [sg.T(' ')],
        [sg.T(' ')],
        [sg.T(' ')],
        [sg.T(' ')],
        [sg.T(' ')],
        [sg.Frame('Puntaje jugador',[[sg.Text(jugador, key='text_pun_jug',font='Fixedsys 16')]],font='Fixedsys 16')],
        [sg.Frame('Puntaje ',[[sg.Text('palabra actual',font='Fixedsys 16')],[sg.Text('0                 ',key='text_pun_pal',font='Fixedsys 16')]],font='Fixedsys 16',size=(15,None))],
        ]
        return layout







    def columna_atril_computadora():
        '''Devuelve el diseño del atril de la computadora '''
        layout=[[but(''),but(''),but(''),but(''),but(''),but(''),but('')]]
        return layout

    def columna_atril_jugador(fichas_jugadorb=False):
        '''Devuelve el diseño del atril del jugador con sus fichas correspondientes '''
        if fichas_jugadorb==False:
           layout=[[but(letra_elegida(bolsa_fichas),1),but(letra_elegida(bolsa_fichas),2),but(letra_elegida(bolsa_fichas),3),but(letra_elegida(bolsa_fichas),4),but(letra_elegida(bolsa_fichas),5),but(letra_elegida(bolsa_fichas),6),but(letra_elegida(bolsa_fichas),7)]]
        else:
           layout=[[but(fichas_jugadorb[0],1),but(fichas_jugadorb[1],2),but(fichas_jugadorb[2],3),but(fichas_jugadorb[3],4),
           but(fichas_jugadorb[4],5),but(fichas_jugadorb[5],6),but(fichas_jugadorb[6],7)]]

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

    def palabra_pc(letras_pc,bolsa_fichas,dificultad,conj_dificil):
        '''La funcion recibe las fichas de la computadora, toma entre 3 y 7 letras y las permuta hasta encontrar una palabra. Luego retorna las fichas de la palabra en una lista y toma nuevas fichas'''
        palabra_encontrada=False
        cant_letras=[3,4,5,6,7]
        while palabra_encontrada==False:
            i=random.choice(cant_letras)
            cant_letras.remove(i)
            print(cant_letras)
            letras_permutadas = permutations(letras_pc,i)
            for x in letras_permutadas:
                lista_palabra=list(x)
                separador=''
                x=separador.join(x).lower()
                if check_pattern(x,dificultad,conj_dificil):
                    palabra=x
                    palabra_encontrada=True
                    break
            if not(cant_letras) and not(palabra_encontrada):
                print('no existen palabras')
                for x in range(7):
                    letras_pc[x]=letra_elegida(bolsa_fichas,'pc',letras_pc[x])
                cant_letras=[3,4,5,6,7]
        print('palabra de la pc= ',palabra)
        for x in lista_palabra:
            letras_pc.remove(x)
            letras_pc.append(letra_elegida(bolsa_fichas))
        print(letras_pc)
        print(lista_palabra)
        return lista_palabra

    def turno_palabra_pc(fichas_computadora,bolsa_fichas,nivel_dificultad,conjunto_hard,tuplas_usadas,inicia_pc=False):
        ''' Esta funcion genera una palabra llamando a la funcion palabra_pc y luego la ubica en el tablero de forma aleatoria'''
        acum_puntos_pc=0
        print(fichas_computadora)
        a_poner=palabra_pc(fichas_computadora,bolsa_fichas,nivel_dificultad,conjunto_hard)
        palabra_puesta=False
        while palabra_puesta==False:
            if not inicia_pc:
                posx_inicio=7
                posy_inicio=7
            else:
                posx_inicio=random.randrange(15)
                posy_inicio=random.randrange(15)
            boton_inicio=window.FindElement((posx_inicio,posy_inicio))
            tuplas_a_usar=[(posx_inicio,posy_inicio)]
            if boton_inicio.GetText()=='':
                que_sentido=random.choice(['derecha','abajo'])
                print(que_sentido)
                se_puede=False
                der=True
                abj=True
                while (der or abj) and palabra_puesta==False:
                    print('while')
                    print(str(posy_inicio))
                    print(str(posx_inicio))
                    if que_sentido=='abajo':
                        print('abj')
                        largo_palabra_pc=len(a_poner)
                        print(largo_palabra_pc)
                        if (posx_inicio+largo_palabra_pc-1)<15:
                            print('entro')
                            posx_aux=posx_inicio
                            for i in range(len(a_poner)-1):
                                print('i es '+str(i))
                                boton_aux=window.FindElement((posx_aux+i+1,posy_inicio))
                                print(boton_aux.GetText())
                                if boton_aux.GetText()!='':
                                    que_sentido='derecha'
                                    abj=False
                                    break
                                elif i == len(a_poner)-2:
                                    se_puede=True
                        else:
                            abj=False
                            que_sentido='derecha'
                        print(se_puede)
                        if se_puede:
                            boton_inicio.Update(text=a_poner[0])
                            acum_puntos_pc=acum_puntos_pc+calcular_puntos(boton_inicio,a_poner[0],bolsa_fichas)
                            i=0
                            for x in a_poner[1:]:
                                i+=1
                                tuplas_a_usar.append((posx_inicio+i,posy_inicio))
                                boton_aux=window.FindElement((posx_inicio+i,posy_inicio))
                                boton_aux.Update(text=x)
                                acum_puntos_pc=acum_puntos_pc+calcular_puntos(boton_aux,x,bolsa_fichas)
                            tuplas_usadas+=tuplas_usadas+tuplas_a_usar
                            palabra_puesta=True
                    elif que_sentido=='derecha':
                        print('der')
                        largo_palabra_pc=len(a_poner)
                        if (posy_inicio+largo_palabra_pc-1) < 15:
                            posy_aux=posy_inicio
                            for i in range(len(a_poner)-1):
                                boton_aux=window.FindElement((posx_inicio,posy_aux+i+1))
                                if boton_aux.GetText()!='':
                                    que_sentido='abajo'
                                    der=False
                                    break
                                elif i == len(a_poner)-2:
                                    se_puede=True
                        else:
                            der=False
                            que_sentido='abajo'
                        if se_puede:
                            boton_inicio.Update(text=a_poner[0])
                            acum_puntos_pc=acum_puntos_pc+calcular_puntos(boton_inicio,a_poner[0],bolsa_fichas)
                            i=0
                            for x in a_poner[1:]:
                                i+=1
                                tuplas_a_usar.append((posx_inicio,posy_inicio+i))
                                boton_aux=window.FindElement((posx_inicio,posy_inicio+i))
                                boton_aux.Update(text=x)
                                acum_puntos_pc=acum_puntos_pc+calcular_puntos(boton_aux,x,bolsa_fichas)
                            tuplas_usadas+=tuplas_a_usar
                            palabra_puesta=True
        turno_quien='usuario'
        texto=window.FindElement('tur')
        texto.Update('Turno:'+turno_quien)
        return acum_puntos_pc

    def cumple(primero, cas_inicio,tuplas):
        '''Devuelve True si la palabra que el jugador ingreso es la primera y, por lo tanto, una de sus letras se encuentra en el
        casillero de inicio; si no es la primera, tambien devuelve True. En caso de que no se cumpla ninguna de las dos
        posibilidades devuelve false'''
        if(primero==False):
           listo=False
           for i in tuplas:
              if i==cas_inicio:
                  listo=True
                  break
        else:
           listo=True
        return listo
        
    def obtener_tablero():
        tab=[]    #devuelve una lista de listas
        for i in range(15):
           for j in range(15):
              tup=(i,j)			   
              casillero=window.FindElement(tup)
              if(casillero.GetText()!=''):
                 elemento=[tup,casillero.GetText()]
                 tab.append(elemento)		
       ##[[ho,sa][sa,fd][]]
        for i in tab:
            for valor in i:			
                print(valor) 			

        return tab
      

		    


    #programa principal:
    fichas_jugador=[]
    #LEO EL ARCHIVO QUE VIENE DE CONFIGURACIONES CON LOS DATOS DE LAS LETRAS
    if(pospuesto==False):
        arch_configuraciones=open('./datos/configuracion_guardada.txt','r')
        lista_datos_letras=[]
        lista_datos_letras=json.load(arch_configuraciones)
        arch_configuraciones.close()
        max_tiempo=lista_datos_letras[29]['cant']
        nivel_dificultad=lista_datos_letras[29]['letra'].lower()
        lista_datos_letras.pop()
        bolsa_fichas=crear_fichas(lista_datos_letras)
        lista_tuplas_usadas=[]
        primero=False
        primera_vez=False
        acumulador_puntos_jugador=0
        acumulador_puntos_pc=0
        fichas_computadora=[]
        tablero=False
        for i in range(7):
            fichas_computadora.append(letra_elegida(bolsa_fichas))
        cont_cambio=3    
        fichas_jugadorb=False
        conjunto_hard=''
        if(nivel_dificultad=='facil'):
            palabras_permitidas='Todas'
        elif(nivel_dificultad=='medio'):
            palabras_permitidas='Verbos y Sustantivos'
        else:
    	    posibles_conjuntos=['NN','VB','JJ']
    	    conjunto_hard=random.choice(posibles_conjuntos)
    	    print('Juega con el conjunto: '+conjunto_hard)
    	    if(conjunto_hard=='NN'):
    		    palabras_permitidas='Sustantivos'
    	    elif(conjunto_hard=='VB'):
    		    palabras_permitidas='Verbos'
    	    else:
    		    palabras_permitidas='Adjetivos'
    	
    else:
        bolsa_fichas=pospuesto['bolsa_fichas']
        nivel_dificultad=pospuesto['nivel_dificultad']
        fichas_jugadorb=pospuesto['fichas_jugador']
        num=1
        for i in fichas_jugadorb:
            fic=sg.Button(i[0],key=num)
            fichas_jugador.append(fic)
            num+=1
        fichas_computadora=pospuesto['fichas_computadora']
        acumulador_puntos_pc=pospuesto['acumulador_puntos_pc']
        acumulador_puntos_jugador=pospuesto['acumulador_puntos_jugador']
        paused_time=pospuesto['paused_time']  
        cont_cambio=pospuesto['cont_cambio']
        lista_tuplas_usadas=pospuesto['lista_tuplas_usadas']
        max_tiempo=pospuesto['max_tiempo']
        primera_vez=pospuesto['primera_vez']
        primero=pospuesto['primero']
        palabras_permitidas=pospuesto['palabras_permitidas']
        tablero=pospuesto['tablero']
        conjunto_hard=pospuesto['conjunto_hard']
        start_time=pospuesto['start_time']
        turno_quien=pospuesto['turno_quien']
        		
            

    		
    #lista_tuplas_usadas=[]
    list_palabra=[]
    indice=-1
    abajo=False
    al_lado=False
    continuar=True
    dic_letras={}
    dic_letra_anterior={}

    if sys.platform == 'win32':
        atril_os=283
    else:
        atril_os=400
    casillero_inicio=(7,7)
    #primero=False
    tam_celda =25
    color_button = ('white','green')
    tam_button = 3,1
    but = lambda name,clave=None : sg.Button(name,button_color=color_button,size=tam_button,key=clave)
    layout = [
             [sg.Button('INICIAR',key='inicio',size=(12,None)),sg.Button('Terminar juego',key='terminar') ],
             [sg.Text('Tipos de palabras permitidas:'+palabras_permitidas,font='Fixedsys 16')],
             [sg.Text('Turno:                 ',key='tur',font='Fixedsys 16') ],
             [sg.Text(' '*64),sg.Column(columna_atril_computadora(),background_color='Black',size=(atril_os,45 )) ,sg.Text(' '*19),sg.Column(columna_timer())],
             [sg.Column(columna_puntos(acumulador_puntos_pc,acumulador_puntos_jugador)),sg.Column(column_tablero(nivel_dificultad,tablero)),sg.Column(columna_bolsa(0,cont_cambio))],
            [sg.Text(' '*64),sg.Column(columna_atril_jugador(fichas_jugadorb),background_color='Black',size=(atril_os,45 ))],
            [sg.Text(' '*64),sg.Button('Borrar',button_color=('black','white'),key='borrador'),sg.Text(' '*40),sg.Button('Verificar',button_color=('white','red'),key='verifica',disabled=True)]]


    window = sg.Window('ScrabbleAR',layout)
    #primera_vez=False
    paused=False
    current_time=0
    empezado=False #cuando se presiona el boton iniciar  pasa a True
    #acumulador_puntos_jugador=0
    sumador_puntos_jugador=0
    #acumulador_puntos_pc=0
    button_selected = False
    current_button_selected = ''
    Check_button = lambda x: window.FindElement(x).Update(button_color=('black','yellow'))
    Uncheck_button = lambda x:x.Update(button_color=('white','green'))
    block_button=lambda x: x.Update(button_color=('black','red'))
    fichas_usadas=[]
    tuplas_recien_usadas=[]
    fichas_recien_usadas=[]
    palabra=''
    #fichas_jugador=[]
    #fichas_computadora=[]
    if(pospuesto==False):
       for i in range(7):
          fichas_jugador.append(window.FindElement(i+1))
          print(i+1)

    #cont_cambio=3
    while True:
        if empezado and not paused:
            event, values = window.read(timeout=10)
            current_time = int(round(time.time() * 100)) - start_time
        else:
            event, values = window.read()
        if event is None or 'tipo' == 'Exit':
            break
        if event =='inicio' and  empezado:#se activo posponer
           print('Posponerrrr')
           paused=True
           paused_time = int(round(time.time() * 100))
           tablero=obtener_tablero()
           if(nivel_dificultad=='dificil'):
              guardar_posponer(turno_quien,start_time,fichas_jugador,fichas_computadora,acumulador_puntos_pc,acumulador_puntos_jugador,paused_time,nivel_dificultad,tablero,bolsa_fichas,cont_cambio,lista_tuplas_usadas,max_tiempo,primera_vez,primero,palabras_permitidas,conjunto_hard)
           else:
              guardar_posponer(turno_quien,start_time,fichas_jugador,fichas_computadora,acumulador_puntos_pc,acumulador_puntos_jugador,paused_time,nivel_dificultad,tablero,bolsa_fichas,cont_cambio,lista_tuplas_usadas,max_tiempo,primera_vez,primero,palabras_permitidas)
			   
           break


        elif event =='inicio' and not empezado:
            empezado=True
            inicio=window.FindElement('inicio')
            inicio.Update('Posponer')
            if(pospuesto==False):
               start_time = int(round(time.time() * 100))
               current_time = 0
               paused_time = start_time
               desicion=['computadora','usuario']
               turno_quien=random.choice(desicion)
               texto=window.FindElement('tur')
               texto.Update('Turno:'+turno_quien)
               if(turno_quien=="computadora"):
                   sleep(1)
                   sum_puntos_pc=turno_palabra_pc(fichas_computadora,bolsa_fichas,nivel_dificultad,conjunto_hard,lista_tuplas_usadas,primera_vez)
                   acumulador_puntos_pc=acumulador_puntos_pc+sum_puntos_pc
                   text=window.FindElement('text_pun_comp')
                   text.Update(int(acumulador_puntos_pc))
                   primero=True
                   primera_vez=True
               else:
                   paused = False
                   start_time = start_time + int(round(time.time() * 100)) - paused_time


        if(empezado==True): #si ya se apreto el boton iniciar se pueden utizar los otros botones del juego


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
                if not(event in lista_tuplas_usadas):
                    elem=window.FindElement(event)
                    print(bolsa_fichas)
#                    print('imprimo el get texto')
#                    print(elem.GetText())
                    indice, dic_letra_anterior, list_palabra, abajo, al_lado, continuar=comprobar_fichas(ficha,event,indice, dic_letra_anterior, list_palabra, abajo, al_lado)
#                    print('salio')
                    if continuar== True:
                        comprobar(elem)
#                        print('ficha.GetText():',ficha.GetText())

                        puntos_la_ficha=calcular_puntos(elem,current_button_selected,bolsa_fichas)
                        sumador_puntos_jugador=sumador_puntos_jugador+puntos_la_ficha
                        text=window.FindElement('text_pun_pal')
                        text.Update(int(sumador_puntos_jugador))

                        lista_tuplas_usadas.append(event)
                        tuplas_recien_usadas.append(event)#son los lugares recien ocupados, si la palabra no es correcta tengo que sacar de estos lugares lo escrito
                        fichas_usadas.append(ficha)
                        fichas_recien_usadas.append(ficha)#son las fichas elegidas ese turno por el usuario, las tengo que devolver en caso de que sea incorrecto
                        block_button(ficha)
                    if indice==1:
                        boton_verificar=window.FindElement('verifica')
                        boton_verificar.Update(disabled=False)

            elif event=='bolsa' and (cont_cambio>0)and len(fichas_recien_usadas)==0:
                for i in range(7):
                    fichas_jugador.append(window.FindElement(i+1))
#                    print(i+1)
                cambio=cf.creacion_ventana(fichas_jugador)
#                print('lista cambio:')
                if len(cambio)>=1:
                    for i in cambio:
                        ficha_cambio=window.FindElement(i)
                        vieja=ficha_cambio
                        ficha_cambio.Update(letra_elegida(bolsa_fichas,'usuario',vieja))
                        texto=window.FindElement('cant_cambio')
                    cont_cambio-=1
                    nuevo='('+(str(cont_cambio))+')'
                    texto.Update(nuevo)
                    turno_quien='computadora'
                    texto=window.FindElement('tur')
                    texto.Update('Turno:'+turno_quien)
                    sleep(1)
                    sum_puntos_pc=turno_palabra_pc(fichas_computadora,bolsa_fichas,nivel_dificultad,conjunto_hard,lista_tuplas_usadas,primera_vez)
                    acumulador_puntos_pc=acumulador_puntos_pc+sum_puntos_pc
                    primera_vez=True
                    primero=True
                    text=window.FindElement('text_pun_comp')
                    text.Update(int(acumulador_puntos_pc))

            elif event == 'verifica':
                print(list_palabra)
                palabra=palabra.join(list_palabra)
    #            print(palabra,'holaaaaaaaaaaa')
#                print('acaaaaaaaaaaa')
                print(check_pattern(palabra,nivel_dificultad,conjunto_hard), 'este es el chek pattern')
                print(cumple(primero,casillero_inicio,tuplas_recien_usadas), 'este es el cumple')
                print(palabra, 'esta es la palabra')
                if  not primera_vez:
                    if cumple(primero,casillero_inicio,tuplas_recien_usadas):
                       primero=True


                if (check_pattern(palabra,nivel_dificultad,conjunto_hard))and primero:
                    primera_vez=True
                    acumulador_puntos_jugador+=sumador_puntos_jugador
                    text=window.FindElement('text_pun_jug')
                    text.Update(int(acumulador_puntos_jugador))
                    sumador_puntos_jugador=0
                    text=window.FindElement('text_pun_pal')
                    text.Update(int(sumador_puntos_jugador))
#                    print('Puntos jugador: '+str(int(acumulador_puntos_jugador)))
                    indice=-1
                    boton_verificar=window.FindElement('verifica')
                    boton_verificar.Update(disabled=True)
                    for i in fichas_recien_usadas:
                        i.Update(letra_elegida(bolsa_fichas))
                        Uncheck_button(i)
                        if i in fichas_usadas:
                            fichas_usadas.remove(i)
                    turno_quien='computadora'
                    texto=window.FindElement('tur')
                    texto.Update('Turno:'+turno_quien)
                    sleep(1)
                    sum_puntos_pc=turno_palabra_pc(fichas_computadora,bolsa_fichas,nivel_dificultad,conjunto_hard,lista_tuplas_usadas,primera_vez)
                    acumulador_puntos_pc=acumulador_puntos_pc+sum_puntos_pc
                    text=window.FindElement('text_pun_comp')
                    text.Update(int(acumulador_puntos_pc))

                else:
                    if not primera_vez:
                       primero=False
                    indice=-1
                    boton_verificar=window.FindElement('verifica')
                    boton_verificar.Update(disabled=True)
                    reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas)
                    sumador_puntos_jugador=0
                    text=window.FindElement('text_pun_pal')
                    text.Update(int(sumador_puntos_jugador))

                tuplas_recien_usadas=[]
                fichas_recien_usadas=[]
                dic_letra_anterior={}
                list_palabra=[]
                abajo=False
                al_lado=False
                continuar=True
                i=0
                palabra=''


            elif event=='borrador':
                sumador_puntos_jugador=0
                text=window.FindElement('text_pun_pal')
                text.Update(int(sumador_puntos_jugador))
                i=0
                dic_letra_anterior={}
                list_palabra=[]
                abajo=False
                al_lado=False
                continuar=True
                indice=-1
                boton_verificar=window.FindElement('verifica')
                boton_verificar.Update(disabled=True)
                reinicio(fichas_recien_usadas,fichas_usadas,tuplas_recien_usadas,lista_tuplas_usadas)
                tuplas_recien_usadas=[]
                fichas_recien_usadas=[]



        if(event=='terminar'):
            guardar_ranking(acumulador_puntos_jugador,'difi')
            break
        window['tiemp'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                  (current_time // 100) % 60,
                                                                  current_time % 100))
        if(current_time//100)//60==max_tiempo:
            guardar_ranking(acumulador_puntos_jugador,'difi')
            if(acumulador_puntos_pc<acumulador_puntos_jugador):
               ganador='Felicitaciones, usted ha ganado'
            elif(acumulador_puntos_pc==acumulador_puntos_jugador):
                ganador='Se ha producido un empate'
            else:
                ganador='Usted ha perdido'

            sg.popup('Fin del juego:'+ganador)
            break


    window.Close()
