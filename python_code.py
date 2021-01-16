import serial
import time
from pylab import *

#Se inicia comunicacin con Arduino 
ser = serial.Serial('COM3', baudrate=9600, timeout=1 )  ## Donde COM= puerto del arduino,  
                                                        #9600 baudios de Serial.begin,  timeout = timepo que recoge datos

time.sleep(3) #Se tiene un tiempo de espera para obtener el primer dato, ya que sin el , el primer dato obtiene basura 
Puntos =160 #Se Define el numero de datos que se quieren obtener en funcion del tiempo de medicin
ListaDatos= [0]*Puntos #Se crea una lista de la dimension de puntos.


def Valores(): # Se declara una funcion que arroje una lista con los datos que recibe de arduino
    ser.write(b'g') # Se manda al arduino la letra g para que lea datos cuando nosotros lo indiquemos 
    ArduinoDatos= ser.readline().decode().split('\r\n') #Se crea la variable donde se guardan los datos  donde se docodifica en codigo ASCII
    
    return ArduinoDatos[0] 

while 1:  #Se incializa un ciclo que siempre se cumple para estar en sintonia con el loop de arduino 
    
    Input= input('Empezar a tomar datos?') #Se declara una variable que pregunte al usuario si ya quiere tomar datos 
    
    if Input == 'y': #Si el usuario pone la letra y = si , entonces comienza  el conteo y analisis de datos 
        pendientes=[] #Se declara una lista vacia donde se guarden las pendientes
        maximos=[] #Se declara una lista vacia donde se guarden los maximos
        diastolica=[] #Se declara una lista vacia donde se guarden las presiones diastolicas,osea las presiones mas bajas
        sistolica=[] #Se declara una lista vacia donde se guarden las presiones sistolicas,osea las presiones mas altas
        for i in range(0,Puntos): #Se inicializa un ciclo donde se cambian los valores de voltaje a presion
            Dato=Valores()
            
            Dato=int(Dato) #Se cambia los valores tipo str a int
            ListaDatos[i]=(Dato-562.5555556)/3.08 +15 # Se hace la conversion y se guarda en una lista
        
        for i in range(1,Puntos): #Se inicializa un ciclo donde se guarden las pendientes de los datos
            m=(ListaDatos[i]-ListaDatos[i-1])/2 #Se hac la pendiente para cada valor
            pendientes.append(m) 
        for i in range(1,len(pendientes)):#Se crea un ciclo donde se analizan las pendientes
            if(pendientes[i]==0): #si la pendiente entre dos puntos es cero no hace nada
                continue     
            else: #si la pendiente es negativa y es mayor que la pendiente anterior se guardan esos valores de la lista de datos como maximos
                if(pendientes[i-1]/pendientes[i] < 0 and pendientes[i-1] > pendientes[i]):
                    maximos.append(ListaDatos[i])
        for i in range(len(maximos)):  # En estos dos for se guardan los  valores que pasen estas cotas y se guardan en dos listas , en la sistolia y diastolica
            if(maximos[i] < 130 ):
                sistolica.append(maximos[i])
        for i in range(len(maximos)):
            if(maximos[i] > 70  ):
                diastolica.append(maximos[i])
                
        
        
        plt.rcParams['figure.figsize'] = (7,7)  # En estas cuatro lineas unicamente imprimimos la grafica de la lista de datos
        t=arange(0,len(ListaDatos),1)
        plot(t,ListaDatos,'r')
        ylabe('voltaje (presion)',fontsize=14)
        xlabel('tiempo (100ms)',fontsize=14)
        grid(True)
        show() 
        
        #yprint(dataList)
        #print(maximos)
        print("presin diastolica %f " %diastolica[-1]) #se imprime el ultimo valor de la lista de diastolica
        print("presin sistolica %f"%sistolica[0]) #se imprime el primer valor de la lista de sistolica 
