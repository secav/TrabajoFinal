import PySimpleGUI as sg
import json
import time

def aviso():
    '''mensaje que aparece si no se encuantran los archivos necesarios para abrir la ventana'''
    sg.popup('No se ha encontrado el archivo correspondiente para abrir esta ventana')

def guardar_ranking(puntaje_ult, nivel_ult):
    '''entran el nivel y el puntaje que pobtuvo el jugador en la ultima partida jugada y lo guarda en el archivo
    que tiene todos los datos guardados'''


    def ordenar_lista(aux_lista):
        '''ordena la lista de datos segun el puntaje de mayor a menor'''
        aux_lista=sorted(aux_lista, key= lambda x:x[1], reverse=True)
        return aux_lista

    try:
        archivo= open('./datos/rankin.txt','r')
    except FileNotFoundError:
        aviso()
    lista_puntajes=[]
    aux_lista=[]
    aux_tupla=[]
    lista_puntajes=json.load(archivo)
    archivo.close()
    fe= time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    fecha=fe[4:22]
    dic_datos_ult={'fecha':fecha,'puntaje':int(puntaje_ult),'nivel':nivel_ult}
    lista_puntajes.append(dic_datos_ult)
    for i in lista_puntajes:
        aux_tupla=[i['fecha'],i['puntaje'],i['nivel']]
        aux_lista.append(aux_tupla)
    aux_lista=ordenar_lista(aux_lista)
    j=0
    for i in lista_puntajes:
        i['fecha']=aux_lista[j][0]
        i['puntaje']=aux_lista[j][1]
        i['nivel']=aux_lista[j][2]
        j=j+1

    if len(lista_puntajes)>=11:
        lista_puntajes.pop()



    try:
        archivo= open('./datos/rankin.txt','w')
    except FileNotFoundError:
        aviso()
    json.dump(lista_puntajes,archivo)
    archivo.close()




def imprimir_rankin():

    '''imprime la ventana que muestra el top ten del juego con la fecha, el puntaje y el nivel en el cual se lograron.
    Se le ingresa de la ventana de tablero el puntaje de la ultima partida y el nivel en el cual se jugo. Si ese puntaje entra en
    el top ten lo guarda en un diccionario que despues sera agregado en el archivo rankin.txt que es donde se guarda toda esta
    informacion'''

    lista_colum1=[]
    lista_colum2=[]
    lista_colum3=[]

    try:
        archivo= open('./datos/rankin.txt','r')
    except FileNotFoundError:
        aviso()
    lista_puntajes=[]
    lista_puntajes=json.load(archivo)
    archivo.close()

    for i in lista_puntajes:
        lista_colum1.append([sg.Text(i['fecha'], size=(20,1))])
        lista_colum2.append([sg.Text(i['puntaje'], size=(10,1))])
        lista_colum3.append([sg.Text(i['nivel'], size=(10,1))])


    layout=[[sg.Text('Fecha', size=(21,1)),sg.Text('Puntaje',size=(13,1)),sg.Text('Nivel',size=(10,1))],
            [sg.Column(lista_colum1),sg.Column(lista_colum2),sg.Column(lista_colum3)],
            [sg.Button('Volver',image_filename="./imagenes/boton_naranja_chico.png",image_size=(82, 21),border_width=0,button_color=('black','black'))]
            ]


    window = sg.Window('Top 10').Layout(layout)


    while True:
        evento,valores = window.Read()
#        print(evento,valores)

        if evento=='Volver':
            break
        elif evento==None:
            break

    window.Close()

#guardar_ranking(100.5, 'dificil')
#imprimir_rankin()
