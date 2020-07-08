import PySimpleGUI as sg


def imprimir_reglas():

    '''esta funcion abre el archivo donde se encuentran las reglas del juego y las imprime en una ventana nueva
    tiene un boton para volver al tablero'''

    reglas=open('arch_reglas.txt','r')

    layout = [[sg.Text(reglas.read(), size=(100,30))],
            [sg.Button('Volver',button_color=('white','black'),key='volver')]
            ]
    window = sg.Window('Reglas').Layout(layout)
    event, values = window.Read()
    reglas.close()
    while True:

        if event == 'volver':
            break
        elif event == None:
            break

    window.close()
