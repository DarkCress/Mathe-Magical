#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tkinter import *
from tkinter.ttk import Progressbar #Para la barra de progreso
from tkinter import ttk #Para la barra de progreso
import time,random,threading
import winsound

random.seed(random.random())

Valores=[0,0,0,0]
Final=[0,0,0,0]
Resp=0   #Variable que almacena la respuesta para compararla con la seleccionada
Vidas=3
Score=0
Contador=0 #Contador de operaciones

def Play(cancion):
    winsound.PlaySound(cancion, winsound.SND_ASYNC | winsound.SND_LOOP)
Play("Intro.wav")

#------------------------------------ ------------------------------------ ------------------------------------

def GetValores():  #Funcion para obtener los valores a,b, cualesquiera y de los botones
    for i in range(4):
        Valores[i]=random.randint(1,100)
        
def Operaciones(Count):
    global Resp
    SumResp=Valores[0]+Valores[1]
    ResResp=Valores[0]-Valores[1]
    MultResp=Valores[0]*Valores[1]
    DivResp=Valores[0]/Valores[1]
    #print(Valores)
    SumRes=[[f"{Valores[0]} + {Valores[1]} = ___",SumResp], #sublistas, [[Texto,resp],[Text,Rep]]
            [f"%d + ___ = %d"%(Valores[0],SumResp),Valores[1]],
            [f"{Valores[0]} - {Valores[1]} = ___",ResResp],
            [f"{Valores[0]} - ___ = {ResResp}",Valores[1]]]
    Mult=[[f"{Valores[0]} x {Valores[1]} = ___",MultResp],
          [f"{Valores[0]} x ___ = {MultResp}",Valores[1]]]
    Div=[[f"{Valores[0]} / {Valores[1]} = ___",DivResp],
         [f"{Valores[0]} / ___ = {round(DivResp,3)}",Valores[1]]]
    
    a=0 #Varible para conocer que tipo de problema va a seleccionarse
    PosiblesRes=[Valores[2],Valores[3]] #Los posibles resultados que apareceran en los botones
    
    if Count<=10:  #Para sumas y restas
        a=random.randint(0,3)
        #print(a)
        canvas4.itemconfig(Operacion,text=SumRes[a][0])  #Se muestra el texto de la operacion
        PosiblesRes.append(SumRes[a][1])                 #Se agrega la respuesta a una lista de las opciones
        Resp=SumRes[a][1]
        Rtrampa=SumRes[a][1]-random.randint(7,28)        #Y se coloca una de trampa

    elif Count>10 and Count<=20:  #Para multiplicaciones
        a=random.randint(0,1)
        canvas4.itemconfig(Operacion,text=Mult[a][0])
        PosiblesRes.append(Mult[a][1])
        Resp=Mult[a][1]
        Rtrampa=Mult[a][1]-random.randint(7,28)
    else:   #Para divisiones
        a=random.randint(0,1)
        canvas4.itemconfig(Operacion,text=Div[a][0]) 
        PosiblesRes.append(round(Div[a][1],3))
        Resp=round(Div[a][1],3)
        Rtrampa=Div[a][1]-random.randint(7,28)
    
    #print(PosiblesRes) 
    
    if Rtrampa in PosiblesRes: #En caso de que la respuesta trampa esté repetida entre las opciones
        Rtrampa+=3
    PosiblesRes.append(Rtrampa) 
    #print(PosiblesRes) 

    for y in range(4): #Se acomodan las respuestas de forma aleatoria
        Final[y]=PosiblesRes[round(random.randint(0,len(PosiblesRes)-1),3)]
        PosiblesRes.remove(Final[y])
        
    boton_resp1.configure(text=Final[0]) #Cambiar los textos de los botones a las respuestas
    boton_resp2.configure(text=Final[1])
    boton_resp3.configure(text=Final[2])
    boton_resp4.configure(text=Final[3])
        
