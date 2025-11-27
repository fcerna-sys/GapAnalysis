Usando Pytesseract para convertir imágenes en un sitio HTML por Armaiz Adenwala.

Descripción general

Utilizando la biblioteca de OCR Tesseract de Google, escanearemos imágenes de un conjunto de datos y crearemos un sitio web HTML con navegación. Abarcaremos diversos temas, como la biblioteca Pytesseract , la biblioteca Tesseract de Google , Makefiles , expresiones regulares y más. Esta publicación pretende servir como introducción al potencial de las redes neuronales mediante OCR básico.



Vea un vídeo del proyecto en acción aquí .



Siéntete libre de seguir consultando el repositorio de GitHub para este proyecto de OCR de Python. Los conjuntos de datos y el styles.cssarchivo están dentro de este repositorio.



Creando la estructura del proyecto

Cree el directorio raíz del proyecto:



$ mkdir python-ocr-tutorial

$ cd python-ocr-tutorial

mkdir python-ocr-tutorial: crea nuestro directorio raíz



cd python-ocr-tutorial: cambia el directorio actual a nuestro directorio de proyecto



Crea nuestras carpetas de proyecto:



$ mkdir html data utils

mkdir html: nuestra carpeta html donde se mostrará nuestro html



mkdir data:nuestra carpeta de datos donde estarán nuestras imágenes



mkdir utils:nuestro paquete de utilidades donde guardaremos todas nuestras funciones de utilidad



Crea nuestros archivos de proyecto:



$ touch utils/utils.py utils/\_\_init\_\_.py main.py requirements.txt Makefile

touch: comando que crea/actualiza la fecha de modificación de un archivo



touch utils/utils.py: crea nuestro archivo de utilidades donde vivirán nuestras funciones de utilidad



touch utils/\_\_init\_\_.py: le dice a Python que utilsdebe tratarse como un paquete



touch main.py: crea el archivo que llamará a nuestras funciones de utilidades



touch requirements.txt: crea el archivo que indica pipqué pip3paquetes necesitamos instalar



touch Makefile: crea el Makefile que nos ayudará a ejecutar tareas importantes como run, test, yclean



Configuración de nuestras bibliotecas

Primero, necesitaremos descargar Tesseract. Pytesseract, un contenedor para la biblioteca de Google. Esto significa que sirve como puente entre Python y Tesseract. Para que la biblioteca de Python funcione, es necesario instalar la biblioteca Tesseract siguiendo la guía de instalación de Google .



Añade requirements.txtlo siguiente:



pytesseract==0.3.2

pytesseract:Un contenedor para la biblioteca OCR Tesseract de Google que nos permite escanear imágenes y extraer esos datos en una cadena



Actualice su Makefile:



init:

&nbsp;	pip3 install -r requirements.txt

init: este es el nombre del comando que se puede llamar mediante $ Make init. El nombre puede ser cualquiera.



pip3 install -r requirements.txt: pip3es el instalador de paquetes de Python 3. (es posible que necesites usarlo pipsi no lo tienes python 3)



-r requirements.txtEsta es una opción obligatoria para \[nombre del archivo pip3]. El requirements.txtarchivo contiene la lista de dependencias que pip3deben instalarse. Puede ejecutar \[nombre del archivo] $ pip3 help installpara obtener más información.



Correr $ Make init:



$ Make init

pip3 install -r requirements.txt

Processing /Users/.../Caches/pip/...

...

Collecting Pillow

...

Installing collected packages: Pillow, pytesseract

Successfully installed Pillow-7.0.0 pytesseract-0.3.2

Nota: Al instalar dependencias de Python, sería ideal utilizar virtualenv, sin embargo, para esta guía no cubriremos eso.



Make generará un error si usas espacios en lugar de tabulaciones. Algunos IDE convierten automáticamente las tabulaciones en espacios. Tendrás que desactivar esta opción o usar " nanoo" vim.



Puedes verificar si el archivo es válido ejecutando $ cat -e -t -v Makefile. Si ves ^Iantes de cada línea, significa que es válido y usa tabulaciones. Si solo ves espacios, debes convertirlos en tabulaciones.





Si te diste cuenta, $ Make initse instala Pillowautomáticamente. Esto se debe a que pytesseractlo requiere y lo instala automáticamente. Puedes ver más información sobre las bibliotecas instaladas ejecutándolas pip3en $ pip3 show PACKAGE\_NAMEla terminal (no en la consola de Python):



$ pip3 show pytesseract

Name: pytesseract

Version: 0.3.2

...

Location: /usr/local/lib/python3.7/site-packages

Requires: Pillow

De esto, podemos ver que esta biblioteca requiere, Pillowque es una bifurcación de PILla biblioteca de imágenes de Python. Esta biblioteca nos permite pasar la ruta a una imagen pytesseracty procesarla automáticamente.



El problema con nuestro requirements.txtes que tiende a instalar diferentes Pillowversiones. Si este proyecto se configura en un dispositivo diferente, la Pillowdependencia instalará la versión más reciente. Si bien es recomendable usar la versión más reciente, la actualización de las dependencias debe hacerse intencionalmente, no automáticamente, para evitar que las aplicaciones fallen. Deberíamos desinstalar Pillow, actualizar nuestro requirements.txtpara instalar específicamente Pillow 7.0.0y ejecutar $ Make init.



Desinstalar Pillowusando el $ pip3 uninstall PACKAGE\_NAMEcomando:



$ pip3 uninstall Pillow

Uninstalling Pillow-7.0.0:

&nbsp; Would remove:

&nbsp;   /usr/local/lib/python3.7/site-packages/PIL/\*

&nbsp;   /usr/local/lib/python3.7/site-packages/Pillow-7.0.0.dist-info/\*

Proceed (y/n)? y

&nbsp; Successfully uninstalled Pillow-7.0.0

Actualizar requirements.txt:



pytesseract==0.3.2

Pillow==7.0.0

Instalar dependencias:



$ Make init

pip3 install -r requirements.txt

