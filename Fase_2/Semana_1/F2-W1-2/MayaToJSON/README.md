# Explicación del código ma_to_json.py

>*Como en Arte, hay infinitas formas de llegar al mismo resultado. Esta es la mía.*

Vamos a desarmar el script creado usando una Analogía del Inspector en una Fábrica. 

Imaginemos que el código es un inspector parado frente a una cinta transportadora (el archivo .ma). Por la cinta pasan cajas (las líneas de texto). El inspector tiene una libreta maestra (meshes_encontrados) y un portapapeles temporal (mesh_actual).

## 🧰 1. Los Preparativos (Antes de prender la cinta)
```python
meshes_encontrados = []
    mesh_actual = None 
    regex_name = re.compile(r'-n "(.*?)"')
    regex_parent = re.compile(r'-p "(.*?)"')
```
- *meshes_encontrados = []*: Es la libreta maestra del inspector. Empieza vacía. Acá vamos a entregar el reporte final.

- *mesh_actual = None*: Es el portapapeles que el inspector lleva en la mano. Como todavía no empezó a mirar la cinta, no tiene nada (None). Este es nuestro famoso "Estado".

- *re.compile(...)*: En vez de armar el bisturí de búsqueda cada vez que pasa una caja, el inspector los afila antes de empezar el turno. compile hace que el script sea muchísimo más rápido cuando tiene que leer archivos gigantes.

## 📦 2. Encendiendo la Cinta Transportadora
```python
with open(filepath, 'r', encoding='utf-8') as f:
        for linea in f:
```
- *with open(...)*: Es como abrir la puerta de la fábrica. Usar with es una buena práctica crítica: asegura que si el script explota a la mitad, la puerta del archivo se cierre sola y no corrompa el .ma original.

- *for linea in f*:: Acá está la magia de rendimiento. No estamos abriendo el archivo de 1GB y metiéndolo entero en la memoria RAM. Estamos agarrando una sola caja a la vez, la miramos, y la dejamos pasar.

## 🧠 3. El Cerebro (Los 3 Escenarios del Inspector)
Por cada caja (línea) que pasa, el inspector solo puede tomar una de tres decisiones:

### Decisión A: "¡Encontré un Cubo!" (El Trigger)
```python
if linea.startswith('createNode mesh'):
                # ... (buscamos con regex y extraemos)
                mesh_actual = { "name": name, "parent": parent, "attrs": [] }
                meshes_encontrados.append(mesh_actual)
```
Si la caja dice "*createNode mesh*", el inspector agarra una hoja en blanco en su portapapeles (*mesh_actual*), anota el nombre y el padre, y dibuja una cajita vacía para los atributos ("*attrs*": []).

**🔥 El concepto vital:** El inspector inmediatamente guarda esa hoja en su libreta maestra (*append*). En Python, las listas guardan referencias (conexiones vivas). Si el inspector sigue escribiendo en su hoja del portapapeles más adelante, esa información se actualiza automáticamente adentro de la libreta maestra.

### Decisión B: "Estos son detalles del Cubo" (La Grabación)
```python
elif mesh_actual is not None and linea.startswith('\tsetAttr'):
                atributo_limpio = linea.strip()
                mesh_actual["attrs"].append(atributo_limpio)
```
Si la caja dice setAttr Y el inspector tiene una hoja en el portapapeles (mesh_actual is not None), significa que esta caja le pertenece al cubo que acaba de encontrar.
Limpia la mugre del texto (los tabuladores y saltos de línea usando .strip()) y anota ese atributo en la hoja que tiene en la mano.

### Decisión C: "Esto es otra cosa" (El Corte)
```python
elif linea.startswith('createNode') and not linea.startswith('createNode mesh'):
                mesh_actual = None
```
Si la caja dice que se está creando una cámara o una luz (createNode, pero no es mesh), el inspector tira la hoja que tenía en el portapapeles (mesh_actual = None). Corta la grabación. Esto evita que por accidente le anote propiedades de la cámara al cubo que estaba revisando antes.

## 🚪 4. La Ventanilla de Recepción (CLI y argparse)
Una herramienta profesional no requiere que entremos al código a cambiar el nombre del archivo cada vez que queremos escanear algo distinto. Para eso construimos una interfaz de línea de comandos (CLI).
```python
parser = argparse.ArgumentParser(...)
parser.add_argument("filepath", ...)
parser.add_argument("-o", "--output", ...)
args = parser.parse_args()
```
- *argparse*: Es la ventanilla de recepción de nuestra fábrica. Le permite al usuario (o a un servidor automático) indicarle al script exactamente qué archivo procesar (filepath) y, opcionalmente, dónde guardar el resultado usando el comando especial -o o --output.

