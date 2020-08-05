import PySimpleGUI as sg

#funcion que intecambie las fichas

def creacion_ventana(fichas):
	'''Esta funcion recibe las fichas del jugador y crea una ventana con las mismas de manera que el jugador pueda seleccionar
	las que desea intercambiar por otras aleatorias de la bolsa de fichas. La funcion devuelve una lista vacia en caso de
	que el jugador haya presionado el boton cancelar o la cruz para cerrar la ventana; si ninguna de las cosas sucedio
	devuelve una lista con las fichas que el jugador desea intercambiar'''
	tam_celda =25
	color_button = ('black','#b8b8b8')

	tam_button = 3,1
	But = lambda name,clave : sg.Button(name,button_color=color_button,size=tam_button,key=clave)
	layout=[[sg.Text('Seleccione las fichas a cambiar')],
	         [But(fichas[0].GetText(),"1"),But(fichas[1].GetText(),"2"),But(fichas[2].GetText(),"3"),But(fichas[3].GetText(),"4"),But(fichas[4].GetText(),"5"),But(fichas[5].GetText(),"6"),But(fichas[6].GetText(),"7")],
	         [sg.Button('Aceptar',key='accept',image_filename="./imagenes/boton_naranja_chico.png",image_size=(82, 21),border_width=0,button_color=('black','black')),sg.Button('Cancelar',key='cancel',image_filename="./imagenes/boton_naranja_chico.png",image_size=(82, 21),border_width=0,button_color=('black','black'))]]
	window=sg.Window('Cambio de fichas',layout)
	Check_button = lambda x: window.FindElement(x).Update(button_color=('black','yellow'))
	Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('black','#b8b8b8'))
	cambio=[]
	while True:
		event,values=window.Read()

		if event == 'cancel' or event is None:
			
			cambio=[]
			break

		elif type(event)==str and event!='cancel' and event!='accept':
			if(int(event) in cambio):
				Uncheck_button(event)
				event=int(event)
				cambio.remove(event)
			else:
				Check_button(event)
				event=int(event)
				cambio.append(event)
		elif event=='accept':
			break
	window.Close()

	return cambio