...

Collecting Pillow==7.0.0

...

Installing collected packages: Pillow

Successfully installed Pillow-7.0.0

Probando Tesseract

Antes de cubrir nuestro programa, debemos analizar de cerca tesseracty pytesseractcomprender el núcleo de nuestro proyecto.



Primero, complete la datacarpeta. Descargue la datacarpeta del repositorio de imagen a HTML y guarde el contenido en nuestra carpeta de datos. Esto significa que todas las jpgimágenes van dentro.python-ocr-tutorial/data/



Inicie Python con $ python3:



$ python3

Python 3.7.6 (default, Dec 30 2019, 19:38:28)

\[Clang 11.0.0 (clang-1100.0.33.16)] on darwin

Type "help", "copyright", "credits" or "license" for more information.

>>>

Nota: Lo utilizaré python3para esta guía; python(las versiones anteriores) también deberían funcionar.



Necesitamos decirle a Python que importe la pytesseractbiblioteca:



>>> import pytesseract

>>>

Si no vemos ningún error significa que hemos importado exitosamente pytesseract.



Si ve un error, es posible que deba instalar \[ Nombre del producto tesseract]. Para esta guía, he usado \[ Nombre del producto 4.1.1], que nos permite usar su nuevo motor LSTM de redes neuronales. \[Nombre del producto] pytesseractusará automáticamente el motor de OCR según la disponibilidad. Visite la guía de instalación de tessearct de Google .



La pytesseractbiblioteca proporciona un image\_to\_stringmétodo que permite pasar una ruta a una imagen o a un objeto de imagen. La biblioteca escaneará una imagen y devolverá el texto que reconoce. Si no se encuentra texto, no se devolverá nada. Podemos intentar escanear nuestra primera imagen del conjunto de datos ( ./data/python\_dataset\_01.jpg):



>>> pytesseract.image\_to\_string('./data/python\_dataset\_01.jpg')

'Chapter 1: Lorem\\n\\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nisi ...Praesent ut diam aliquet, dapibus felis in,'

>>>

Después de unos segundos, debería aparecer el texto de la imagen. Tenga en cuenta que el OCR no es perfecto; afortunadamente, nuestro conjunto de datos es ideal para el OCR, ya que está correctamente orientado y tiene un texto muy claro y consistente.



En esta guía no nos ocuparemos mucho de esto, pero tesseractnos permite configurar el modo de motor de OCR y el modo de segmentación de página que usaremos. Ejecutar $ tesseract --help-extrapara ver nuestras opciones:



$ tesseract --help-extra

\# ...

OCR options:

&nbsp; # ...

&nbsp; --psm NUM             Specify page segmentation mode.

&nbsp; --oem NUM             Specify OCR Engine mode.

Page segmentation modes:

&nbsp; 0    Orientation and script detection (OSD) only.

&nbsp; 1    Automatic page segmentation with OSD.

&nbsp; 2    Automatic page segmentation, but no OSD, or OCR. (not implemented)

&nbsp; 3    Fully automatic page segmentation, but no OSD. (Default)

&nbsp; 4    Assume a single column of text of variable sizes.

&nbsp; 5    Assume a single uniform block of vertically aligned text.

&nbsp; 6    Assume a single uniform block of text.

&nbsp; 7    Treat the image as a single text line.

&nbsp; 8    Treat the image as a single word.

&nbsp; 9    Treat the image as a single word in a circle.

&nbsp;10    Treat the image as a single character.

&nbsp;11    Sparse text. Find as much text as possible in no particular order.

&nbsp;12    Sparse text with OSD.

&nbsp;13    Raw line. Treat the image as a single text line,

&nbsp;      bypassing hacks that are Tesseract-specific.



OCR Engine modes:

&nbsp; 0    Legacy engine only.

&nbsp; 1    Neural nets LSTM engine only.

&nbsp; 2    Legacy + LSTM engines.

&nbsp; 3    Default, based on what is available.

\# ...

Desde aquí, podemos ver que tenemos muchas opciones para pasar a las opciones de configuración --psmy --oem. Podemos pasar estas opciones pytesseractusando el configparámetro en nuestro image\_to\_stringmétodo. Aquí hay un ejemplo del uso intencional del psm incorrecto (lo configuré para que esperara texto alineado verticalmente):



>>> pytesseract.image\_to\_string('./data/python\_dataset\_01.jpg', config="--psm 5")

"=\\n5\\nLEE:\\nce\\nae\\not\\nnH\\nHite\\noo. =\\nnda ...a5\\nicees 3 3\\nor \_ 8s\\nbaka gs\\nGas g\\n528 Ze\\n© © 5\\nEe 52\\n> 28\\nzo\\n2"

El texto es ilegible debido a que Tesseractel documento se lee verticalmente.



Descripción general del archivo Utils

Tendremos los siguientes métodos en nuestro utils.pyarchivo:



extract: encuentra todas las imágenes en la datacarpeta y devuelve una matriz que contiene cada línea de todas las imágenes



build\_chapters:construye un hash donde las claves son los títulos de los capítulos y el valor de cada clave es una cadena igual al contenido del capítulo



get\_chapter\_file: convierte una cadena de capítulo en el nombre de archivo html apropiado ( Chapter 1: Hello Worldsería igual a hello-world.html)



build\_html\_file: convierte un par clave-valor del build\_chaptersmétodo en una página html



convert\_chapter\_to\_spinal: convierte el nombre de un capítulo en mayúsculas y minúsculas ("Hola mundo" se convierte en "hola-mundo")



Creando el método de extracción:

El objetivo del método de extracción es devolver una matriz de líneas de todas las imágenes de la datacarpeta. Por lo tanto, el primer paso es determinar qué archivos necesitaremos revisar tesseract. Podemos hacerlo mediante el paquete integrado glob. Podemos pasar un patrón a la globbiblioteca y esta devolverá una lista de archivos que coincidan con él, de forma similar al lscomando.



