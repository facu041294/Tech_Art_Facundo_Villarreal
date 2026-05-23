import json
import shutil
from pathlib import Path

from project_renamer import BatchTool


class MassMover(BatchTool):
    """
    Mueve archivos masivamente a un directorio destino, filtrando por extensión.
    """

    def __init__(
        self,
        target_dir: Path,
        dest_dir: Path,
        extension_filter: str = None,
        dry_run: bool = True,
    ):
        super().__init__(target_dir, dry_run)
        self.dest_dir = dest_dir
        self.extension_filter = extension_filter.lower() if extension_filter else None

        # Si no es dry_run, nos aseguramos de que el destino exista
        if not self.dry_run and not self.dest_dir.exists():
            self.dest_dir.mkdir(parents=True, exist_ok=True)

    def process_item(self, filepath: Path):
        # Regla de negocio: Si hay un filtro y no coincide, lo ignoramos
        if self.extension_filter and filepath.suffix.lower() != self.extension_filter:
            self.results.append(
                {
                    "old": filepath.name,
                    "new": "N/A",
                    "status": "[yellow]Ignorado (Filtro)",
                }
            )
            return

        new_filepath = self.dest_dir / filepath.name

        if self.dry_run:
            self.results.append(
                {
                    "old": filepath.name,
                    "new": f"-> {self.dest_dir.name}/",
                    "status": "[blue]Pendiente (Dry Run)",
                }
            )
        else:
            shutil.move(str(filepath), str(new_filepath))
            self.results.append(
                {
                    "old": filepath.name,
                    "new": f"-> {self.dest_dir.name}/",
                    "status": "[green]Movido OK",
                }
            )


class MassConverter(BatchTool):
    """
    Simula la conversión masiva de formatos (Ej: de .obj a .fbx).
    """

    def __init__(self, target_dir: Path, target_format: str, dry_run: bool = True):
        super().__init__(target_dir, dry_run)
        # Nos aseguramos de que el formato empiece con un punto
        self.target_format = f".{target_format.strip('.')}".lower()

    def process_item(self, filepath: Path):
        old_name = filepath.name

        if filepath.suffix.lower() == self.target_format:
            self.results.append(
                {
                    "old": old_name,
                    "new": old_name,
                    "status": "[yellow]Ignorado (Ya convertido)",
                }
            )
            return

        new_filepath = filepath.with_suffix(self.target_format)

        if self.dry_run:
            self.results.append(
                {
                    "old": old_name,
                    "new": new_filepath.name,
                    "status": "[blue]Pendiente (Dry Run)",
                }
            )
        else:
            # Acá iría la llamada a subprocess o a la API del DCC para la conversión real
            # Para la prueba, simplemente lo renombramos a nivel OS
            filepath.rename(new_filepath)
            self.results.append(
                {
                    "old": old_name,
                    "new": new_filepath.name,
                    "status": "[green]Convertido OK",
                }
            )


class MassTagger(BatchTool):
    """
    Agrega metadata masivamente creando archivos sidecar (.meta.json) adyacentes al asset.
    """

    def __init__(
        self, target_dir: Path, author: str, category: str, dry_run: bool = True
    ):
        super().__init__(target_dir, dry_run)
        self.metadata = {
            "author": author,
            "category": category,
            "pipeline_version": "1.0",
            "approved": False,
        }

    def process_item(self, filepath: Path):
        # Ignoramos si la tool intenta procesar los archivos de metadatos que acabamos de crear
        if filepath.suffix.lower() == ".json":
            return

        sidecar_filepath = filepath.with_suffix(f"{filepath.suffix}.meta.json")

        if sidecar_filepath.exists():
            self.results.append(
                {
                    "old": filepath.name,
                    "new": sidecar_filepath.name,
                    "status": "[yellow]Ignorado (Meta ya existe)",
                }
            )
            return

        if self.dry_run:
            self.results.append(
                {
                    "old": filepath.name,
                    "new": f"+ {sidecar_filepath.name}",
                    "status": "[blue]Pendiente Tagger (Dry Run)",
                }
            )
        else:
            # Creamos el archivo adyacente con la metadata inyectada
            with open(sidecar_filepath, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=4)
            self.results.append(
                {
                    "old": filepath.name,
                    "new": f"+ {sidecar_filepath.name}",
                    "status": "[green]Taggeado OK",
                }
            )
