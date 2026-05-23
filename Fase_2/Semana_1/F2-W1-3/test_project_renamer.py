from pathlib import Path

import pytest
from project_renamer import ProjectRenamer

# Simulamos la configuración que vendría del JSON
DUMMY_CONFIG = {"naming_convention": "{project}_{asset}_{variant}_v{version:03d}{ext}"}


# --- EDGE CASE 1: Archivo que ya cumple la convención ---
def test_ignore_already_conforming_file(tmp_path):
    """Prueba si archivo está bien nombrado, se ignore y no gaste un número de versión."""

    archivo_perfecto = tmp_path / "film_mi_cubo_lookdev_v001.fbx"
    archivo_perfecto.touch()  # Crea un archivo vacío

    renamer = ProjectRenamer(
        target_dir=tmp_path,
        project="film",
        variant="lookdev",
        config=DUMMY_CONFIG,
        dry_run=True,
    )
    renamer.run()

    # Validamos que lo detectó pero lo marcó como 'Ignorado'
    assert len(renamer.results) == 1
    assert "Ignorado" in renamer.results[0]["status"]
    # El contador de versión no debió haber subido
    assert renamer.version_counter == 1


# --- EDGE CASE 2: Nombres con basura, tildes, caracteres japoneses y emojis ---
def test_clean_string_with_garbage_characters(tmp_path):
    """Prueba la robustez del sanitizador de texto."""

    # Nombre horrible de artista apurado
    archivo_sucio = tmp_path / "Mállá_   fînal @#!! 最終 (1) 👽.ma"
    archivo_sucio.touch()

    renamer = ProjectRenamer(
        target_dir=tmp_path,
        project="PRJ",
        variant="base",
        config=DUMMY_CONFIG,
        dry_run=True,
    )
    renamer.run()

    # Validamos cómo limpió esa pesadilla
    resultado_nuevo = renamer.results[0]["new"]
    # La tilde se va, los espacios se vuelven _, los símbolos y emojis mueren.
    # Resultado esperado: prj_malla_final_1_base_v001.ma
    assert resultado_nuevo == "prj_malla_final_1_base_v001.ma"


# --- EDGE CASE 3: Archivo sin extensión ---
def test_file_without_extension(tmp_path):
    """Prueba que el renombrador no colapse si un archivo no tiene extensión."""

    archivo_raro = tmp_path / "archivo_huerfano"
    archivo_raro.touch()

    renamer = ProjectRenamer(
        target_dir=tmp_path,
        project="TEST",
        variant="geo",
        config=DUMMY_CONFIG,
        dry_run=True,
    )
    renamer.run()

    resultado_nuevo = renamer.results[0]["new"]
    # Debe mantener el formato, simplemente con extensión vacía
    assert resultado_nuevo == "test_archivo_huerfano_geo_v001"
