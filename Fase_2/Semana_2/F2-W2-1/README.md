# Fase 2 - Semana 2: Setup Visual Studio + Entorno C++
🎯 **F2-W2-1 — Pipeline Technical Art Environment**

Este repositorio contiene la documentación y la estructura inicial correspondientes a la **Fase 2, Semana 2** del plan de especialización técnica. El objetivo principal de este hito fue configurar un entorno nativo de desarrollo C++ (MSVC) e implementar, compilar y ejecutar de forma exitosa un flujo básico de compilación orientado al desarrollo de herramientas de pipeline y plugins de bajo nivel para DCCs como Maya y Unreal Engine.

---

## 💡 Importancia del Entorno C++ en Technical Art

En entornos de producción de alta escala cinematográfica o de videojuegos, el core de las herramientas principales (**Unreal Engine, Autodesk Maya, SideFX Houdini**) está construido nativamente sobre **C++**. 
* **Optimización de Performance:** Cuando los scripts de automatización en Python alcanzan cuellos de botella en operaciones de cálculo pesado (por ejemplo, deformadores complejos, procesamiento denso de mallas o simulaciones), se recurre al desarrollo de hot paths optimizados en C++.
* **Extensiones del Ecosistema:** Permite la creación y el mantenimiento de plugins compilados (`.mll` en Windows), nodos customizados en el grafo de dependencia de Maya y la modificación o extensión del código fuente de Unreal Engine mediante módulos robustos.

---

## 📦 Herramientas y Stack Utilizado

* **Sistema Operativo:** Windows 11 Pro (x64)
* **Compilador e IDE:** Visual Studio Community 2022
  * *Carga de trabajo (Workload):* Desarrollo para el escritorio con C++ (*Desktop development with C++*).
* **Terminal Utilizada:** Developer Command Prompt para VS 2022.

---

## 🛠️ Implementación y Flujo de Compilación

### 1. El Código Fuente (`hello.cpp`)

Se utilizó una estructura estándar de C++. Adicionalmente, para solventar los problemas nativos de codificación de páginas de caracteres de la consola de Windows (`cmd.exe`), se integró la API nativa de Windows (`windows.h`) para forzar la salida de flujo en formato **UTF-8**, permitiendo la representación correcta de signos de apertura y acentos del español:

```cpp
#include <iostream>
#include <windows.h> // API nativa de Windows para manejo del entorno

int main() {
    // Configura la consola para interpretar correctamente la codificación UTF-8 (Code Page 65001)
    SetConsoleOutputCP(CP_UTF8); 
    
    std::cout << "¡Entorno C++ configurado correctamente para Technical Art!" << std::endl;
    return 0;
}
```
2. Comandos de Navegación y Compilación
Dado que el repositorio local se encuentra alojado en una unidad secundaria (G:), se utilizó el flag /d en la consola nativa de desarrollo para forzar el salto simultáneo de unidad de almacenamiento y ruta del directorio de trabajo:

```bash
# 1. Navegación inter-unidad hacia el espacio de trabajo de la tarea
cd /d "G:\Github repositories\Tech_Art_Facundo_Villarreal\Fase_2\Semana_2\F2-W2-1"

# 2. Compilación del código fuente mediante el compilador MSVC (cl.exe)
cl /EHsc hello.cpp

# 3. Ejecución del binario compilado generado
hello.exe
```
- Nota sobre flags: El parámetro /EHsc le indica al compilador que habilite el modelo estándar de manejo de excepciones síncronas de C++, garantizando que los objetos con destructores locales se destruyan de forma segura si se lanza una excepción, eliminando warnings colaterales durante el build.

## ✅ Criterios de Aceptación Cumplidos
[x] Compilación Exitosa: Generación nativa del archivo de objeto hello.obj y el ejecutable binario hello.exe sin errores de linkeo ni de compilación.

[x] Output Correcto en Consola: Visualización del string en consola respetando la codificación de caracteres.

[x] Comandos Documentados: Flujo de terminal registrado y estandarizado para su uso futuro en scripts automatizados de compilación local o entornos de Integración Continua (CI).

## 📝 Micro-Reflexión del Setup
Desafío Técnico Resuelto: El comportamiento por defecto del comando cd en Windows al intentar migrar de unidades (C: a G:) y la discrepancia de codificación entre el formato de archivo de texto UTF-8 vs la Code Page regional por defecto de la terminal de desarrollo fueron los dos puntos lógicos de fricción resueltos.

Primera Impresión C++ vs Python: A diferencia del dinamismo e interpretación en tiempo de ejecución directa de Python, C++ requiere de un paso explícito de traducción estricta (Compilación + Linkeo de binarios). Esto impone una rigidez de tipado y una estructura de sintaxis mucho más formal (como el uso obligatorio del ;), pero que a su vez se traduce en un control absoluto sobre el hardware, la memoria y el rendimiento de la pipeline.

Nivel de Confianza con el Entorno C++: 5/5 - El compilador responde perfectamente y las bases del pipeline de compilación local quedaron validadas.

