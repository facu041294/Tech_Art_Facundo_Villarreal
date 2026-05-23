# 🚀 Kit de Herramientas Batch para Pipeline (Onboarding)
---
### ¡Bienvenido al equipo! 
Este repositorio contiene una suite de herramientas diseñada para procesar archivos de forma masiva (renombrar, mover, convertir, etc.).

Si eres nuevo en el desarrollo de herramientas, no te preocupes. Aquí explicamos no solo cómo se usan, sino qué está ocurriendo "bajo el capó" para que aprendas a crear tus propias herramientas.

## Primeros pasos (Instalación)
Para que estas herramientas funcionen, necesitas tener configurado tu entorno.

1. Abre tu terminal dentro de la carpeta del proyecto.

2. Activa tu entorno virtual (deberías ver (.venv) a la izquierda de tu terminal en verdecito).

3. Instala las dependencias necesarias ejecutando:
```bash
pip install rich
```

## Manual de Uso: ¿Cómo renombrar assets?
Esta herramienta normaliza los nombres de tus archivos automáticamente para que sigan la regla: proyecto_asset_variant_v001.ext.

1. Primero, prueba de forma segura (Modo "Dry-Run")
Por seguridad, la herramienta siempre empieza en "Modo Simulación". No cambiará nada en tus archivos, solo te mostrará en pantalla qué es lo que planea hacer.
```bash
python project_renamer.py ./tu_carpeta_de_assets -p "FILM" -v "lookdev"
```
*Si la tabla que aparece en pantalla es correcta, ¡estás listo para aplicar los cambios!*

2. Aplicar los cambios reales
Cuando estés seguro de que el resultado es el que buscas, agrega --apply:
```bash
python project_renamer.py ./tu_carpeta_de_assets -p "FILM" -v "lookdev" --apply
```
*¡Listo! Tus archivos han sido normalizados y se generó un log con el historial.*

3. ¿Cómo funciona esto? (Entendiendo el código)
Para no tener que programar cada herramienta desde cero, creamos un "Framework Base" llamado BatchTool.

## La analogía del esqueleto
Imagina que BatchTool es una maquinaria de fábrica que ya viene construida:

- Sabe cómo abrir carpetas.

- Sabe cómo mostrar errores si algo falla.

- Sabe cómo hacer reportes bonitos.

Tú, como artista o desarrollador, solo necesitas darle la pieza que falta (la regla de negocio).

### Diagrama de la estructura
- BatchTool (La fábrica): Es la clase base. No la cambies, solo úsala.

- ProjectRenamer / MassMover / MassTagger (Las piezas): Son clases hijas que heredan todo el poder de la fábrica y solo definen qué hacer con cada archivo en el método process_item().

## ¿Quieres crear tu propia herramienta? (Paso a Paso)
Si te piden una herramienta nueva (ejemplo: mover archivos), no escribas código desde cero. Sigue estos 3 pasos:

- Crea un archivo nuevo (o usa derived_tools.py).

- Importa la base: 
```python
from project_renamer import BatchTool
```

- Crea tu clase hija:
```python
class MiNuevaTool(BatchTool):
    def process_item(self, filepath):
        # Aquí escribes tu lógica única: ¿Qué quieres hacer con el archivo?
        print(f"Estoy procesando: {filepath.name}")
```
*Al hacer esto, tu nueva herramienta tendrá automáticamente soporte para --apply, logs y reportes en tabla.*

## Auditoría de calidad
Para asegurarnos de que el código no se rompa mientras trabajamos, tenemos pruebas automatizadas. Si haces algún cambio, siempre ejecuta:
```bash
pytest test_project_renamer.py -v
```
Si ves todo en VERDE, puedes estar tranquilo/a de que tu código es seguro para el equipo.

¿Tienes dudas? No te quedes trabado más de 90 minutos. Pregunta en Discord #fase-2-ayuda. ¡Estamos aquí para aprender juntos!