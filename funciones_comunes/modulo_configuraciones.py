
import PySimpleGUI as sg
import string
import json


def imprimir_configuraciones():
    ''' imprime la ventana para configurar el nivel, el tiempo a jugar, la cantidad de fichas por tecla y la cantidad de puntos
    que se obtiene por usar cada una. Guarda los valores indicados en un json para devolverle los datos al programa ppal en el
    mismo'''
    def aviso():
        ''' mensaje que aparece cuando se quiere guardar en los recuadros de las fichas una letra o un numero
        negativo'''
        sg.popup('Los valores ingresados deben ser numeros mayores iguales a 0')

    def aviso_2():
        '''mensaje que aparece si se quiere cerrar la ventana de configuraciones y no se eligio la dificultad
        del nivel'''
        sg.popup('Por favor, elija el nivel de dificultad con el cual quiere jugar')
    def defino_tiempo(dific, t1, t2, t3):
        '''asocia el velor de la cantidad de tiempo de juego(parametro de entrada), con la dificultas seleccionada en
        la ventana (variable de entrada)'''
        if dific=='Facil':
            val=t1
        elif dific=='Medio':
            val=t2
        else:
            val=t3
        return val
    def aviso_3():
        '''mensaje que aparece si no se encuantran los archivos necesarios para abrir la ventana'''
        sg.popup('No se ha encontrado el archivo correspondiente para abrir esta ventana')

    letras='A B C D E F G H I J K L LL M N Ñ O P Q R RR S T U V W X Y Z'.split()

# Abro archivo con los datos predefinidos
    try:
        arch=open('./datos/configuracion_guardada.txt', 'r')
    except FileNotFoundError:
        aviso_3()
    try:
        arch_tiem=open('./datos/configuracion_tiemp.txt', 'r')
    except FileNotFoundError:
        aviso_3()
    lista_guardada=[]
    lista_tiemp=[]
    lista_guardada= json.load(arch)
    arch.close()
    lista_tiemp=json.load(arch_tiem)
    arch_tiem.close()

    list_datos_letras=[]
    lista_col1=[]
    lista_claves=[]
    i=0
    for x in letras[0:15]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_claves.append([clave_cant,clave_val])
