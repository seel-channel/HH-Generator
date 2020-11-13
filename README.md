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
        [low+"R1235.CG.e.mseed", low+"R1235.CG.n.mseed", low+"R1235.CG.z.mseed"],
        folder="9CG - R1235")

    #USING MERGED DATA
    file = "./data/ASCII merge/SNRA9510.091"
    HH( [file], None, 
        start_whole=[1,1], 
        end_whole=[1,1], 
        folder="SNRA9510",
        use_baseline_correction=False)

```
