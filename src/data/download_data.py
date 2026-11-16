"""Descarga el CSV original del conjunto oficial de alquiler municipal."""
from pathlib import Path
import requests

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "data" / "bronze" / "alquiler_municipios_original.csv"
URL = "https://analisi.transparenciacatalunya.cat/api/v3/views/qww9-bvhh/export.csv?accessType=DOWNLOAD"


def main():
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    print(f"Descargando datos desde: {URL}")
    respuesta = requests.get(URL, timeout=120)
    respuesta.raise_for_status()
    if not respuesta.content:
        raise RuntimeError("La respuesta de la fuente está vacía.")
    DESTINO.write_bytes(respuesta.content)
    print(f"Archivo guardado: {DESTINO}")
    print(f"Tamaño: {len(respuesta.content):,} bytes")


if __name__ == "__main__":
    main()
