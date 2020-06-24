import PySimpleGUI as sg

#funcion que intecambie las fichas

def creacion_ventana(fichas):
	tam_celda =25
	color_button = ('white','green')
	tam_button = 3,1
	But = lambda name,clave : sg.Button(name,button_color=color_button,size=tam_button,key=clave)
	layout=[[sg.Text('Seleccione las fichas a cambiar')],
	         [But(fichas[0].GetText(),"1"),But(fichas[1].GetText(),"2"),But(fichas[2].GetText(),"3"),But(fichas[3].GetText(),"4"),But(fichas[4].GetText(),"5"),But(fichas[5].GetText(),"6"),But(fichas[6].GetText(),"7")],
	         [sg.Button('Aceptar',key='accept'),sg.Button('Cancelar',key='cancel')]]
	window=sg.Window('Cambio de fichas',layout)
	Check_button = lambda x: window.FindElement(x).Update(button_color=('black','yellow'))
	Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('white','green'))
	cambio=[]
	while True:
		event,values=window.Read()
		print(event,values)
		if event == 'cancel' or event is None:
			print('siii')
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
