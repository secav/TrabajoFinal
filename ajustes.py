import PySimpleGUI as sg
import string
import json
print('Hola'*2)


print()

def correr():
    #layout de configuracion
    letras=list(string.ascii_uppercase)
    letras.insert(14,'Ñ')
    dificultad={'Facil':180,'Medio':120,'Dificil':60}
    lista_col1=[]
    for x in letras[0:14]:
        lista_col1.append([sg.Text(x),sg.InputText(size=(4,1)),sg.InputText(size=(4,1))])
    lista_col2=[]
    for x in letras[14:27]:
        lista_col2.append([sg.Text(x),sg.InputText(size=(4,1)),sg.InputText(size=(4,1))])

    layout_config=[[sg.Text('Dificultad:'),sg.InputCombo(values=('Facil','Medio','Dificil'))],
    [sg.Text('Tiempo en segundos:               ')],
    [sg.Text('Cantidades de letras y puntos:')],
    [sg.Column(lista_col1),sg.Column(lista_col2)],
    [sg.Button('Guardar'),sg.Button('Cerrar')]
    ]

    windowconf = sg.Window('Configuracion').Layout(layout_config)
    
    while True:
        evento,valores = windowconf.Read()
        print(evento,valores)
        if evento=='Guardar':
            archivo=open('config.txt','w')
            json.dump(evento[1],archivo)
            archivo.close()
            evento = windowconf.Read()
        else:
            windowconf.Close()
            break
