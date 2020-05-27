import PySimpleGUI as sg
import ajustes


#Layout de menu
layout_menu=[
[sg.Text('ScrabbleAR')],
[sg.Button('Jugar')],
[sg.Button('Configurar')],
[sg.Button('Salir')]
]

window = sg.Window('Menu',size=(250,250)).Layout(layout_menu)
event = window.Read()

while True:
    if event[0] == 'Jugar':
        print('A hacer')
        #ABRIR JUEGO
    elif event[0] == 'Configurar':
        ajustes.correr()
        event = window.Read()
    else:
        window.Close()
        break