#        print(lista_claves , 'trato de imprimir lista de clave')  ta perfecto
        lista_col1.append([sg.Text(x, size=(2,1)), sg.Text('Cant. de fichas:'), sg.InputText(lista_guardada[i]['cant'], size=(4,1), key=clave_cant), sg.Text('valor de c/u:'), sg.InputText(lista_guardada[i]['pun'], size=(4,1), key=clave_val)])
        i=i+1
    lista_col2=[]
    for x in letras[15:29]:
        clave_cant=''
        clave_val=''
        cla_cant=[x,'c']
        cla_val=[x,'v']
        clave_cant=clave_cant.join(cla_cant)
        clave_val=clave_val.join(cla_val)
        lista_claves.append([clave_cant,clave_val])
        lista_col2.append([sg.Text(x, size=(3,1)), sg.Text('Cant. de fichas:'), sg.InputText(lista_guardada[i]['cant'],size=(4,1), key=clave_cant), sg.Text('valor de c/u:'),sg.InputText(lista_guardada[i]['pun'], size=(4,1), key=clave_val)])
        i=i+1
    nivel_def=lista_guardada[len(lista_guardada)-1]['letra']
    tiem_def=lista_guardada[len(lista_guardada)-1]['cant']

    layout_config=[[sg.Frame('Dificultad:',[[sg.InputCombo(values=('Facil','Medio','Dificil'),key='difi',default_value=nivel_def,enable_events=True)]]),
                sg.Frame('Tiempo de la Partida:',[[sg.Text(tiem_def,key='tiem', size=(3,1)), sg.Text('Minutos')]])],
                [sg.Frame('Cantidades de letras y puntos:',
                [[sg.Column(lista_col1),sg.Column(lista_col2)]])],
                [sg.Frame('Configuracion de tiempo por nivel',[
                [sg.Text('Nivel: Facil', size=(11,1)), sg.InputText(lista_tiemp[0]['facil'],size=(3,1), key='tiemf'), sg.Text('minutos', size=(11,1)),sg.Text('Nivel: Medio', size=(11,1)), sg.InputText(lista_tiemp[0]['medio'],size=(3,1), key='tiemm'), sg.Text('minutos', size=(11,1)),sg.Text('Nivel: Dificil', size=(11,1)), sg.InputText(lista_tiemp[0]['dificil'],size=(3,1), key='tiemd'), sg.Text('minutos', size=(11,1))]])],
                [sg.Button('Guardar'),sg.Button('Restaurar Valores')]
                ]
    windowconf = sg.Window('Configuracion').Layout(layout_config)
    dic_aux={}
    lista_aux=[]
    lista_originales=[]
    j=''
    t1=3
    t2=2
    t3=1
    t_aux=False
    while True:
        evento,valores = windowconf.Read()
        list_datos_letras=[]
        dif_aux= valores['difi']
        if dif_aux!= '':
            t1=valores['tiemf']
            t2=valores['tiemm']
            t3=valores['tiemd']
            tiempo=windowconf.FindElement('tiem')
            tiempo.Update(defino_tiempo(dif_aux, t1, t2, t3))
        if evento=='Guardar':
            t=False

            try:
                for i in lista_claves:

                    if len(i[0])==2:
                        j=i[0][0]
                        dic_aux['letra']=j
    #                        try:
                        dic_aux['cant']=int(valores[i[0]])
                        dic_aux['pun']=int(valores[i[1]])
                        if valores[i[0]].isdigit() and valores[i[1]].isdigit():
                            t=True

                    else:
                        j=i[0][0:2]
                        dic_aux['letra']=j
                        dic_aux['cant']=int(valores[i[0]])
                        dic_aux['pun']=int(valores[i[1]])
                        if valores[i[0]].isdigit() and valores[i[1]].isdigit():
                            t=True

                    if t:
                        list_datos_letras.append(dic_aux)

                        dic_aux={}
                        t==False


            except ValueError:
                aviso()
                list_datos_letras=[]

            if len(list_datos_letras) == 29:
                t1=valores['tiemf']
                t2=valores['tiemm']
                t3=valores['tiemd']
                if t1.isdigit() and t2.isdigit() and t3.isdigit():
                    tiempo=windowconf.FindElement('tiem')
                    tiempo.Update(defino_tiempo(dif_aux, t1, t2, t3))
                    tiempo_guardar=defino_tiempo(dif_aux, t1, t2, t3)
                    dif_aux= valores['difi']
                    t_aux=True
                    dic_aux={'letra': dif_aux, 'cant':int(tiempo_guardar), 'pun':''}
                else:
                    aviso()
                    t_aux=False


                try:
                    archivo=open('./datos/configuracion_guardada.txt','w')
                except FileNotFoundError:
                    aviso_3()
                list_datos_letras.append(dic_aux)
                json.dump(list_datos_letras,archivo)
                archivo.close()
                print(t1,t2,t3, 'estos son los tiempos')
                lista_tiemp[0]['facil']=valores['tiemf']
                lista_tiemp[0]['medio']=valores['tiemm']
                lista_tiemp[0]['dificil']=valores['tiemd']
                print(lista_tiemp)

                try:
                    arch_tiem=open('./datos/configuracion_tiemp.txt','w')
                except FileNotFoundError:
                    aviso_3()
                json.dump(lista_tiemp, arch_tiem)
                print(lista_tiemp)
                dic_aux={}
                arch_tiem.close()
                if t_aux:

                    break
        elif evento=='Restaurar Valores':
            try:
                arch=open('./datos/configuracion_original_fichas.txt', 'r')
            except FileNotFoundError:
                aviso_3()
            lista_originales= json.load(arch)
            arch.close()
            k=0
            for i in lista_claves:
                casillero= windowconf.FindElement(i[0])
                casillero.Update(lista_originales[k]['cant'])
                casillero= windowconf.FindElement(i[1])
                casillero.Update(lista_originales[k]['pun'])
                k=k+1
        elif evento == None:
            break
    windowconf.Close()
#    return dificultad
#imprimir_configuraciones()
