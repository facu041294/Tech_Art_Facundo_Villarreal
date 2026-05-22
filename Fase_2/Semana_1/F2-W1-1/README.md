# 🛠️ Pipeline Setup Guide: Python 3.11 + VS Code + Black + Ruff

Este instructivo está diseñado para estandarizar el entorno de desarrollo del equipo de Technical Art y Pipeline. Configurar correctamente este entorno previene errores de compatibilidad con herramientas de producción de terceros (DCCs como Maya, Unreal Engine, Houdini) y evita la pérdida de tiempo depurando fallos de infraestructura local.

---

## 🎯 Requisitos del Entorno de Estudio
* **Python:** Versión estricta **3.11.x** (Estándar global dictado por la *VFX Reference Platform* para garantizar compatibilidad interna en DCCs).
* **IDE:** VS Code.
* **Formateador:** Black (Estética de código unificada).
* **Linter:** Ruff (Calidad de código y detección temprana de bugs).

---

## 📂 Escenarios de Instalación de Python

Elegí el escenario que corresponda al estado actual de tu computadora de trabajo: (**El objetivo principal es mantener el sistema global limpio**)

### Escenario A: Computadora limpia (Sin versiones previas de Python)
1. Dirigite a la página oficial de descargas: [Python Windows Versions](https://www.python.org/downloads/windows/).
2. Descargá el instalador correspondiente: **`Windows installer (64-bit)`** (un archivo `.exe`). No descargues el paquete *embeddable* ni el código fuente.
3. **⚠️ PASO CRÍTICO:** Al ejecutar el instalador en modo administrador, en la primera pantalla, **ASEGURARSE DE DESMARCAR la casilla `Add python.exe to PATH`**.
<img width="654" height="401" alt="image" src="https://github.com/user-attachments/assets/c1caf391-9f9c-4fbf-8d69-e27a9429a461" />

4. Luego, elegí **"Customize installation"**.
5. En la pantalla de "Optional Features" presionas Next.
6. En la pantalla de "Advanced Options", verificá que la casilla **`Add Python to environment variables` también esté DESMARCADA**.
<img width="645" height="396" alt="image" src="https://github.com/user-attachments/assets/909bbe5b-0006-47f7-8d0e-73cae96b6bae" />

7. Completá la instalación.
   * *¿Por qué esto importa?* Si omitís este paso, Windows registrará el ejecutable del lenguaje a nivel global, llevando a posibles conflictos graves con las versiones internas de Python que traen otros programas (DCCs).

### Escenario B: Computadora con otra versión instalada (Ej. Python 3.13+)
**No desinstales la versión que ya tenés.** En Technical Art es mandatorio poder alternar entornos. El ecosistema oficial de Python en Windows maneja esto de forma nativa a través del **Python Launcher** (`py.exe`), el cual se encarga de rutear los comandos sin ensuciar el PATH global.

1. Descargá e instalá el ejecutable de **Python 3.11.x (64-bit)** siguiendo los **mismos pasos estrictos de aislamiento del Escenario A** (todo desmarcado).
2. Para llamar a una versión específica desde la consola del sistema para crear entornos, usarás el flag de versión en el launcher:
   * Para la 3.11: `py -3.11 --version`
   * Para tu otra versión: `py -3.13 --version`

---

## 📦 Aislamiento del Entorno (Creación del Virtual Environment)

**Regla de oro del estudio:** Nunca instalamos librerías, formateadores o linters en el entorno global de Windows. Cada repositorio posee su propia "burbuja" de dependencias.

0. Si no lo tienes a Visual Studio Code, descargalo de este [Link de descarga](https://code.visualstudio.com).
1. Abrí **VS Code** y abrí la carpeta raíz del repositorio del proyecto test para esta tarea (`File > Open Folder...`).
2. Abrí la terminal integrada de VS Code (`Ctrl + \``). Asegurate de que esté usando **PowerShell (PS)** o **CMD**.
3. Parado en la raíz de tu proyecto, ejecutá el comando para crear el entorno virtual aislado:
```powershell
   py -3.11 -m venv .venv
```
4. Activación del entorno:

- Ejecutá el script de activación:
```powershell
.\\.venv\\Scripts\\activate
```
- Sabrás que funcionó porque el prompt de tu consola ahora estará antecedido por el prefijo (.venv) en color verde.

🛑 ¿Error de permisos en PowerShell? > Si al intentar activar te aparece un texto rojo indicando que "la ejecución de scripts está deshabilitada en este sistema", ejecutá la siguiente directiva de seguridad para tu usuario y volvé a intentar la activación:
```powershell
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```

## 🏗️ Configuración del Proyecto y Dependencias
En el estudio utilizamos archivos estandarizados para que el onboarding de un nuevo artista sea automático.

1. Dependencias (requirements-dev.txt)
Asegurate de que en la raíz del repositorio exista el archivo requirements-dev.txt con el siguiente contenido:
```plaintext
black
ruff
```
Una vez que visualices el prefijo (.venv) activo en tu terminal, procedé a instalar todas las herramientas de un solo golpe ejecutando:
```powershell
pip install -r requirements-dev.txt
```
2. Reglas del Linter y Formateador (pyproject.toml)
Para que Black y Ruff no se peleen entre sí y respeten el estándar del estudio, el repositorio debe contener en su raíz el archivo pyproject.toml con esta configuración:
```toml
[tool.black]
line-length = 88
target-version = ['py311']
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | \.vscode
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W"]
ignore = []
```

## ⚙️ Configuración del Workspace en VS Code
Para evitar obligar a cada miembro del equipo a modificar sus preferencias globales, el repositorio utiliza ajustes locales.

1. En la raíz de tu proyecto, asegurate de tener una carpeta llamada .vscode.

2. Dentro de esa carpeta, creá o verificá el archivo settings.json.

3. El bloque de configuración debe ser exactamente este:
```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "python.linting.ruffEnabled": true
}
```
*Nota: Asegurate de tener instaladas las extensiones de VS Code: Python (Microsoft), Black Formatter (Microsoft) y Ruff (Astral Software).*

## ✅ Criterios de Aceptación (Verificación del Setup)
Para dar por aprobado tu onboarding del entorno, debés validar estos 3 puntos:

Intérprete del Editor: En la esquina inferior derecha de VS Code (o usando Ctrl+Shift+P > Python: Select Interpreter), asegurate de que esté seleccionado el intérprete que apunta a .\\.venv\\Scripts\\python.exe.

Auto-formateo (Black): Creá un archivo de prueba test_pipeline.py, escribí una línea con espaciados incorrectos deliberados (ej. def mi_funcion(   a ,  b   ):) y guardá el archivo (Ctrl + S). El código debe formatearse de forma simétrica e instantánea.

Control de Calidad (Ruff): En tu terminal activa (.venv), ejecutá el inspector de código:
```powershell
ruff check black_hello.py
```
La consola debe listar advertencias lógicas claras (como variables declaradas en desuso o imports innecesarios) si es que existen en el script.
