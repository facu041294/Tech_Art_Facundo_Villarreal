import argparse
import json
import logging
import re
import sys
import unicodedata
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

# Terceros (UI)
from rich.console import Console
from rich.table import Table

console = Console()


def setup_logger() -> logging.Logger:
    """Configura el logger para guardar logs en la carpeta /logs."""
    # 1. Definimos la carpeta de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)  # La crea si no existe, si existe no hace nada

    # 2. Generamos el nombre del archivo dentro de esa carpeta
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f"rename_log_{timestamp}.txt"

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )
    return logging.getLogger("BatchToolLogger")


logger = setup_logger()


# ==========================================
# ARQUITECTURA BASE (FRAMEWORK)
# ==========================================
class BatchTool(ABC):
    """
    Clase abstracta base para herramientas de procesamiento masivo.
    Maneja el state, el dry_run, los errores y el reporte de forma unificada.
    """

    def __init__(self, target_dir: Path, dry_run: bool = True):
        self.target_dir = target_dir
        self.dry_run = dry_run
        self.results = []  # Almacenará dicts: {"old": str, "new": str, "status": str}

    def run(self):
        """Punto de entrada principal. Itera y atrapa errores globales."""
        if not self.target_dir.exists() or not self.target_dir.is_dir():
            msg = f"Directorio inválido o inexistente: {self.target_dir}"
            logger.error(msg)
            console.print(f"[bold red]{msg}[/bold red]")
            sys.exit(1)

        logger.info(
            f"--- Iniciando BatchTool en:{self.target_dir} | Dry Run:{self.dry_run} ---"
        )

        # Iteramos solo archivos, ignorando carpetas y nuestros propios logs
        for filepath in self.target_dir.iterdir():
            if filepath.is_file() and not filepath.name.startswith("rename_log_"):
                try:
                    self.process_item(filepath)
                except PermissionError:
                    self.results.append(
                        {
                            "old": filepath.name,
                            "new": "N/A",
                            "status": "[red]Acceso Denegado",
                        }
                    )
                    logger.error(f"Permiso denegado: {filepath.name}")
                except Exception as e:
                    self.results.append(
                        {
                            "old": filepath.name,
                            "new": "N/A",
                            "status": f"[red]Error: {e}",
                        }
                    )
                    logger.exception(f"Error inesperado en {filepath.name}: {e}")

        self.report()

    @abstractmethod
    def process_item(self, filepath: Path):
        """Debe ser implementado por la clase hija para la lógica específica."""
        pass

    def report(self):
        """Genera una tabla visual usando Rich con los resultados de la operación."""
        table = Table(
            title=f"Resultados de Operación {'(DRY RUN)' if self.dry_run else '(APPLIED)'}"
        )
        table.add_column("Archivo Original", style="cyan")
        table.add_column("Nuevo Archivo", style="magenta")
        table.add_column("Estado", justify="center")

        for r in self.results:
            table.add_row(r["old"], r["new"], r["status"])

        console.print(table)
        logger.info("--- Operación Finalizada ---")


# ==========================================
# IMPLEMENTACIÓN ESPECÍFICA (RENAMER)
# ==========================================
class ProjectRenamer(BatchTool):
    """
    Renombrador que aplica la convención: proyecto_asset_variant_v###.ext
    """

    def __init__(
        self,
        target_dir: Path,
        project: str,
        variant: str,
        config: dict,
        dry_run: bool = True,
    ):
        super().__init__(target_dir, dry_run)
        self.config = config
        self.project = self._clean_string(project)
        self.variant = self._clean_string(variant)
        self.version_counter = 1

    def _clean_string(self, text: str) -> str:
        """Remueve tildes, ñ, caracteres especiales y cambia espacios por guiones bajos."""
        # Normalizar tildes y caracteres extraños
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        # Reemplazar todo lo que NO sea letra o número por espacios
        # (Evitamos \w para que no se nos filtren guiones bajos viejos)
        text = re.sub(r"[^a-zA-Z0-9]", " ", text)

        # Reemplazar espacios múltiples por un solo guion bajo
        text = re.sub(r"\s+", "_", text.strip())
        return text.lower()

    def process_item(self, filepath: Path):
        old_name = filepath.name
        extension = filepath.suffix.lower()

        # --- DEFENSA: Verificamos si el archivo YA cumple la convención ---
        # Busca: proyecto_cualquierCosa_variante_v[3 numeros].ext
        patron_validacion = f"^{self.project}_.*_{self.variant}_v[0-9]{{3}}{extension}$"
        if re.match(patron_validacion, old_name):
            self.results.append(
                {
                    "old": old_name,
                    "new": old_name,
                    "status": "[yellow]Ignorado (Ya cumple)",
                }
            )
            return

        asset_base = self._clean_string(filepath.stem)

        new_name = self.config["naming_convention"].format(
            project=self.project,
            asset=asset_base,
            variant=self.variant,
            version=self.version_counter,
            ext=extension,
        )
        new_filepath = filepath.with_name(new_name)

        if old_name == new_name:
            self.results.append(
                {
                    "old": old_name,
                    "new": new_name,
                    "status": "[yellow]Ignorado (Ya cumple)",
                }
            )
            return

        if self.dry_run:
            self.results.append(
                {
                    "old": old_name,
                    "new": new_name,
                    "status": "[blue]Pendiente (Dry Run)",
                }
            )
            logger.info(f"Dry Run: {old_name} -> {new_name}")
        else:
            filepath.rename(new_filepath)
            self.results.append(
                {"old": old_name, "new": new_name, "status": "[green]Renombrado OK"}
            )
            logger.info(f"Renamed: {old_name} -> {new_name}")

        self.version_counter += 1


# ==========================================
# PUNTO DE ENTRADA CLI
# ==========================================
def main():
    parser = argparse.ArgumentParser(
        description="Normalizador masivo de nombres de Assets (Pipeline TD)."
    )
    parser.add_argument(
        "directory", type=str, help="Carpeta objetivo con los archivos a renombrar."
    )
    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Acrónimo del proyecto (ej: PRJ1).",
    )
    parser.add_argument(
        "-v",
        "--variant",
        type=str,
        default="base",
        help="Variante del asset (ej: base, proxy, high).",
    )
    # El flag --apply invierte el dry-run por defecto. Si no se pone, dry_run = True.
    parser.add_argument(
        "--apply", action="store_true", help="EJECUTA los cambios físicos en el disco."
    )

    args = parser.parse_args()

    target_path = Path(args.directory).resolve()
    # Si --apply está presente, dry_run es False. Si no está, dry_run es True.
    is_dry_run = not args.apply

    config_path = Path("config.json")
    if not config_path.exists():
        console.print(
            "[bold red]ERROR CRÍTICO: No se encontró el archivo config.json[/bold red]"
        )
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        project_config = json.load(f)

    renamer = ProjectRenamer(
        target_dir=target_path,
        project=args.project,
        variant=args.variant,
        config=project_config,
        dry_run=is_dry_run,
    )
    renamer.run()


if __name__ == "__main__":
    main()
