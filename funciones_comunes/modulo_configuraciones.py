
import PySimpleGUI as sg
import string
import json


def imprimir_configuraciones():
    ''' imprime la ventana para configurar el nivel, el tiempo a jugar, la cantidad de fichas por tecla y la cantidad de puntos
    que se obtiene por usar cada una. Guarda los valores indicados en un json para devolverle los datos al programa ppal en el
    mismo'''
    def aviso():
        ''' mensaje que aparece cuando se quiere guardar en los recuadros de las fichas una letra o un numero
        negativo'''
        sg.popup('La cantidad de fichas y su puntaje debe ser un numero mayor igual a 0')

    def aviso_2():
        '''mensaje que aparece si se quiere cerrar la ventana de configuraciones y no se eligio la dificultad
        del nivel'''
        sg.popup('Por favor, elija el nivel de dificultad con el cual quiere jugar')
    def defino_tiempo(dific):
        '''asocia el velor de la cantidad de tiempo de juego(parametro de entrada), con la dificultas seleccionada en
        la ventana (variable de entrada)'''
        if dific=='Facil':
            val='120'
        elif dific=='Medio':
            val='100'
        else:
            val='60'
        return val
    def aviso_3():
        '''mensaje que aparece si no se encuantran los archivos necesarios para abrir la ventana'''
        sg.popup('No se ha encontrado el archivo correspondiente para abrir esta ventana')

    letras='A B C D E F G H I J K L LL M N Ñ O P Q R RR S T U V W X Y Z'.split()

# Abro archivo con los datos predefinidos
    try:
        arch=open('./datos/configuracion_guardada.txt', 'r')
    except FileNotFoundError:
        aviso_3()
    lista_guardada=[]
    lista_guardada= json.load(arch)
    arch.close()
    list_datos_letras=[]
    lista_col1=[]
    lista_claves=[]
    i=0
    for x in letras[0:15]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_claves.append([clave_cant,clave_val])
#        print(lista_claves , 'trato de imprimir lista de clave')  ta perfecto
        lista_col1.append([sg.Text(x, size=(2,1)), sg.Text('Cant. de fichas:'), sg.InputText(lista_guardada[i]['cant'], size=(4,1), key=clave_cant), sg.Text('valor de c/u:'), sg.InputText(lista_guardada[i]['pun'], size=(4,1), key=clave_val)])
        i=i+1
    lista_col2=[]
    for x in letras[15:29]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_claves.append([clave_cant,clave_val])
        lista_col2.append([sg.Text(x, size=(3,1)), sg.Text('Cant. de fichas:'), sg.InputText(lista_guardada[i]['cant'],size=(4,1), key=clave_cant), sg.Text('valor de c/u:'),sg.InputText(lista_guardada[i]['pun'], size=(4,1), key=clave_val)])
        i=i+1
    nivel_def=lista_guardada[len(lista_guardada)-1]['letra']
    tiem_def=lista_guardada[len(lista_guardada)-1]['cant']

    layout_config=[[sg.Text('Dificultad:'),sg.InputCombo(values=('Facil','Medio','Dificil'),key='difi',default_value=nivel_def,enable_events=True)],
                [sg.Text('Tiempo en segundos:'),sg.Text(tiem_def,key='tiem', size=(3,1)), sg.Text('Segundos')],
                [sg.Text('Cantidades de letras y puntos:')],
                [sg.Column(lista_col1),sg.Column(lista_col2)],
                [sg.Button('Guardar'),sg.Button('Restaurar Valores')]
                ]
    windowconf = sg.Window('Configuracion').Layout(layout_config)
    dic_aux={}
    lista_aux=[]
    lista_originales=[]
    j=''
    while True:
        evento,valores = windowconf.Read()
        list_datos_letras=[]
        dif_aux= valores['difi']
        if dif_aux!= '':
            tiempo=windowconf.FindElement('tiem')
            tiempo.Update(defino_tiempo(dif_aux))
        if evento=='Guardar':
            for i in lista_claves:
                try:
                    if len(i[0])==2:
                        j=i[0][0]
                        dic_aux['letra']=j
#                        try:
                        dic_aux['cant']=int(valores[i[0]])
                        dic_aux['pun']=int(valores[i[1]])
                        if dic_aux['cant']<0:
                            raise ValueError
                        elif dic_aux['pun']<0:
                            raise ValueError
#                        dic_aux={}
                    else:
                        j=i[0][0:2]
                        dic_aux['letra']=j
                        dic_aux['cant']=int(valores[i[0]])
                        dic_aux['pun']=int(valores[i[1]])
                        if dic_aux['cant']<0:
                            raise ValueError
                        elif dic_aux['pun']<0:
                            raise ValueError
#                        list_datos_letras.append(dic_aux)
#                        dic_aux={}
                except ValueError:
                    aviso()
                    list_datos_letras=[]
                else:
                    list_datos_letras.append(dic_aux)
                    dic_aux={}
#            print(list_datos_letras, 'esta es las lista de datos')
            if len(list_datos_letras) == 29:


                dif_aux= valores['difi']
                if dif_aux== '':
                    aviso_2()
                else:
                    tiempo=defino_tiempo(dif_aux)
                    dic_aux={'letra': dif_aux, 'cant':int(tiempo), 'pun':''}
                    try:
                        archivo=open('./datos/configuracion_guardada.txt','w')
                    except FileNotFoundError:
                        aviso_3()
                    list_datos_letras.append(dic_aux)
                    json.dump(list_datos_letras,archivo)
                    archivo.close()
                    dic_aux={}
                    break
        elif evento=='Restaurar Valores':
            try:
                arch=open('./datos/configuracion_original_fichas.txt', 'r')
            except FileNotFoundError:
                aviso_3()
            lista_originales= json.load(arch)
            arch.close()
            k=0
            for i in lista_claves:
                casillero= windowconf.FindElement(i[0])
                casillero.Update(lista_originales[k]['cant'])
                casillero= windowconf.FindElement(i[1])
                casillero.Update(lista_originales[k]['pun'])
                k=k+1
        elif evento == None:
            break
    windowconf.Close()
