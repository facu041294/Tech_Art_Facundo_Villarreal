# 🚀 Fase 1 - Semana 3: Pipeline Setup, Automatización y Fundamentos 3D

**Especialización Technical Artist - Games & Virtual Production** **Autor:** Facundo Villarreal | **Cohorte:** 2026 | **Instructor:** Max Sarlija

Este repositorio contiene los entregables y la documentación correspondientes a la Semana 3 de la Fase 1 del programa. El objetivo central de esta semana fue establecer un entorno de trabajo CGI robusto, desarrollar herramientas procedimentales para optimizar tiempos de producción y validar el pipeline mediante la creación de assets 3D en Autodesk Maya.

---

## 🎯 Objetivos de la Semana
1. **Estandarizar el entorno de trabajo:** Instalación auditada y documentada de todo el software necesario para el pipeline.
2. **Desarrollar herramientas de automatización (Tooling):** Creación de un script en MEL para reducir el tiempo de setup de iluminación y renderizado de 20 minutos a un solo clic.
3. **Validación Artística:** Introducción a la topología y herramientas de modelado de Maya para probar el entorno generado.

---

## 🛠️ Ejercicio 1: Documentación y Setup del Pipeline CGI

El primer paso de un Technical Artist es asegurar que el ecosistema de software sea predecible y replicable. Se generó un **Manual de Documentación de Instalación** que registra cronológicamente las herramientas integradas al workstation.

* **Herramientas Core Registradas:** Maya 2024.2.4 (MtoA, LookdevX, Bifrost), Unreal Engine 5.4.4, Adobe Substance 3D Painter.
* **Control de Versiones y Gestión:** Perforce P4 One, GitHub Desktop, Git.
* **Asistentes y Entornos:** Cursor, Ollama, Python 3.13.7.
* **Enfoque Técnico:** Se establecieron convenciones estrictas para documentar dependencias, variables de entorno (PATH) y resolución de bugs, asegurando un control absoluto sobre las versiones (MAJOR.MINOR.PATCH) de todo el pipeline.

---

## ⚙️ Ejercicio 2: Scripting y Automatización (Arnold Lookdev Studio Pro)

Para optimizar el flujo de trabajo de los artistas 3D al presentar *dailies* o renders de portfolio, se desarrolló una herramienta procedimental en **MEL (Maya Embedded Language)**. Este script automatiza la creación de un estudio fotográfico completo basado en el volumen del asset.

**Características Clave del Tool:**
* **Adaptación Procedimental:** El sistema lee el *Bounding Box* del modelo y calcula matemáticamente las distancias, intensidad de luces y escala del fondo.
* **Z-Up Pipeline Ready:** El script está programado nativamente para entornos Z-Up (estándar de Unreal Engine), realizando extrusiones en *World Space* para evitar colapsos de normales.
* **Iluminación Física y Conexión de Nodos:** Instanciación de *Area Lights* escaladas físicamente y vinculadas directamente al motor de render mediante manipulación del *Node Graph* (`connectAttr` al `defaultLightSet`), evitando fallos de iluminación por defecto.
* **Tri-Cam Setup:** Generación de un array de tres cámaras (Main, Side, High) auto-apuntadas al centro de masa del modelo mediante `aimConstraints` vectoriales, preparadas para *Batch Rendering*.

*(Nota: El código fuente y los detalles técnicos profundos de esta herramienta se encuentran en el script `LookDevStudioPro.mel` adjunto en el repositorio).*

---

## 🎨 Ejercicio 3: Introducción al Modelado (Validación del Pipeline)

Como cierre de la semana, se realizó la transición de la lógica de programación a la aplicación artística. Este ejercicio consistió en el modelado de una figura básica como primera toma de contacto con el *toolkit* de modelado poligonal de Maya.

**Propósito dentro del Pipeline:**
1. **Familiarización con el DCC:** Entender el comportamiento de la topología, los *Edge Loops*, extrusiones manuales y el manejo del pivote dentro del espacio 3D de Maya.
2. **Prueba de Estrés (Stress Test):** Utilizar esta primera malla tridimensional para ejecutar el script del Ejercicio 2, validando que el ciclorama procedimental se adapte a una escala humana/de objeto real, y renderizando las primeras hojas de contacto (*Contact Sheets*) bajo la iluminación de Arnold.

---

## 💡 Reflexión Final
La Semana 3 marca el punto de inflexión donde el software deja de ser un "lienzo en blanco" y se convierte en una **fábrica estructurada**. Al dominar la documentación de nuestro entorno y aprender a programar nuestras propias herramientas de asistencia, garantizamos que el tiempo futuro se invierta en la calidad artística del asset y no en configuraciones repetitivas de software.