def start():
    winsound.PlaySound(None, winsound.SND_ASYNC)
    global Contador,Vidas,Score
    Contador=1
    Vidas=3
    Score = 0
    canvas1.pack_forget()
    canvas4.pack(fill = "both", expand = True)
    canvas4.itemconfig(Imagen,image =imagen_campo)
    canvas4.itemconfig(Operacion,text="")
    canvas4.itemconfig(ContVidas,text=f"Vidas: {Vidas}")
    Play("Battle.wav")  
    
    for anuncio in "Listos...","3","2","1","Go!":
        canvas4.itemconfig(Anunciador,text=anuncio)
        canvas4.update_idletasks()
        time.sleep(1)  
    canvas4.itemconfig(Anunciador,text="") #Para ocultar el anuncio
    GetValores()  #Obtener los valores para las operaciones
    Operaciones(Contador) #Mostrará la primera operacion a realizar 
    
    #print(Final)
    boton_resp1.place(x=100,y=500)  #Se colocan los botones en la pantalla
    boton_resp2.place(x=100,y=560)
    boton_resp3.place(x=350,y=500)
    boton_resp4.place(x=350,y=560)
    
    hilo1=threading.Thread(target=Hilo)  #Hilo para la barra de progreso
    hilo1.start()
#------------------------------------------ HILOS ----------------------------------------------
def HiloCont():
    global Score
    x=0
    
    canvas4.itemconfig(Operacion,text="")    #Oculta el texto de la operacion
    
    boton_resp1.place_forget()  #Se ocultan los botones para que no se presionen
    boton_resp2.place_forget()
    boton_resp3.place_forget()
    boton_resp4.place_forget()
    
    while True:
        time.sleep(1)
        x+=1
        
        if x==3:
            winsound.PlaySound(None, winsound.SND_PURGE)
            canvas4.pack_forget()
            canvas5.itemconfig(ScoreF,text=Score)
            canvas5.pack(fill = "both", expand = True) #Mostrar la puntuacion final
        elif x==6:
            canvas5.pack_forget()
            canvas1.pack(fill = "both", expand = True) 
            Play("Intro.wav") 
            break
            
def Hilo():
    i=0
    global Seguir
    Seguir=1
    while i<=100:
        if Seguir==0:  #Para hacer que se acabe el hilo
            break
        else:
            bar['value']+=1
            if bar['value']==100:  #Cuando se acabe el tiempo
                RestaVidas() # Resta una vida y se encarga de acabar este hilo en caso de ser necesario  
            time.sleep(0.1)
#---------------------------------------------   ---------------------------------------------          
def Respuesta(Ans):  #Metodo cuando se selecciona un boton
    global Resp, Contador,Score

    bonus=bar['value']
    bar['value']=0
    if Ans== Resp:  #Si se seleccionó la respuesta correcta
        Contador+=1
        Score= Score + 100 +(100-bonus)
        GetValores()    
        Operaciones(Contador)
    else:          #En caso contrario
        GetValores()    
        Operaciones(Contador)
        VamoAVer()

#---------------------------------------------   ---------------------------------------------     

        
def RestaVidas(): 
    global Vidas, Seguir
    bar['value']=0
    Vidas-=1  #Se resta una vida
    canvas4.itemconfig(ContVidas,text=f"Vidas: {Vidas}") #Se actualiza el texto
    
    if Vidas==0:  #ESTA PARTE ES CUANDO SE ACABEN LAS VIDAS
        Seguir=0  #Detener el hilo de la barra de progreso
        FinJuego() 
        
def VamoAVer():
    global Vidas, Seguir
    Vidas-=1
    canvas4.itemconfig(ContVidas,text=f"Vidas: {Vidas}") #Se actualiza el texto
    if Vidas==0:
        canvas4.itemconfig(Anunciador,text="¡Se acabó el tiempo!")
        hilo1=threading.Thread(target=HiloCont)  #Hilo para la barra de progreso
        hilo1.start()
        Seguir=0
        
