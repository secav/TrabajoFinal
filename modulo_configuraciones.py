import PySimpleGUI as sg
import string
import json


def correr():
    ''' imprime la ventana para configurar el nivel, el tiempo a jugar, la cantidad de fichas por tecla y la cantidad de puntos
    que se obtiene por usar cada una. Guarda los valores indicados en un json para devolverle los datos al programa ppal en el
    mismo'''

    letras='A B C D E F G H I J K L M N Ñ O P Q R S T U V W X Y Z'.split()
    print(letras, 'lista de letras')

    dic_datos_letras={}
    list_datos=[]
    lista_col1=[]
    lista_claves=[]
    for x in letras[0:14]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_claves.append([clave_cant,clave_val])

        lista_col1.append([sg.Text(x, size=(2,1)), sg.Text('Cant. de fichas:'), sg.InputText(size=(4,1), key=clave_cant), sg.Text('valor de c/u:'), sg.InputText(size=(4,1), key=clave_val)])
    lista_col2=[]
    for x in letras[14:27]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_col2.append([sg.Text(x, size=(2,1)), sg.Text('Cant. de fichas:'), sg.InputText(size=(4,1), key=clave_cant), sg.Text('valor de c/u:'),sg.InputText(size=(4,1), key=clave_val)])

    layout_config=[[sg.Text('Dificultad:'),sg.InputCombo(values=('Facil','Medio','Dificil'),key='difi')],
                [sg.Text('Tiempo en segundos:'),sg.InputCombo(values=('60','120','180'),key='tiem'), sg.Text('Segundos')],
                [sg.Text('Cantidades de letras y puntos:')],
                [sg.Column(lista_col1),sg.Column(lista_col2)],
                [sg.Button('Guardar'),sg.Button('Cerrar')]
                ]
    windowconf = sg.Window('Configuracion').Layout(layout_config)

    while True:
        evento,valores = windowconf.Read()
        print(evento,valores)
        print('a ver si sale la clave de la letra', valores['Ac'], 'y el valor', valores['Av'])
        print('valores de dificil', valores['difi'])
#        if valores['difi'] in dic_tiempo:
#            texto=windowconf.FindElement('cambio')
#            texto.Update(dic_tiempo[valores['difi']])
        if evento=='Guardar':
            for i in lista_claves:

            archivo=open('config.txt','w')
            json.dump(evento[1],archivo)
            archivo.close()
            print('evento 1',evento[1])
            evento = windowconf.read()
        elif evento=='Cerrar' or None:
            break
    windowconf.Close()
