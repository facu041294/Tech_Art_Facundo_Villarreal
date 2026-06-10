# 1. Inicializamos los contadores en cero
vertex_found = 0
faces_found = 0

# 2. Abrimos el archivo de forma segura
with open("modelo.obj", "r") as archivo:
    # 3. Recorremos línea por línea
    for linea in archivo:
        # 4. Evaluamos con qué carácter empieza cada línea
        if linea.startswith("v"):
            vertex_found += 1
        elif linea.startswith("f"):
            faces_found += 1

# 5. Imprimimos el reporte final fuera del bucle
print(
    f"Se encontraron {vertex_found} vertices y {faces_found} caras en este archivo .obj analizado."
)
