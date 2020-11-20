# HH-Generator

<br><br>
View HH Generator images on **https://felipemurguia.com**
<br><br>
<br>

## Creación del ambiente de trabajo

- Desactiva su ambiente de trabajo actual

```
    conda deactivate
```

- Crea el nuevo ambiente de trabajo

```
    conda create --name HHGenerator
```

- Activa el nuevo ambiente de trabajo

```
    conda activate HHGenerator
```

<br>

## Instalación de dependencias

- Una vez clonado o descargado el repositorio, posicionate en su dirección. Por ejemplo:

```
    cd '/home/felipe/Descargas/HH Generator'
```

- Instala pip para descargar las dependencias

```
    conda install pip
```

- Ahora descarga e instala las dependencias con el requirements.txt

```
    pip install -r requirements.txt
```

<br>

## Ejecución del programa

- Abrir la interfaz gráfica.

```
    python GUI.py
```

- Si no puedes abrir la interfaz gráfica, crea un nuevo archivo start.py y pega este código.

```python
from HH import HH

if __name__ == '__main__':
    #USING SPLITTED DATA
    high = "./data/MSEED/20/"
    low = "./data/MSEED/0/"
    HH( [high+"9CG.e.mseed", high+"9CG.n.mseed", high+"9CG.z.mseed"],
        [low+"R1235.CG.e.mseed", low+"R1235.CG.n.mseed", low+"R1235.CG.z.mseed"])

    #USING MERGED DATA
    file = "./data/ASCII merge/SNRA9510.091"
    HH( [file], None,
        start_whole=[0,0],
        end_whole=[0,0],
        use_baseline_correction=False)
    
    #USING DISORDENED DATA PATHS
    HH( [high+"9CG.z.mseed", high+"9CG.e.mseed", high+"9CG.n.mseed"],
        [low+"R1235.CG.e.mseed", low+"R1235.CG.z.mseed", low+"R1235.CG.n.mseed"],
        channel_order = [["Z", "EW", "NS"], ["EW", "Z", "NS"]])
```

<br>

## Documentación (HH Class)

ÍNDICE
 - Line 178-260: Se cargan los datos de cada sensor disponible
 - Line 372: Se grafíca los datos y el baseline
 - Line 392: Se grafíca los baseline y welch method
 - Line 407: Se grafíca los HVSR
 - Line 447: Se grafíca los HHSR

<br>

| Argumento                         | Descripción                                                                                                                                                                                                                                                             |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| files_hpath: _String List_        | Recibe una lista de 3 strings para la splitted data y una lista de 1 string para merged data. Son los paths de los archivos mas altos, como una azotea.                                                                |
| files_lpath: _String List_        | Recibe una lista de 3 strings para la splitted data y una lista de 1 string para merged data. Son los paths de los archivos mas bajos, como el sótano.                                                                |
| channel_order: _String List_      | Recibe una lista de 2 listas con 3 cadenas (strings). Se usa para cambiar el orden de los canales de los files_paths, permitiendo que puedas usar la informacion en cualquier orden. **Default:** [["NS", "EW", "Z"], ["NS", "EW", "Z"]]. **NS**: NORTH-SOUTH, **EW**: EAST-WEST, **Z**: VERTICAL                            |
| segment_length: _int_             | Es un entero que se utiliza para saber cual es la longitud del segmento                                                                                                                                                                                                 |
| sampling_rate: _int_              | Es la velocidad de muestreo, entre mayor sea los datos de las gráfica serán menores                                                                                                                                                                                     |
| start_whole: _int List_           | Recibe una lista de 2 elementos enteros. Esta lista determinará cuantas muestras se quieren omitir al inicio de los datos. El primer elemento se aplicará a los archivos del sensor H. El segundo elemento se aplicará a los archivos del sensor L.                     |
| end_whole: _int List_             | Recibe una lista de 2 elementos enteros. Esta lista determinará cuantas muestras se quieren omitir al final de los datos. El primer elemento se aplicará a los archivos del sensor H. El segundo elemento se aplicará a los archivos del sensor L.                      |
| use_baseline_correction: _bool_   | Al ser falso, se omitirá el baseline correction y tomará tus datos en bruto para realizar el Welch Method, HHSR y el HVSR. Si es verdadero, realizará el baseline correction y el resultado de la correción será utiliza para realizar el Welch Method, HHSR y el HVSR. |
| progress: _Function(int, string)_ | Es una función del tipo callback que se llama cada vez que se hace un progreso en la manipulación de datos. Recibe la función un entero que es el porcentaje y un string que expresa la acción que se realiza.                                                          |

