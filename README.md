# HH-Generator

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

- Si no puedes abrir la interfaz gráfica, crea un nuevo archivo .py y pega este código.

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
        start_whole=[1,1],
        end_whole=[1,1],
        use_baseline_correction=False)
```

<br>

## Documentación (HH Class)

| Argumento                       | Descripción                                                                                                                                                                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| files_hpath: _String List_      | Son los paths de los archivos mas altos, como una azotea.                                                                                                                                                                                                               |
| files_lpath: _String List_      | Es una función del tipo callback que se llama cada vez que se hace un progreso en la manipulación de datos. Recibe la función un entero que es el porcentaje y un string que expresa la acción que se realiza.                                                          |
| folder: _String_                | Es el nombre del folder que deseas guardar las gráficas, automáticamente las guarda con el nombre de los archivos que se gráficarón                                                                                                                                     |
| segment_length: _int_           | Es un entero que se utiliza para saber cual es la longitud del segmento                                                                                                                                                                                                 |
| sampling_rate: _int_            | Es la velocidad de muestreo, entre mayor sea los datos de las gráfica serán menores                                                                                                                                                                                     |
| start_whole: _int List_         | Recibe una lista de 2 elementos enteros. Esta lista determinará cuantas muestras se quieren omitir al inicio de los datos. El primer elemento se aplicará a los archivos del sensor H. El segundo elemento se aplicará a los archivos del sensor L.                     |
| end_whole: _int List_           | Recibe una lista de 2 elementos enteros. Esta lista determinará cuantas muestras se quieren omitir al final de los datos. El primer elemento se aplicará a los archivos del sensor H. El segundo elemento se aplicará a los archivos del sensor L.                      |
| use_baseline_correction: _bool_ | Al ser falso, se omitirá el baseline correction y tomará tus datos en bruto para realizar el Welch Method, HHSR y el HVSR. Si es verdadero, realizará el baseline correction y el resultado de la correción será utiliza para realizar el Welch Method, HHSR y el HVSR. |