def FinJuego():
    global Score
    canvas4.itemconfig(Anunciador,text="¡Se acabó el tiempo!")
    canvas4.itemconfig(Operacion,text="")    #Oculta el texto de la operacion
    
    boton_resp1.place_forget()  #Se ocultan los botones para que no se presionen
    boton_resp2.place_forget()
    boton_resp3.place_forget()
    boton_resp4.place_forget()
    time.sleep(3)               #Despues de un tiempo se regresará a la pantalla de inicio
    canvas4.pack_forget()
    winsound.PlaySound(None, winsound.SND_PURGE)
    canvas5.itemconfig(ScoreF,text=Score) #Se actualiza el texto de la puntuacion final
    canvas5.pack(fill = "both", expand = True) #Mostrar la puntuacion final
    time.sleep(3)
    canvas5.pack_forget()
    canvas1.pack(fill = "both", expand = True)
    Play("Intro.wav")  

# ---------------------------------------------   ---------------------------------------------  

def Instrucciones():  #Boton para mostrar las instrucciones
    canvas1.pack_forget()
    canvas2.pack(fill = "both", expand = True) 
    canvas2.itemconfig(ImagenInfo,image =imagen_info)
    
    hiloText=threading.Thread(target=AparecerTexto)  #Hilo para la barra de progreso
    hiloText.start()

def AparecerTexto():
    global STOP
    
    STOP=1
    texto="Bienvenido a Cristalia!,,un mundo donde hasta la magia tiene sus matemáticas.,,Ayuda a Mapi a vencer al malvado fantasma Ludociel,resolviendo los problemas que aparecerán en la pantalla,para que pueda conjurar sus hechizos.,,Pero ten cuidado porque solo tienes 3 vidas"
    x=texto.split(",")
    i=0
    textoo=""
    for oracion in x:
        for palabras in x[i]:
            if STOP==0:
                break
                
            time.sleep(0.02)
            textoo=textoo+palabras
            canvas2.itemconfig(Info_Jugar,text=textoo)
            canvas2.update_idletasks()
        i+=1
        textoo=textoo+" \n"
    
def Info():   #Boton para mostrar la informacion del juego
    canvas1.pack_forget()
    canvas3.pack(fill = "both", expand = True)
    
def Regresar():    #Boton para regresar al panel de inicio -------------
    global STOP
    STOP=0
    canvas2.pack_forget()
    canvas3.pack_forget()
    canvas1.pack(fill = "both", expand = True)   

    
#---------------------------------------- Ventana general ----------------------------------------------------
window= Tk()
window.title("Mathe-Magical")
window.geometry("650x650+300+0") #Define el ancho y alto de la ventana, asi como la posicion de la misma
window.resizable(0,0)

imagen_portada = PhotoImage(file = "Portada.png")
imagen_info = PhotoImage(file= "Creditos.png")
imagen_credit = PhotoImage(file= "Info.png")
imagen_campo = PhotoImage(file= "Campo.png")
imagen_score = PhotoImage(file= "Score.png")

#---------------------------------- Panel inicio -------------------------------------------------------------
canvas1 = Canvas( window, width = 650, 
                         height = 650) 
canvas1.create_image( 0, 0, image = imagen_portada, anchor = "nw")
boton_jugar=Button(canvas1,text="Jugar",width="18",command=start, font=("Helveltica",12))
boton_jugar.place(x=420,y=250)
boton_como=Button(canvas1,text="Como Jugar",width="18",command=Instrucciones, font=("Helveltica",12))
boton_como.place(x=420,y=300)
boton_acerca=Button(canvas1,text="Acerca de",width="18",command=Info, font=("Helveltica",12))
boton_acerca.place(x=420,y=350)


#--------------------------------- Pantalla como jugar ----------------------------------------------------------
canvas2 = Canvas( window, width = 650, 
                         height = 650) 
ImagenInfo= canvas2.create_image( 0, 0, image = imagen_info, anchor = "nw")
boton_regresar=Button(canvas2,text="Regresar",width="18",command=Regresar, font=("Helveltica",12))
boton_regresar.place(x=10,y=600)

Info_Jugar=canvas2.create_text( 20, 130, 
                    text="", fill="white",
                    anchor="nw",font=("Kristen ITC",15,"bold")) 

canvas1.pack(fill = "both", expand = True) 