El término "globbing" se refiere al proceso que Unix realiza para expandir nombres de archivo. No es una expresión regular, aunque puede ser similar. globUtiliza el patrón de expansión de nombres de ruta de Unix, que no usaremos para nada complejo. De hecho, solo necesitamos usar un comodín simple ( \*). Si queremos obtener una lista de las imágenes jpg en la datacarpeta, simplemente necesitamos usar este patrón: data/\*.jpg. Esto captura cualquier ruta de archivo dentro de la datacarpeta y termina en .jpg. \*Puede ser cualquier cadena.



Podemos probar esto usando el globmétodo de la globbiblioteca. En la consola de Python, importe la globbiblioteca y ejecute el patrón anterior usando el globmétodo:



>>> import glob

>>> glob.glob('data/\*.jpg')

\['data/python\_dataset\_16.jpg', ... 'data/python\_dataset\_33.jpg']

>>>

Nota: asegúrese de ejecutar esto en el directorio raíz del proyecto, no dentro de la carpeta de datos



Podemos recorrer esta matriz de rutas de archivo, ejecutarla tesseracty añadirla a una cadena gigante que luego podemos dividir en una matriz, línea por línea. Aquí está el extractmétodo completo:



import pytesseract

import glob





def extract(path='./data/\*.jpg'):

&nbsp;   pages = glob.glob(path)

&nbsp;   pages.sort()



&nbsp;   text = ''



&nbsp;   for page in pages:

&nbsp;       print('extracting: {}'.format(page))

&nbsp;       image\_string = pytesseract.image\_to\_string(page)

&nbsp;       text += image\_string



&nbsp;   lines = text.split('\\n')

&nbsp;   return lines

import ...: importa las bibliotecas pytesseract y glob



def extract: crea el método de extracción



(path='./data/\*.jpg')El extractmétodo acepta un pathparámetro que, por defecto, corresponde a la ruta que probamos anteriormente. Esto nos permitirá usar un conjunto de datos más pequeño y consistente en nuestras pruebas.



pages = glob.glob(path): Esto recupera una matriz de rutas de archivo para las páginas/archivos de nuestro conjunto de datos. Luego, la asigna a la pagesvariable



pages.sort(): glob no garantiza que los archivos se devuelvan en el orden correcto. Queremos ordenar esta matriz alfanuméricamente para que una página anterior no aparezca después de otra. Tenga en cuenta que sort()muta la matriz, no devuelve una nueva matriz.



>>> a = \[1, 2, 4, 3]

>>> a

\[1, 2, 4, 3]

>>> a.sort()

>>> a

\[1, 2, 3, 4]

text = ''Instanciamos la textcadena en blanco. Añadiremos las cadenas tesseractextraídas de todas nuestras imágenes a la textvariable.



for page in pages:Esto recorre la pagesvariable anterior. La pagevariable se refiere a la ruta de archivo actual en la que se encuentra el bucle.



print(...):Esto imprime el estado actual en la consola, dado que tenemos un conjunto de datos grande, es bueno saber en qué página se encuentra.



'extracting: {}'.format(page): formatreemplazará {}con la variable que pasemos en ( page).



image\_string = pytesseract.image\_to\_string(page): este OCR realiza la página actual y asigna la cadena a la image\_stringvariable



text += image\_string: esto se añade image\_stringa text. Esto significa que textserá una cadena extremadamente larga que contendrá todo el texto de nuestras imágenes, como un documento grande.



lines = text.split('\\n')El splitmétodo forma parte de la clase string, donde se puede crear una matriz de cadenas en puntos de interrupción dentro de una cadena. Por ejemplo, \\nsignifica una nueva línea que tesseractretorna para cada línea. Queremos iterar sobre estas cadenas por separado, por lo que debemos crear un punto de interrupción para \\n.



Aquí hay un ejemplo del splitcomando:



>>> lines = 'line1

line2

line3'