## 🛡️ 5. Los Guardias de Seguridad (Manejo de Errores)
Antes de que la fábrica empiece a procesar cajas, necesitamos asegurarnos de que no nos mandaron algo peligroso o incorrecto.
```python
if not os.path.exists(args.filepath):
    # ...
if not args.filepath.lower().endswith(".ma"):
    # ...
try: 
    # (Ejecución del escaneo)
except Exception as e:
    # ...
```
- *os.path.exists*: Verifica físicamente que el archivo esté en el disco duro. Si el usuario escribió mal el nombre, el script avisa y se cierra ordenadamente con *sys.exit(1)*.

- *.endswith(".ma")*: Revisa la extensión. Si alguien intenta procesar un *.fbx* o un *.jpg*, los guardias lo rechazan inmediatamente.

- *try...except*: Es nuestra red de contención de incendios. Si ocurre cualquier error imprevisto mientras la cinta está corriendo (ej. falta de memoria), atrapa el error y nos avisa amablemente en lugar de crashear de forma violenta.

## ▶️ 6. El Botón de Encendido General
```python
if __name__ == "__main__":
    main()
```
- *if __name__ == "__main__"*: Esta es la barrera de seguridad estructural. Le dice a Python: "Ejecutá estas líneas SOLAMENTE si el usuario le dio play a este archivo directamente desde la consola". Si el día de mañana importamos nuestro parser desde dentro de otro script de Unreal Engine o Maya, esto previene que se ejecute solo por accidente.

### 💻 Ejemplos de uso práctico en la terminal
Con esta arquitectura, la herramienta ahora se opera directamente desde la consola, asumiendo que tu entorno virtual (.venv) está activo:

1. Escaneo rápido (Lectura en consola):
```bash
python ma_to_json.py assets/escena_personaje.ma
```
*Hace el escaneo y te muestra los datos directamente en la pantalla.*

2. Modo Exportación (Ideal para automatización):
```bash
python ma_to_json.py assets/escena_personaje.ma -o reportes/meshes_extraidos.json
```
*Hace el escaneo silenciosamente y genera el archivo .json estructurado y listo para ser auditado por otro programa.*

---

## ## 🤝 Notas Finales: Rompiendo la "Caja Negra"

La idea principal detrás de este nivel de detalle en el instructivo no es abrumarlos, sino todo lo contrario: 
>**destrabar la forma en la que ven el código.** 

Hoy en día es muy fácil y tentador abrir VS Code y pedirle a un LLM (o a un agente de IA integrado) que nos escriba una herramienta entera de cero. El problema de hacer eso sin tener los fundamentos es que el script se convierte en una "caja negra" mágica. Cuando esa magia falla a las 3 AM a un día de la entrega, nos quedamos a ciegas. 

Al entender que Python no procesa un archivo gigante "de golpe", sino que es simplemente un obrero mirando una línea de texto a la vez y tomando decisiones aisladas, le quitamos el misticismo a la programación y le perdemos el miedo.

**De Artista a Dev (y viceversa)**

Bajar a un entorno de desarrollo puro, pelear con la terminal, lidiar con entornos virtuales y leer errores rojos en la consola es abrumador. Es un proceso de aprendizaje tedioso y muchas veces frustrante. 

Pero quiero que tengan algo muy en cuenta: **el camino inverso es igual o peor.** Para alguien que viene del desarrollo de software duro, abrir Maya, entender la densidad topológica, hacer unas UVs limpias o tener buen ojo para el peso visual y la iluminación, es una pesadilla absoluta. Cada disciplina tiene su propia barrera de entrada, y es completamente normal sentir que están chocando contra una pared al principio.

Ahí es donde entra el valor de este equipo. Nuestro objetivo principal es ser ese puente que resuelve los problemas en la intersección exacta entre la visión creativa y la ingeniería. 

No estamos solos frente a la pantalla peleando contra la IA. Estamos acá para apoyarnos mutuamente: ustedes nos ayudan a entender por qué un asset se rompe visualmente, y nosotros los ayudamos a destrabar esa lógica que el LLM les generó mal. 

La única meta que importa acá es que: 
>**lleguemos juntos a los deadlines de producción**. 

Si se traban, levanten la mano, pregunten las veces que haga falta y sigamos empujando los límites del proyecto.

