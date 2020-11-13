import os
import numpy as np
from obspy import read
import matplotlib.pyplot as plt

def clearConsole(): 
    if os.name == 'nt':  # Clean console for windows 
        _ = os.system('cls') 
    else: # Clean console for mac and linux(here, os.name is 'posix') 
        _ = os.system('clear') 

def readFiles(filesName):
    threechannels = None
    for fileName in filesName:
        if threechannels is None:
            threechannels = read(fileName) #Si es nula el threechannel le asigna el red
        else:
            threechannels += read(fileName) #SI no es nula se le agrega otro read del siguiente elemento
    return threechannels
    
def createFilter(filesName, filterType, showDefaultPlot):
    threechannels = readFiles(filesName) #Obtione los obpsy read de los nombre de los archivos
    tr = threechannels[0]
    
    if (showDefaultPlot): #Solo muestra una única vez la plot de los valores predeterminados
        print("\n")
        print("PLOT WITH DEFAULT VALUES")
        threechannels.plot(size=(800, 600))
        
    if filterType == "bandpass": #Al asignar bandpass es necesario otros datos de frecuencia
        tr.filter(filterType, corners=1, zerophase=True, freqmin = 1.0, freqmax = 5.0)
    else: 
        tr.filter(filterType, freq=1.0, corners=1, zerophase=True)
        
    print("\n")
    print("PLOT WITH FILTER (TYPE: " + filterType +")")
    threechannels.plot(size=(800, 600))
    
def createFourier(filesIndex):
    clearConsole()
    for index in filesIndex: #Por cada indice seleccionado obtiene el nombre del archivo y después lo grafica
        fileName = sacFiles[index - 1]
        st = read(fileName)
        y_values = np.fft.fft(st[0].data)
        
        no_of_datapoints = len(y_values)
        time_interval = 0.01 
        
        yf_values = 2.0/no_of_datapoints * np.abs(y_values[:no_of_datapoints//2])
        xf_values = np.fft.fftfreq(no_of_datapoints, d=time_interval)[:no_of_datapoints//2]
        
        fig, ax = plt.subplots()
        ax.plot(xf_values, yf_values, lw=0.3)
        ax.set_xlim([-1, 10])
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("Amplitude")
        ax.set_title(fileName + "'s Fourier graph")
        plt.show()

    
def passFilterMenu(filesIndex):
    clearConsole()
    filesName = filesSelected(filesIndex) #Obtiene los nombre de los archivos a partir de los indices seleccionados
    print("REALIZAR FILTRADO DE:")
    print(" 1.- Pasaaltas  (highpass)")
    print(" 2.- Pasabandas (bandpass)")
    print(" 3.- Pasabajas  (lowpass)")
    print("\n")
    howToUse()
    filterTypes = selectElements(3) #Le pone un limite de 3 para la seleccion
    for key, typeIndex in enumerate(filterTypes): #Dependiendo los tipos de filtros seleccionado pondra su filtro
        showDefaultPlot = True if key == 0 else False #Si el indice es 0 mostrara la plot con los valores inciailes
        if typeIndex == 1:
            createFilter(filesName, "highpass", showDefaultPlot)
        elif typeIndex == 2:
            createFilter(filesName, "bandpass", showDefaultPlot)
        elif typeIndex == 3:
            createFilter(filesName, "lowpass", showDefaultPlot)
    
def filesSelected(filesIndex): #Obtiene los nombre de los archivos
    files = []
    print("ARCHIVOS SELECCIONADOS:")
    for index in filesIndex:
        file = sacFiles[index - 1]
        files.append(file)
        print(" " + str(index) + ".- " + file) #Escribe en lista los nombres de los archivos
    print("\n")
    return files

def howToUse(): #Es una leyenda de intrucciones de uso
    print("INFORMACIÓN DE UTILIZACIÓN:")
    print("- Para seleccionar TODOS los elementos, introduzca cualquier carácter.")
    print("- Para seleccionar MÚLTIPLES elementos, separalos por comas (ejemplo: 1, 3, 5, 6)")

def selectElements(length): #FUnción básica de los menús
    inputValue = input("A SELECCIONAR: ")
    value = [x.strip() for x in inputValue.split(',')] #Separa los elementos al detectar un coma y el x.strip() elimina los espacios
    allFilesIndex = [(x + 1) for x  in np.arange(length)] #Crea un array con los indices de la longitud
    filesSelected = []

    if(len(value) == 1): 
        if(value[0].isnumeric()):
            if(int(value[0]) < length and int(value[0]) > 0): #Si el numero esta en el rango solo toma ese número
                filesSelected = [int(value[0])]
            else: #Selecciona todos los archivos disponibles
                filesSelected = allFilesIndex
        else: #Selecciona todos los archivos disponibles
            filesSelected = allFilesIndex
    else: #Selecciona los elementos en la lista que esten en los rangos de la  longitud
        filesSelected = [int(x) for x in value if int(x) in allFilesIndex]
        filesSelected = list(set(filesSelected)) #Elimina elementos duplicados
        
    return filesSelected
    
if __name__ == "__main__":
    sacFiles = []
    clearConsole()
    
    #Obtiene todos los archivos .sac y los agrega a sacFIles
    for file in os.listdir("./"):
        if file.endswith(".sac"):
            sacFiles.append(file)
    
    print("LECTURA Y GRÁFICACIÓN DE ARCHVIOS (.sac)")
    print("\n")
    for index, file in enumerate(sacFiles):
        print(" " + str(index + 1) + ".- " + file)
    print("\n") 
    howToUse()
    files = selectElements(len(sacFiles)) #Selecciona los archivos a utilizar
    
    #Después de seleccionar los archivo, pide que selecciones la acción a realizar
    clearConsole()
    filesSelected(files)
    print("SELECCIONA UNA OPCIÓN A REALIZAR: ")
    print(" 1.- Realizar filtros (highpass, bandpass y lowpass)")
    print(" 2.- Ver espectro de Fourier")
    selection = input("A SELECCIONAR: ")
    
    if(int(selection) == 1):
        passFilterMenu(files)
    else:
        createFourier(files)
    
    
    
    
    
    
    
    
    
    
        