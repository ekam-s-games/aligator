# aligator

*aligator* intenta ser una pequeña automatización de propósito específico, en apoyo a la gestión de hallazgos, ayudando
en la homologación (o replica) de un requerimiento creado en *QA-Team* hacia las herramientas *Mantis-BT* y *TestLink*.

Para lanzar el proceso basta con abrir una terminal de líneas de comandos en el mismo directorio del programa y
escribir la siguiente instrucción:

``` shell
python main.py
```

El proceso tomará como insumo el contenido del archivo de entrada `input.txt`. Extrayendo del mismo el número del
requerimiento creado en *QA-Team*, un listado de colaboradores interesados en participar en las actividades de pruebas
y una descripción o resumen del requerimiento necesarias en las herramientas *Mantis-BT* y *TestLink*.

Tomando los valores iniciales, pasará a consultar sobre bases de datos, establecidas en el archivo de configuración
`.config` (proporcionado por el *gestor de hallazgos* del equipo de trabajo), la existencia de un proyecto en
*Mantis-BT*; así mismo, un test plan en *TestLink*.

La inexistencia de alguno lanzará el proceso de automatización que replicará el requerimiento en dicha herramienta.

## `.config`

Es un archivo con estructura `JSON` que guarda la información para la conexión a bases de datos y credenciales para el
acceso a las herramientas *Mantis-BT* y *TestLink*. Por motivos de seguridad no es proporcionado en el repositorio.

## `input.txt`

Es un archivo con estructura específica para el proceso. Mantener el orden y el contenido para cada línea en el archivo
es importante para el correcto funcionamiento del producto.

La primera línea guardará un entero positivo; este representa el número hijo entregado al requerimiento en *QA-Team*.
La segunda línea guardará un listado de nombres de usuarios (separados por espacios) que representan a los interesados
en participar en las actividades de pruebas. Desde la tercera línea (en adelante) se guardará la descripción o resumen
del requerimiento.

## Prerrequisitos

### Paquetes

El proceso necesita las herramientas `Selenium` y `PyMySQL`. Ambos listados en el archivo `requirements.txt`.

Para instalarlos, use la siguiente instrucción:

``` shell
pip install -r requirements.txt
```

### chromedriver

Por defecto el proyecto usa el navegador *Chrome*; por tal motivo buscará la solución `chromedriver.txt` en una carpeta
local llamada `tools`.

``` python
driver = webdriver.Chrome(executable_path=r'tools/chromedriver.exe')
```
