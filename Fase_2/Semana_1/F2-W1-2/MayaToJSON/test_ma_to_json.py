import pytest
from ma_to_json import parse_ma_file


# --- TEST 1: El Camino Feliz (Happy Path) ---
def test_parse_valid_mesh_with_parent(tmp_path):
    """Prueba para parser extraiga correctamente mesh estándar con padre y atributos."""

    # 1. Armamos nuestro archivo falso en la memoria temporal
    fake_ma = tmp_path / "test_mesh.ma"
    fake_ma.write_text(
        'createNode transform -n "SM_Cubo";\n'
        'createNode mesh -n "SM_CuboShape" -p "SM_Cubo";\n'
        '\tsetAttr -k off ".v";\n'
        '\tsetAttr ".vir" yes;\n'
        'createNode light -n "luz";\n',
        encoding="utf-8",
    )

    # 2. Ejecutamos tu motor
    resultado = parse_ma_file(str(fake_ma))

    # 3. Validamos (Assertions)
    assert len(resultado) == 1  # Debería encontrar exactamente 1 mesh
    assert resultado[0]["name"] == "SM_CuboShape"
    assert resultado[0]["parent"] == "SM_Cubo"
    assert len(resultado[0]["attrs"]) == 2  # Debería haber guardado 2 atributos
    assert 'setAttr -k off ".v";' in resultado[0]["attrs"]


# --- TEST 2: El Camino Alternativo (Edge Case) ---
def test_parse_mesh_without_parent(tmp_path):
    """Prueba que el parser no explote si el mesh está en la raíz y no tiene flag -p."""

    fake_ma = tmp_path / "test_root_mesh.ma"
    # Faltó el flag -p a propósito
    fake_ma.write_text(
        'createNode mesh -n "SM_RootShape";\n' '\tsetAttr ".v" yes;\n', encoding="utf-8"
    )

    resultado = parse_ma_file(str(fake_ma))

    assert len(resultado) == 1
    assert resultado[0]["name"] == "SM_RootShape"
    assert resultado[0]["parent"] == ""  # El padre debe ser un string vacío, no None


# --- TEST 3: Filtrado de Ruido (Defensa) ---
def test_ignore_non_mesh_nodes(tmp_path):
    """Prueba que el parser ignore por completo cámaras, luces y otros nodos."""

    fake_ma = tmp_path / "test_cameras.ma"
    fake_ma.write_text(
        'createNode camera -n "perspShape" -p "persp";\n'
        '\tsetAttr ".v" no;\n'
        'createNode light -n "luzDireccional";\n',
        encoding="utf-8",
    )

    resultado = parse_ma_file(str(fake_ma))

    # La lista debe estar vacía porque no hay ningún "createNode mesh"
    assert len(resultado) == 0