>>> lines.split('

')

\['line1', 'line2', 'line3']

return lines: Esto devuelve la matriz de líneas de todos los documentos. La usaremos para generar el hash de nuestros capítulos.



Nota: Hay dos líneas en blanco encima del método a seguir pep8.



Probando nuestro método de extracción:

Dado que el extractmétodo recorre más de 40 imágenes, deberíamos reducir esa cantidad temporalmente para realizar pruebas. Podemos segmentar un array a solo los primeros 3 elementos usando \[:3]. Los dos puntos ( :) indican a Python que extraiga todo antes del índice 3.



Podemos actualizar la pagesvariable para que solo recorra unas pocas imágenes:



\# ...

pages.sort()

pages = pages\[:3]

\# ...

Ahora que nuestra solución temporal está en su lugar, podemos probar la biblioteca en la consola de Python:



>>> from utils.utils import extract

>>> extract()

extracting: data/python\_dataset\_01.jpg

extracting: data/python\_dataset\_02.jpg

extracting: data/python\_dataset\_03.jpg

\['Chapter 1: Lorem', '', ... 'fermentum porta risus.']

>>>

from utils.utils import extractEsto le indica a Python que queremos importel extractmétodo desde utils/utils.py. El primero utilsse refiere al nombre del paquete (debido al \_\_init\_\_.pyarchivo) y el segundo utilsal utils.pyarchivo.



Si se devolvió una matriz muy grande, ¡su extractmétodo funciona según lo previsto!



Creando el método build\_chapters

Nuestro objetivo con este método es convertir la matriz del extract()método en un hash de capítulos.



Por ejemplo, las líneas se convertirían en capítulos aquí:



lines = \['Chapter 1: Lorem', 'line 1', 'line 2', 'Chapter 2: Ipsum', 'line 3']

build\_chapters(lines) # {'Chapter 1: Lorem': 'line 1\\nline2', 'Chapter 2: Ipsum', 'line 3'}

Para lograr esto, necesitamos reconocer qué línea es un capítulo y cuál es una línea normal. Podemos saber si una cadena es un capítulo si empieza por Chapter NUMBER:. Afortunadamente, se pueden usar expresiones regulares para ver si una cadena coincide con un patrón de "capítulo". Lo haremos mediante la rebiblioteca integrada:



>>> import re

>>> re.match(r"^(Chapter \[0-9]+:)", 'Chapter 1: Lorem')

<re.Match object; span=(0, 10), match='Chapter 1:'>

>>> re.match(r"^(Chapter \[0-9]+:)", 'Ipsum')

>>>

import re: importa la biblioteca de expresiones regulares incorporada de Python



re.matchEl método match devolverá un objeto si la cadena coincide con el patrón proporcionado



r"^(Chapter \[0-9]+:)":Este es el patrón de expresión regular que verifica Chapter NUMBER:, pronto explicaremos lo que esto significa



'Chapter 1: Lorem':esta es la cadena que queremos comprobar



<re.Match object..>:El objeto que se devuelve cuando se encuentra una coincidencia



re.match(..., 'Ipsum'):No se devuelve nada de esto porque no es un capítulo.





A continuación se muestra un desglose del r"^(Chapter \[0-9]+:)"patrón:



r: significa que es una expresión regular



^: indica que la cadena comienza con el patrón, por lo que Lorem chapter 1: ipsumno coincidirá. Para este proyecto, asumiremos que tesseractel reconocimiento óptico de caracteres (OCR) de los capítulos será correcto.



(...): indica el patrón que se debe aplicar a^



Chapter: indica el patrón a buscar Chapteren la cadena



\[0-9]: le dice al patrón que busque un número entre 0en 9esta posición



+: indica al patrón que busque uno o más de los patrones anteriores. En este caso, busca uno o más0-9



::le indica el patrón a buscar:





Aquí está el flujo de trabajo general del build\_chaptersmétodo:



Crea un hash de capítulos en blanco y una cadena para la clave del capítulo actual

recorrer cada línea

Si es un capítulo, actualiza la clave del capítulo actual

Si no es un capítulo, añádelo al valor de la clave del capítulo actual.

devolver capítulos hash



Aquí está el build\_chaptersmétodo:



import re

\# ...

def build\_chapters(lines):

&nbsp;   chapters = {}

&nbsp;   cur\_chapter = 'Intro'

&nbsp;   for line in lines:

&nbsp;       is\_chapter = re.match(r"^(Chapter \[0-9]+:)", line)



&nbsp;       if is\_chapter:

&nbsp;           cur\_chapter = line

&nbsp;       elif cur\_chapter in chapters.keys():

&nbsp;           content = '{}\\n'.format(line)

&nbsp;           chapters\[cur\_chapter] += content

&nbsp;       else:

&nbsp;           content = '{}\\n'.format(line)

&nbsp;           chapters\[cur\_chapter] = content



&nbsp;   return chapters

import reImporta la biblioteca de expresiones regulares. Debe estar al principio del archivo junto con las demás importaciones.



def build\_chapters(lines): define el build\_chaptersmétodo y tiene linescomo parámetro



chapters = {}: instancia un hash de capítulos en blanco



cur\_chapter = 'Intro': asigna introa cur\_chapter. Esto es solo una alternativa si el documento no comienza con una línea de capítulo. Por lo tanto, cualquier línea que no sea de capítulo y que aparezca antes de la primera línea de capítulo se asignará bajo la introclave.



for line in lines:: recorre las líneas



is\_chapter = re.match(...): verifica si la línea actual es un capítulo usando el patrón de expresión regular que usamos antes



if is\_chapter: manejaremos las líneas de capítulo de manera diferente a las líneas que no son de capítulo, por lo que usaremos una declaración if



cur\_chapter = line:esta línea le dice a nuestro método que ha terminado con el último capítulo y que el contenido que sigue será para el próximo capítulo. (ej. Chapter 1: Lorem-> Chapter 2: Ipsum)



elif cur\_chapter in chapters.keys():Esto comprueba si cur\_chapterhay una clave en nuestro hash. Si ya se ha instanciado un par clave-valor, podemos añadir una línea al valor actual. No podemos usarlo cur\_chapter in chaptersporque no se verificará con un array de claves. Por lo tanto, usamos el chapters.keys()método que devuelve un array de claves.



content = '{}\\n'.format(line): construye nuestra cadena de contenido para agregar una nueva línea ( \\n). chapters\[cur\_chapter] += content: Como sabemos que cur\_chapterexiste en chapters, podemos agregarlo a su valor actual usando el +=operador.



else::si el contenido no está en la cadena, entonces instanciaremos el par clave/valor



content = '{}\\n'.format(line): Igual que lo anterior. Es importante no repetir código (DRY); sin embargo, en este caso solo se repitió dos veces, así que no es tan grave. De lo contrario, deberíamos extraerlo a un método o refactorizarlo. Como es solo una línea, no tendremos que preocuparnos.



chapters\[cur\_chapter] = contentDado que el par clave-valor no existe, debemos crearlo mediante el =operador. Esta línea solo aparecerá una vez por capítulo.



return chapters:devuelve el hash de los capítulos que creamos



Probando build\_chapters

En la consola de Python, pasemos el resultado de nuestro extract()método a nuestro build\_chaptersmétodo:



>>> from utils.utils import extract, build\_chapters

>>> lines = extract()

extracting: data/python\_dataset\_01.jpg

extracting: data/python\_dataset\_02.jpg

extracting: data/python\_dataset\_03.jpg

>>> chapters = build\_chapters(lines)

>>> chapters

{'Chapter 1: Lorem': '\\nLorem ...\\n', 'Chapter 2: lpsum': '\\nFusce ...'}

>>> chapters.keys()

dict\_keys(\['Chapter 1: Lorem', 'Chapter 2: lpsum', 'Chapter 3: Dolor'])

Nota: asegúrese de guardar el archivo de utilidades y reiniciar la consola de Python



Si puedes ver un diccionario de claves para cada capítulo, ¡entonces tu función funciona correctamente!



Creando el método convert\_chapter\_to\_spinal y la excepción InvalidChapterException

Antes de convertir el hash de los capítulos a HTML, debemos crear algunos métodos auxiliares. Primero, debemos compilar el convert\_chapter\_to\_spinalmétodo. Además, crearemos una excepción personalizada llamada InvalidChapterException.



Nuestro convert\_chapter\_to\_spinalmétodo convierte una clave de capítulo, como Chapter 1: Lorem Ipsum Doloren un caso espinal, sin la parte del capítulo:lorem-ipsum-dolor



Aquí está nuestro convert\_chapter\_to\_spinalmétodo:



def convert\_chapter\_to\_spinal(chapter):

&nbsp;   name = re.sub(r"^(Chapter \[0-9]+: )", '', chapter)

&nbsp;   if name == chapter:

&nbsp;       raise InvalidChapterException

&nbsp;   name = name.lower().replace(' ', '-')

&nbsp;   return name

def convert\_chapter\_to\_spinal(chapter):: define nuestro método y toma una cadena llamada chaptercomo parámetro



re.sub(.., '', chapter)La biblioteca de expresiones regulares ofrece un submétodo para reemplazar coincidencias mediante expresiones regulares. Este método utiliza el patrón que creamos anteriormente para encontrar la coincidencia, eliminarla de \[nombre de la variable] chaptery luego asignarla a \[ namenombre de la variable]. No es obligatorio, pero quería que las URL HTML fueran cortas y fáciles de leer. El primer parámetro es el patrón, el segundo parámetro es con qué lo reemplazamos y el último es con qué lo verificamos.



if name == chapter:En este punto, el capítulo debería ser Chapter 1: Lorem, y la namevariable debería ser lorem. Si el re.submétodo no funcionó, namedebería ser igual a capítulo, ya que no se reemplazó nada. Si la cadena no es un capítulo válido, debería generar un error.



raise InvalidChapterExceptionEsto genera una excepción personalizada. Explicaremos cómo funciona en breve. Cuando se genera una excepción, se aplica al método que la llama. El método generará una excepción si no la detecta (envolviéndola en un \[nombre faltante try except]).



name = name.lower().replace(' ', '-')Esto limpia nuestra namecadena. La convierte Lorem Ipsuma lorem-ipsum. El lower()método convierte nuestra cadena a minúsculas y .replacereemplaza todos los espacios ( ' ') con un guion ( -).



return name:luego devolvemos el nombre que creamos.



Aquí está la excepción personalizada que creamos debajo del método:



class InvalidChapterException(Exception):

&nbsp;   """Chapter name is invalid"""

&nbsp;   pass

class InvalidChapterException(Exception):crea una clase llamada InvalidChapterExceptionque hereda la Exceptionclase.



"""Chapter name is invalid""":Este es el mensaje que se devolverá si se genera la excepción.



pass:no necesitamos nada en esta excepción ya que heredamos la Exceptionclase



Ahora, cada vez que generemos InvalidChapterException, se hará referencia a esta excepción.



Prueba de Convert\_chapter\_to\_spinal y InvalidChapterException

Reinicie la consola de Python e intente pasar cadenas al nuevo convert\_chapter\_to\_spinalmétodo:



>>> from utils.utils import convert\_chapter\_to\_spinal

>>> convert\_chapter\_to\_spinal('Chapter 1: Lorem')

'lorem'

>>> convert\_chapter\_to\_spinal('Chapter 2: Lorem Ipsum')

'lorem-ipsum'

>>> convert\_chapter\_to\_spinal('Dolor Sit')

Traceback (most recent call last):

&nbsp; File "<stdin>", line 1, in <module>

&nbsp; File ".../utils/utils.py", line 42, in convert\_chapter\_to\_spinal

&nbsp;   raise InvalidChapterException

utils.utils.InvalidChapterException

>>>

Podemos ver que el método convierte nuestros capítulos apropiadamente y genera nuestro error personalizado cuando se pasa un capítulo no válido.



Creando el método get\_chapter\_file

Nuestro último método auxiliar convierte nuestra cadena de capítulo en un nombre de archivo:



def get\_chapter\_file(chapter):

&nbsp;   chapter\_spinal\_case = convert\_chapter\_to\_spinal(chapter)

&nbsp;   return '{}.html'.format(chapter\_spinal\_case)

def get\_chapter\_file(chapter):: Define el get\_chapter\_filemétodo y requiere una chaptercadena como parámetro



convert\_chapter\_to\_spinal(chapter): utiliza el método auxiliar que creamos en la última sección y lo asigna achapter\_spinal\_case



return '{}.html'.format(chapter\_spinal\_case): devuelve la cadena de capítulo convertida como un nombre de archivo html. Chapter 1: Loremse convierte en lorem.html.



Podemos probar este método pasando las mismas cadenas de la última prueba del método auxiliar:



>>> from utils.utils import get\_chapter\_file

>>> get\_chapter\_file('Chapter 1: Lorem')

'lorem.html'

>>> get\_chapter\_file('Chapter 2: Lorem Ipsum')

'lorem-ipsum.html'

>>> get\_chapter\_file('Dolor Sit')

Traceback (most recent call last):

&nbsp; File "<stdin>", line 1, in <module>

&nbsp; File ".../utils/utils.py", line 53, in get\_chapter\_file

&nbsp;   chapter\_spinal\_case = convert\_chapter\_to\_spinal(chapter)

&nbsp; File ".../utils/utils.py", line 43, in convert\_chapter\_to\_spinal

&nbsp;   raise InvalidChapterException

utils.utils.InvalidChapterException

>>>

Podemos ver que se devuelven los nombres de archivo HTML correctos. Podemos ver dónde se genera inicialmente nuestro error y cómo avanza por la cadena hasta el get\_chapter\_filemétodo.



Creando el método build\_html\_files

Nos queda un último método: crear los archivos HTML. Veamos cómo crear uno manualmente en la consola de Python:



>>> from utils.utils import get\_chapter\_file

>>> chapters = {'Chapter 1: Lorem': 'content



line2



line3'}

>>> chapter\_key = list(chapters)\[0]

>>> chapter\_file = get\_chapter\_file(chapter\_key)

>>> content = chapters\[chapter\_key]

>>> file\_name = '{0}{1}'.format('html/', chapter\_file)

>>> html\_file = open(file\_name, 'w')

>>> html\_file.write(content)

>>> html\_file.close()

from utils.utils import get\_chapter\_file: importa el get\_chapter\_method, solo crearemos datos simulados en lugar de usar los otros métodos auxiliares por ahora



{'Chapter 1: Lorem': 'content'}: crea un diccionario de capítulos de ejemplo



list(chapters)\[0]Convertimos los capítulos en una lista que solo devolverá un array de claves. chapters.keys()Por simplicidad, no usamos este método. En Python 3, .keys()devuelve dict\_keysque son iterables, pero no indexables. Esto se debe a que Python 3.6 y versiones anteriores no ordenan las claves dentro de nuestros diccionarios/hashes. Usan menos memoria; sin embargo, usaremos la ruta menos eficiente y la convertiremos en una lista. En este proyecto, no necesitaremos analizar mucho la eficiencia; sin embargo, es un concepto importante a tener en cuenta. Luego, tomamos la lista de claves y recuperamos el primer elemento usando\[0]



get\_chapter\_file(chapter\_key):Esto utiliza nuestro método auxiliar de antes para recuperar el nombre de nuestro archivo html, que será lorem.html.



chapters\[chapter\_key]: recupera el valor de nuestra clave y lo asigna acontent



'{0}{1}'.format('html/', chapter\_file): crea nuestra ruta de archivo html que seráhtml/lorem.html



html\_file = open(file\_name, 'w'):Esto abre nuestro archivo html que nos permitirá acceder a él. wSignifica que simplemente escribiremos en él.



html\_file.write(content)Esto añade "our" contenta nuestro archivo HTML. Al abrirlo, veremos esto. En nuestro método, tendremos una plantilla HTML.



html\_file.close():esto cierra nuestro archivo html para escribir, queremos hacer esto en cada iteración/archivo



Ahora podemos ver que nuestro archivo html se crea en html/lorem.html:



A basic html page for the lorem chapter that says "content".

Este fue un enfoque muy simplificado de nuestro método; sin embargo, es un buen paso para comprender su concepto general. Básicamente, recuperamos un hash de capítulos y recorremos cada clave. Recuerde que cada clave representa un capítulo, donde su valor es el contenido de ese capítulo.



En cada iteración, tenemos un capítulo para el que necesitamos crear un archivo HTML. Obtenemos el nombre del archivo, el nombre del capítulo y su contenido mediante métodos auxiliares. Abrimos nuestro archivo HTML y le pasamos el código HTML. Una vez completado, cerramos el archivo y pasamos al siguiente capítulo hasta terminar. Veamos nuestro método build\_html\_files:



def build\_html\_files(chapters, dest='html/'):

&nbsp;   for chapter in chapters.keys():

&nbsp;       chapter\_file = get\_chapter\_file(chapter)

&nbsp;       file\_name = '{0}{1}'.format(dest, chapter\_file)

&nbsp;       html\_file = open(file\_name, 'w')

&nbsp;       paragraph = chapters\[chapter].replace('\\n\\n', '<br/><br/>')

&nbsp;       content = """

<html>

&nbsp;   <head>

&nbsp;       <link rel="stylesheet" href="styles.css">

&nbsp;   </head>

&nbsp;   <body>

&nbsp;       <div>

&nbsp;           <h1>{0}</h1>

&nbsp;           <p>{1}</p>

&nbsp;       </div>

&nbsp;   </body>

</html>

""".format(chapter, paragraph)

&nbsp;       html\_file.write(content)

&nbsp;       html\_file.close()

def build\_html\_files(chapters, dest='html/'):crea nuestro build\_html\_filesmétodo con chapterscomo parámetro y a destcomo parámetro (Destino de la carpeta html, por defecto html/)



for chapter in chapters.keys():Recuerda que .keys()los retornos dict\_keysson iterables. Así, podemos recorrer cada clave de capítulo en nuestra chaptersvariable.



chapter\_file = get\_chapter\_file(chapter): utiliza nuestro método auxiliar de antes para obtener el nombre del archivo del capítulo (ej. lorem.html)



file\_name = '{0}{1}'.format(dest, chapter\_file): construye la ruta completa del archivo (ej. html/lorem.html)



html\_file = open(file\_name, 'w'): abre el archivo html en modo escritura



chapters\[chapter].replace('\\n\\n', '<br/><br/>'): Esto toma el valor de nuestra clave de capítulos y reemplaza los saltos de línea con <br/><br/>. En HTML, este <br/>elemento se refiere a un salto de línea, donde dos saltos de línea resultan en una línea en blanco como espaciado. Esto nos permite ver correctamente los saltos de línea ( \\n\\n) en nuestro archivo HTML. Esto se asigna a paragraph.



content = """

&nbsp; <html>

&nbsp;     <head>

&nbsp;         <link rel="stylesheet" href="styles.css">

&nbsp;     </head>

&nbsp;     <body>

&nbsp;         <div>

&nbsp;             <h1>{0}</h1>

&nbsp;             <p>{1}</p>

&nbsp;         </div>

&nbsp;     </body>

&nbsp; </html>

""".format(chapter, paragraph)

Este es nuestro archivo HTML completo como una cadena. Es muy básico, y es todo lo que necesitamos. Usamos comillas triples ( """) para indicar que es un archivo HTML de varias líneas. La linkmetaetiqueta importa un styles.cssarchivo, que veremos pronto. \[ Nombre <h1>{0}</h1>del archivo] es donde se ubicará el título y <p>{1}</p>el contenido del capítulo. \[ Nombre del archivo] {0}y {1}hace referencia al primer y segundo parámetro del formatmétodo ( chapter, paragraph). Todo el contenido HTML se asigna entonces a \[Nombre del archivo] content.



html\_file.write(content):esto escribe nuestro contenido html en el archivo html actual.



html\_file.close():esto cierra el archivo html.



Probando archivos build\_html

Podemos probar la build\_html\_filesfunción ahora (crearemos styles.css más adelante).



Pero aún necesitamos vaciar nuestra carpeta html. Agrega el cleancomando a tu Makefile:



init:

&nbsp;	pip3 install -r requirements.txt

clean:

&nbsp;	rm html/\*.html

rm:este es el comando para eliminar archivos en el shell de Unix



html/\*.html:este es un patrón que se pasa a rmque le indica que elimine todos los archivos html en la carpeta html.



Ejecutar Make cleanpara limpiar nuestra carpeta html.



Inicie nuevamente la terminal de Python y pruebe nuestro nuevo método:



>>> from utils.utils import build\_html\_files

>>> chapters = {'Chapter 1: Lorem': 'content



line2



line3'}

>>> build\_html\_files(chapters)

>>>

Abra la carpeta html y vea el lorem.htmlarchivo:



Basic HTML page that says "Chapter 1: Lorem. Content, line2, line 3. This is the screen generated by the python program.

En este punto tu utils.pyarchivo debería verse así:



import pytesseract

import glob

import re





def extract(path='data/\*.jpg'):

&nbsp;   pages = glob.glob(path)

&nbsp;   pages.sort()

&nbsp;   pages = pages\[:3]



&nbsp;   text = ''



&nbsp;   for page in pages:

&nbsp;       print('extracting: {}'.format(page))

&nbsp;       image\_string = pytesseract.image\_to\_string(page)

&nbsp;       text += image\_string



&nbsp;   lines = text.split('

')

&nbsp;   return lines





def build\_chapters(lines):

&nbsp;   chapters = {}

&nbsp;   cur\_chapter = 'Intro'

&nbsp;   for line in lines:

&nbsp;       is\_chapter = re.match(r"^(Chapter \[0-9]+:)", line)



&nbsp;       if is\_chapter:

&nbsp;           cur\_chapter = line

&nbsp;       elif cur\_chapter in chapters.keys():

&nbsp;           content = '{}

'.format(line)

&nbsp;           chapters\[cur\_chapter] += content

&nbsp;       else:

&nbsp;           content = '{}

'.format(line)

&nbsp;           chapters\[cur\_chapter] = content



&nbsp;   return chapters





def convert\_chapter\_to\_spinal(chapter):

&nbsp;   name = re.sub(r"^(Chapter \[0-9]+: )", '', chapter)

&nbsp;   if name == chapter:

&nbsp;       raise InvalidChapterException

&nbsp;   name = name.lower().replace(' ', '-')

&nbsp;   return name





class InvalidChapterException(Exception):

&nbsp;   """Chapter name is invalid"""

&nbsp;   pass





def get\_chapter\_file(chapter):

&nbsp;   chapter\_spinal\_case = convert\_chapter\_to\_spinal(chapter)

&nbsp;   return '{}.html'.format(chapter\_spinal\_case)





def build\_html\_files(chapters, dest='html/'):

&nbsp;   for chapter in chapters.keys():

&nbsp;       chapter\_file = get\_chapter\_file(chapter)

&nbsp;       file\_name = '{0}{1}'.format(dest, chapter\_file)

&nbsp;       html\_file = open(file\_name, 'w')



&nbsp;       paragraph = chapters\[chapter].replace('



', '<br/><br/>')

&nbsp;       content = """

<html>

&nbsp;   <head>

&nbsp;       <link rel="stylesheet" href="styles.css">

&nbsp;   </head>

&nbsp;   <body>

&nbsp;       <div>

&nbsp;           <h1>{0}</h1>

&nbsp;           <p>{1}</p>

&nbsp;       </div>

&nbsp;   </body>

</html>

""".format(chapter, paragraph)

&nbsp;       html\_file.write(content)

&nbsp;       html\_file.close()

Creando el archivo main.py

Ahora podemos conectar todo en nuestro main.pyarchivo. Actualízalo main.pypara incluir lo siguiente:



from utils.utils import extract, build\_chapters, build\_html\_files



lines = extract()



chapters = build\_chapters(lines)



build\_html\_files(chapters)

En este punto, este archivo debería ser bastante claro. Importamos el método de extracción para extraer las líneas de nuestras imágenes. Luego, importamos el build\_chaptersmétodo para crear nuestro chaptershash usando lines. Después, lo pasamos a build\_html\_filespara crear nuestros archivos HTML.



Guarde este archivo y ejecútelo $ Make cleany luego $ python3 main.py(o $ python main.py):



$ python3 main.py

extracting: data/python\_dataset\_01.jpg

extracting: data/python\_dataset\_02.jpg

extracting: data/python\_dataset\_03.jpg

Ahora si verificamos si los archivos existen en nuestra carpeta html usando ls:



$ ls html

dolor.html lorem.html lpsum.html

¡Ya tenemos nuestros 3 capítulos creados! Abre uno para verlo:



The HTML page for the full Chapter 2 section. There is a lost of content and it is unstyled.

Esta página necesita un poco de estilo. Descarga los styles.cssarchivos de la htmlcarpeta en el repositorio de GitHub y guárdalos en nuestra htmlcarpeta. Una vez completado, actualiza la página:



This is a styled screen for chapter 2 that is inspired by material design.

Ahora es mucho más legible. Sin embargo, aún podemos añadir una función más: la navegación .



Añadiendo navegación

Podemos mejorar nuestro código actual para poder navegar entre páginas con un botón nexty previous. Aquí tienes un resumen básico de cómo lograrlo:



actualizamos nuestro bucle for para incluir el índice en el que estamos

Si estamos en la 2da iteración o posterior, agregamos un botón anterior

Si estamos antes de la última página, agregamos el botón siguiente



Comenzando con el primer paso, actualice su bucle desde:



for chapter in chapters.keys():

a:



chapter\_keys = list(chapters)

for index, chapter in enumerate(chapter\_keys):

list(chapters):esto convierte nuestro chapters.keys()en un conjunto listde claves que es indexable y lo asigna achapter\_keys



for index, chapter:se agrega indexcomo una variable que incrementa en cada bucle.



enumerate(chapter\_keys):Python nos proporciona una función incorporada llamada enumerateque realizará un seguimiento de las iteraciones para nosotros, lo que nos permitirá recuperar el indexvalor de cada bucle.



Ahora podemos trabajar en agregar nuestro enlace anterior:



\# ...

html\_file = open(file\_name, 'w')

prev\_link = ''

if index > 0:

&nbsp; prev\_chapter = chapter\_keys\[index - 1]

&nbsp; prev\_chapter\_file = get\_chapter\_file(prev\_chapter)

&nbsp; prev\_link = '<p><a href="{}">Previous</a></p>'.format(

&nbsp;   prev\_chapter\_file)

&nbsp;# ...

content = """

<html>

&nbsp;   ...

&nbsp;           <h1>{0}</h1>

&nbsp;           <p>{1}</p>

&nbsp;           {2}

&nbsp;   ...

</html>

""".format(chapter, paragraph, prev\_link)

prev\_link = '':Este es nuestro enlace anterior, que por defecto está en blanco.



if index > 0::si es la 2da página o posterior



prev\_chapter = chapter\_keys\[index - 1]:obtiene el capítulo anterior



get\_chapter\_file(prev\_chapter): obtiene el nombre del archivo del capítulo anterior



'<p><a href="{}">Previous</a></p>'Nuestro HTML para el enlace anterior, el enlace sería relativo a la carpeta donde se encuentra ( html), por lo que podemos pasar el nombre de archivo normal (ej. lorem.html). Agregamos el enlace del archivo mediante el formatmétodo.



content = """...{2}...""": Esto se refiere a la cadena de enlace anterior. Si está en blanco, se considerará como si nunca se hubiera añadido. Si la cadena contiene las etiquetas HTML, aparecerá en la página HTML como un enlace. Esto significa que no necesitaremos una condición para ocultar el enlace anterior si no existe. Si no existe, no aparecerá en el archivo HTML.



.format(chapter, paragraph, prev\_link): agrega el enlace anterior como parámetro



El nextbotón funciona básicamente igual, excepto que nuestra condición comprobaría if (index < len(chapters) - 1):si la página actual no es la última. También mostrará el siguiente capítulo chapter\_keys\[index + 1]en lugar del anterior.



Aquí está el método completo con los botones de navegación:



def build\_html\_files(chapters, dest='html/'):

&nbsp;   chapter\_keys = list(chapters)

&nbsp;   for index, chapter in enumerate(chapter\_keys):

&nbsp;       chapter\_file = get\_chapter\_file(chapter)

&nbsp;       file\_name = '{0}{1}'.format(dest, chapter\_file)

&nbsp;       html\_file = open(file\_name, 'w')



&nbsp;       prev\_link = ''

&nbsp;       next\_link = ''

&nbsp;       if index > 0:

&nbsp;           prev\_chapter = chapter\_keys\[index - 1]

&nbsp;           prev\_chapter\_file = get\_chapter\_file(prev\_chapter)

&nbsp;           prev\_link = '<p><a href="{}">Previous</a></p>'.format(

&nbsp;               prev\_chapter\_file)



&nbsp;       if (index < len(chapters) - 1):

&nbsp;           next\_chapter = chapter\_keys\[index + 1]

&nbsp;           next\_chapter\_file = get\_chapter\_file(next\_chapter)

&nbsp;           next\_link = '<p><a href="{}">Next</a></p>'.format(

&nbsp;               next\_chapter\_file)

&nbsp;       paragraph = chapters\[chapter].replace('\\n\\n', '<br/><br/>')

&nbsp;       content = """

<html>

&nbsp;   <head>

&nbsp;       <link rel="stylesheet" href="styles.css">

&nbsp;   </head>

&nbsp;   <body>

&nbsp;       <div>

&nbsp;           <h1>{0}</h1>

&nbsp;           <p>{1}</p>

&nbsp;           {2}{3}

&nbsp;       </div>

&nbsp;   </body>

</html>

""".format(chapter, paragraph, prev\_link, next\_link)

&nbsp;       html\_file.write(content)

&nbsp;       html\_file.close()

Una vez actualizado el código, ejecute $ Make cleany luego python3 main.py. Una vez ejecutado el script, revise sus archivos HTML para ver los botones siguiente y anterior:



A HTML screen with a next and previous button to navigate through pages and chapters.

Prueba de todo el conjunto de datos

Ahora que verificamos que funcionó para las primeras 3 imágenes, podemos probarlo con todo el conjunto de datos eliminando pages = pages\[:3]. Actualizar el extractmétodo desde:



def extract(path='data/\*.jpg'):

&nbsp;   pages = glob.glob(path)

&nbsp;   pages.sort()

&nbsp;   pages = pages\[:3]

&nbsp;   

&nbsp;   text = ''

&nbsp;   # ...

a:



def extract(path='data/\*.jpg'):

&nbsp;   pages = glob.glob(path)

&nbsp;   pages.sort()



&nbsp;   text = ''

&nbsp;   # ...

Ahora corre $ Make cleany python3 main.py:



$ python3 main.py

extracting: data/python\_dataset\_01.jpg

...

extracting: data/python\_dataset\_38.jpg

Si todo salió bien, ¡ahora deberías tener un sitio web estático en html/!



¿Que sigue?

En este punto, el proyecto está en una buena posición para desarrollarlo. Puedes agregar más funciones como una tabla de contenido, un contador de palabras y más. Recomiendo consultar el repositorio de Github para ver cómo probé el archivo utils.py usando pytesty coverage. Siempre estoy disponible para ayudarte con cualquier pregunta, así que no dudes en contactarme.





https://github.com/ArmaizAdenwala/image-scans-to-html.git

