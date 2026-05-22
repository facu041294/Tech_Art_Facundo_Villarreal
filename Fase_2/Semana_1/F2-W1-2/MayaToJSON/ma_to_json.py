import argparse
import json
import os
import re
import sys


def parse_ma_file(filepath):
    # Lista donde vamos a guardar todos los meshes encontrados
    meshes_encontrados = []
    # Nuestro "Estado": arranca en None porque todavía no leímos ningún mesh
    mesh_actual = None
    # Patrones pre-compilados (para que regex sea rápido si escaneamos miles de líneas)
    regex_name = re.compile(r'-n "(.*?)"')
    regex_parent = re.compile(r'-p "(.*?)"')

    # Abrimos el archivo en modo lectura
    with open(filepath, "r", encoding="utf-8") as f:
        for linea in f:

            # 1. ¿Encontramos un nodo de geometría?
            if linea.startswith("createNode mesh"):
                # Buscamos coincidencias en esta línea
                match_name = regex_name.search(linea)
                match_parent = regex_parent.search(linea)

                # Extraemos los datos (usamos None o "" si el flag -p no existe)
                name = match_name.group(1) if match_name else "Unknown"
                parent = match_parent.group(1) if match_parent else ""

                # Iniciamos nuestro "Estado" armando el diccionario
                mesh_actual = {"name": name, "parent": parent, "attrs": []}
                # Lo agregamos a nuestra lista maestra
                meshes_encontrados.append(mesh_actual)

            # 2. ¿Estamos leyendo atributos Y nuestro estado de mesh está activo?
            elif mesh_actual is not None and linea.startswith("\tsetAttr"):
                # Limpiamos los saltos de línea y tabulaciones de los extremos
                atributo_limpio = linea.strip()
                # Lo guardamos en el diccionario del mesh que está activo
                mesh_actual["attrs"].append(atributo_limpio)

            # 3. ¿Encontramos la creación de OTRO nodo que no es mesh?
            elif linea.startswith("createNode") and not linea.startswith(
                "createNode mesh"
            ):
                # Apagamos el estado. Ya no estamos leyendo un mesh.
                mesh_actual = None

    return meshes_encontrados


def main():
    # 1. Configuramos la Puerta de Entrada (CLI - Command Line Interface)
    parser = argparse.ArgumentParser(
        description="Parser de Maya ASCII (.ma) a JSON. "
        "Extrae geometrías y sus atributos."
    )

    # Definimos qué argumentos esperamos recibir en la consola
    parser.add_argument(
        "filepath", help="Ruta absoluta o relativa al archivo .ma que querés escanear."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Ruta opcional para guardar el JSON generado. "
        "Si no se usa, imprime en consola.",
        default=None,
    )

    # Leemos lo que el usuario (o el servidor CI) escribió
    args = parser.parse_args()

    # 2. Manejo de Errores (Defensa Perimetral)
    # Verificamos si el archivo realmente existe en el disco
    if not os.path.exists(args.filepath):
        print(f"ERROR CRÍTICO: No se encontró archivos en la ruta: '{args.filepath}'")
        sys.exit(1)  # Aborta el script y le devuelve un código de error al sistema

    # Verificamos que sea un archivo de texto de Maya (.ma)
    if not args.filepath.lower().endswith(".ma"):
        print(f"ERROR CRÍTICO: Archivo '{args.filepath}' no es archivo .ma válido.")
        sys.exit(1)

    # 3. Ejecución Segura (La Red de Contención)
    try:
        print(f"Iniciando escaneo de: {args.filepath}...")

        # Llamamos a tu motor
        resultado = parse_ma_file(args.filepath)

        # 4. Salida de Datos (Output)
        if args.output:
            # Si el usuario pasó el flag -o, creamos el archivo JSON
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=4)
            print(
                f"¡Éxito! Se encontraron {len(resultado)} meshes. "
                "Datos guardados en: {args.output}"
            )
        else:
            # Si no pasó la ruta de salida, se lo escupimos en la pantalla
            print(json.dumps(resultado, indent=4))
            print(f"\n¡Éxito! Se escanearon {len(resultado)} meshes de forma correcta.")

    except Exception as e:
        # Si CUALQUIER cosa explota dentro del parser (falta de memoria,
        # archivo corrupto), cae acá
        print(f"Error inesperado al procesar el archivo: {e}")
        sys.exit(1)


# Nuestro nuevo Botón de Play
if __name__ == "__main__":
    main()