#--------------------------------- Pantalla informacion ----------------------------------------------------------
canvas3= Canvas(window,width = 650,
                      height = 650)
canvas3.create_image( 0, 0, image = imagen_credit, anchor = "nw")
boton_regresar=Button(canvas3,text="Regresar",width="18",command=Regresar, font=("Helveltica",12))
boton_regresar.place(x=10,y=600)

CreadorT= canvas3.create_text( 325, 110, fill="white",
                        text="Desarrolladores", anchor="center",
                        font=("Ink Free",30,"bold"))
NombreT= canvas3.create_text( 325, 150, fill="white",
                        text="José Adrián Alcalá Calderón", anchor="center",
                        font=("Ink Free",20,"bold"))
NombreT2= canvas3.create_text( 325, 200, fill="white",
                        text="Juan Carlos Huerta Vasquez", anchor="center",
                        font=("Ink Free",20,"bold"))
CreadorT= canvas3.create_text( 325, 270, fill="white",
                        text="Ilustraciones", anchor="center",
                        font=("Ink Free",30,"bold"))
NombreT= canvas3.create_text( 325, 310, fill="white",
                        text="José Adrián Alcalá Calderón", anchor="center",
                        font=("Ink Free",20,"bold"))
MusicaT= canvas3.create_text( 325, 380, fill="white",
                        text="Música", anchor="center",
                        font=("Ink Free",30,"bold"))
CancionT= canvas3.create_text( 325, 420, fill="white",
                        text="Pokemon Diamond BGM Piano Medley - Pally", anchor="center",
                        font=("Ink Free",18,"bold"))


#---------------------------------- Pantalla Juego ---------------------------------------------------------------
canvas4= Canvas(window,width = 650,
                      height = 650)
Imagen=canvas4.create_image( 0, 0, image = imagen_portada, anchor = "nw")

style=ttk.Style()                                                          #Barra de progreso
style.theme_use('default')                                                 #
style.configure("black.Horizontal.TProgressbar",background='green')        #
bar=Progressbar(canvas4,length=400, style="black.Horizontal.TProgressbar") #
bar.place(x=125, y=20, height=30)                                               #Para la ubicacion de la barra
bar['value']=0  #Para aumentar el valor del progreso

ContVidas= canvas4.create_text( 300, 65, fill="black",
                        text=f"Vidas: {Vidas}", anchor="center",
                        font=("Ink Free",20))
Anunciador= canvas4.create_text( 300, 300, fill="black",
                        text="Listos...", anchor="center",
                        font=("Ink Free",45))
Operacion= canvas4.create_text( 300, 120, fill="black",
                        text="", anchor="center",
                        font=("Ink Free",45))

#---------------------------------- Pantalla Puntuacion Final --------------------------------------------------

canvas5= Canvas(window,width = 650,
                      height = 650)
Imagen_Score=canvas5.create_image( 0, 0, image = imagen_score, anchor = "nw")
Puntuacion= canvas5.create_text( 300, 150, fill="black",
                        text="Puntuación", anchor="center",
                        font=("Ink Free",45))
ScoreF= canvas5.create_text( 300, 200, fill="black",
                        text="", anchor="center",
                        font=("Ink Free",45))
#---------------------------------------------------------------------------------------------------------------
boton_resp1=Button(canvas4,text="Respuesta1",width="15",command= lambda:Respuesta(Final[0]), font=("Helveltica",18))
boton_resp2=Button(canvas4,text="Respuesta2",width="15",command= lambda:Respuesta(Final[1]), font=("Helveltica",18))
boton_resp3=Button(canvas4,text="Respuesta3",width="15",command= lambda:Respuesta(Final[2]), font=("Helveltica",18))
boton_resp4=Button(canvas4,text="Respuesta4",width="15",command= lambda:Respuesta(Final[3]), font=("Helveltica",18))

#----------------------------------           ---------------------------------------------------------------------
def Cerrar():
    winsound.PlaySound(None, winsound.SND_PURGE)
    window.destroy()

window.protocol("WM_DELETE_WINDOW", Cerrar)
window.mainloop()


# In[ ]:




