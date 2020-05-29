import PySimpleGUI as sg
import random

def letra_elegida(letra):
	eleccion=random.choice(letra)
	letra.remove(eleccion)
	return eleccion

def comprobar(elem):
	print('texto:',elem.GetText())
	if(elem.GetText()==''):
		print('si es')
		elem.Update(current_button_selected)

def button(name,key ):
	return (sg.Button(name,button_color=color_button,size=tam_button,key=key),name)

def column():
	tablero=[]
	for i in range(10):
		row = []
		for j in range(10):
			row.append(sg.Button('',  size=(3, 1),button_color=('black','white'), pad=(0, 0), key=(i,j)))
		tablero.append(row)
	
	return tablero		
	
tam_celda =25
color_button = ('white','green')
tam_button = 3,1
but = lambda name : sg.Button(name,button_color=color_button,size=tam_button)
letra='A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
print(letra)
layout = [
        #[sg.Graph((500,500),(0,260),(260,0), key='_GRAPH_', background_color='white',change_submits=True, drag_submits=False)],
         [sg.Column(column())],
					
		#[sg.Button(' ',key=y,button_color=color_button,size=tam_button)  for x in range(10) for y in range(x+1,x+10)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(11,21)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(21,31)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(31,41)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(41,51)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(51,61)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(61,71)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(71,81)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(81,91)],
       # [sg.Button(' ',key=i,button_color=color_button,size=tam_button) for i in range(91,101)],
        [but(letra_elegida(letra)),but(letra_elegida(letra)),but(letra_elegida(letra)),but(letra_elegida(letra)),but(letra_elegida(letra))]]

window = sg.Window('Ejercicio1',layout)

button_selected = False
current_button_selected = ''
Check_button = lambda x: window.FindElement(x).Update(button_color=('white','blue'))
Uncheck_button = lambda x: window.FindElement(x).Update(button_color=('white','green'))
while True:
    event, values = window.Read()
    print(event,values)
    print(values)
    if event is None or 'tipo' == 'Exit':
        break
    if type(event)==tuple and button_selected:
        print(event)
        elem=window.FindElement(event)
        comprobar(elem)     
        
    if button_selected:
	    if event == current_button_selected:
		    Uncheck_button(event)
		    button_selected = False
		    current_button_selected = ''
    elif type(event)==str:
        Check_button(event)
        button_selected = True
        current_button_selected = event
        
