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


    layout = [[sg.Multiline(reglas.read(), size=(100,30),font='Fixedsys 12', background_color=('black'))],
            [sg.Button('Volver',image_filename="./imagenes/boton_naranja_chico.png",image_size=(82, 21),border_width=0,button_color=('black','black'))]
            ]
    window = sg.Window('Reglas').Layout(layout)
    reglas.close()
    while True:
        event, values = window.Read()

        if event == 'Volver' or event == None:
            break


    window.close()
