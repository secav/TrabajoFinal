import PySimpleGUI as sg


def imprimir_reglas():

    '''esta funcion abre el archivo donde se encuentran las reglas del juego y las imprime en una ventana nueva
    tiene un boton para volver al tablero'''
    def aviso():
        '''mensaje que aparece si no se encuantran los archivos necesarios para abrir la ventana'''
        sg.popup('No se ha encontrado el archivo correspondiente para abrir esta ventana')

    try:
        reglas=open('./datos/arch_reglas.txt','r', encoding="utf8")
    except FileNotFoundError:
        aviso()

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
