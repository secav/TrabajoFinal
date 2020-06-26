import PySimpleGUI as sg


def imprimir_reglas():

    '''esta funcion abre el archivo donde se encuentran las reglas del juego y las imprime en una ventana nueva
    tiene un boton para volver al tablero'''

    reglas=open('arch_reglas.txt','r')
    imprimir= lambda linea: reglas.read()

    layout = [[sg.Text(reglas.read())],
            [sg.Button('Volver',button_color=('white','black'),key='volver')]
            ]
    window = sg.Window('Reglas',layout)
    event, values = window.Read()
